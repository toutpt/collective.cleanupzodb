from zope import interface
from zope import schema

from plone.app.z3cform import layout
from z3c.form import button, field, form, validator

from Products.CMFCore.utils import getToolByName

from zope.i18nmessageid import MessageFactory
from Products.statusmessages.interfaces import IStatusMessage
_ = MessageFactory('collective.cleanupzodb')

class IGenericSetupCleaner(interface.Interface):
    """GenericSetup Cleaner"""

    def remove_import_step(stepid):
        """Remove step created with import_steps.xml"""

class GenericSetupCleaner(object):

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

class IGenericSetupCleanerFormSchema(interface.Interface):
    """Form schema to let a person use the cleaner"""

    stepid = schema.ASCIILine(title=_(u"Step ID"))

class GenericSetupCleanerForm(form.Form):
    
    fields = field.Fields(IGenericSetupCleanerFormSchema)
    label = u"GenericSetup Cleaner Form"
    ignoreContext = True #we will never use the context

    @button.buttonAndHandler(_(u'Remove Import Step'),
                             name='remove_import_step')
    def remove_import_step(self, action):
        data, errors = self.extractData()
        if errors:
            return
        stepid = data.get('stepid',None)
        IGenericSetupCleaner(self.context).remove_import_step(stepid)
        IStatusMessage(self.request).add(_(u'step %s has been removed'))

    @button.buttonAndHandler(_(u'Remove Export Step'),
                             name='remove_export_step')
    def remove_export_step(self, action):
        data, errors = self.extractData()
        if errors:
            return
        stepid = data.get('stepid',None)
        IGenericSetupCleaner(self.context).remove_export_step(stepid)
        IStatusMessage(self.request).add(_(u'step %s has been removed'))

class GenericSetupCleanerPage(layout.FormWrapper):
    label = _(u"Cleanup portal_setup")
    form = GenericSetupCleanerForm
