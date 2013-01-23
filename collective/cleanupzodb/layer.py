from zope import component
from plone.browserlayer.interfaces import ILocalBrowserLayerType


def remove_browser_layer(name):
    """this will remove browser layer even if the addon has been removed
    from the system.
    Created and used to remove collective.groupdashboard
    symptom: can't apply portlets import step ->
    2013-01-23 12:15:51 ERROR Zope.SiteErrorLog 1358939751.450.337074106184 ...
    Traceback (innermost last):
      Module ZPublisher.Publish, line 135, in publish
      Module Zope2.App.startup, line 291, in commit
      Module transaction._manager, line 93, in commit
      Module transaction._transaction, line 322, in commit
      Module transaction._transaction, line 416, in _commitResources
      Module ZODB.Connection, line 558, in commit
      Module ZODB.Connection, line 606, in _commit
      Module ZODB.Connection, line 640, in _store_objects
      Module ZODB.serialize, line 422, in serialize
      Module ZODB.serialize, line 431, in _dump
    PicklingError: Can't pickle
    <class 'collective.groupdashboard.interfaces.IGroupDashboardLayer'>:
    import of module collective.groupdashboard.interfaces failed
    """
#    name = "collective.groupdashboard"
    existing = component.queryUtility(ILocalBrowserLayerType, name=name)
    if existing is None:
        return

    site_manager = component.getSiteManager()

    site_manager.unregisterUtility(component=existing,
                                   provided=ILocalBrowserLayerType,
                                   name=name)
    site_manager._p_changed = True
