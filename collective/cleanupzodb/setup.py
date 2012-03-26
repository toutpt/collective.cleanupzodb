from zope import interface
from zope import schema

from plone.app.z3cform import layout
from z3c.form import button, field, form, validator

from Products.CMFCore.utils import getToolByName

from zope.i18nmessageid import MessageFactory
from Products.statusmessages.interfaces import IStatusMessage
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
_ = MessageFactory('collective.cleanupzodb')

class IGenericSetupCleaner(interface.Interface):
    """GenericSetup Cleaner"""

    def remove_import_step(stepid):
        """Remove step created with import_steps.xml"""

    def remove_export_step(stepid):
        """Remove step created with export_steps.xml"""

class GenericSetupCleaner(object):
    interface.implements(IGenericSetupCleaner)

    def __init__(self, context):
        self.context = context

    def remove_import_step(self, stepid):
        context = getToolByName(self.context, 'portal_setup')
        registry = context.getImportStepRegistry()
        if stepid in registry.listSteps():
            registry.unregisterStep(stepid)
            context._p_changed = True

    def remove_export_step(self, stepid):
        context = getToolByName(self.context, 'portal_setup')
        registry = context.getExportStepRegistry()
        if stepid in registry.listSteps():
            registry.unregisterStep(stepid)
            context._p_changed = True

class StepVocabulary(object):
    interface.implements(IVocabularyFactory)
    
    def __call__(self, context):
        portal_setup = getToolByName(context, 'portal_setup')
        registry = portal_setup.getImportStepRegistry()
        steps = registry.listSteps()
        terms = [SimpleTerm('import-%s'%str(i),
                            'import-%s'%str(i),
                            u'import: %s'%i) for i in steps]
        registry = portal_setup.getExportStepRegistry()
        steps = registry.listSteps()
        terms += [SimpleTerm('export-%s'%str(i),
                            'export-%s'%str(i),
                            u'export: %s'%i) for i in steps]
        return SimpleVocabulary(terms)

StepVocabularyFactory = StepVocabulary()

class IGenericSetupCleanerFormSchema(interface.Interface):
    """Form schema to let a person use the cleaner"""

    stepid = schema.Choice(title=_(u"Step ID"),
                           vocabulary="collective.cleanupzodb.steps")

class GenericSetupCleanerForm(form.Form):
    
    fields = field.Fields(IGenericSetupCleanerFormSchema)
    label = u"GenericSetup Cleaner Form"
    ignoreContext = True #we will never use the context

    @button.buttonAndHandler(_(u'Remove Step'),
                             name='remove_step')
    def remove_step(self, action):
        data, errors = self.extractData()

        if errors:
            return

        step = data.get('stepid')
        step_type = step[:6]
        stepid = step[7:]

        if step_type == 'import':
            IGenericSetupCleaner(self.context).remove_import_step(stepid)
        else:
            IGenericSetupCleaner(self.context).remove_export_step(stepid)

        IStatusMessage(self.request).add(_(u'step %s has been removed'))
        url = self.context.absolute_url()+'/@@cleanup-portal_setup'
        self.request.response.redirect(url)


class GenericSetupCleanerPage(layout.FormWrapper):
    label = _(u"Cleanup portal_setup")
    form = GenericSetupCleanerForm
