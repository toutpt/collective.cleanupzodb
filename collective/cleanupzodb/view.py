from zope import interface
from zope import schema
from zope.i18nmessageid import MessageFactory

from plone.app.z3cform import layout
from z3c.form import button, field, form, validator

from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

_ = MessageFactory('collective.cleanupzodb')

class ReplaceViewFormSchema(interface.Interface):
    """schema"""

    type = schema.Choice(title=_(u'Content type'),
                  vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes")

    old_view = schema.ASCIILine(title=_(u'Old view id'))

    new_view = schema.ASCIILine(title=_(u'New view id'))


class ReplaceViewForm(form.Form):

    fields = field.Fields(ReplaceViewFormSchema)
    label = u"Remove view Form"
    ignoreContext = True #we will never use the context

    @button.buttonAndHandler(_(u'Replace View'),
                             name='replace_view')
    def replace_view(self, action):
        data, errors = self.extractData()

        if errors:
            return

        ctype = data.get('type')
        old_view = data.get('old_view')
        new_view = data.get('new_view')

        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(portal_type=ctype)

        removed = 0
        for brain in brains:
            ob = brain.getObject()
            layout = ob.getLayout()
            if layout == old_view:
                ob.setLayout(new_view)
                removed +=1

        IStatusMessage(self.request).add('%s content updated'%removed)
        url = self.context.absolute_url()+'/@@cleanup-view'
        self.request.response.redirect(url)

class ReplaceViewPage(layout.FormWrapper):
    label = _(u"Cleanup view")
    form = ReplaceViewForm
