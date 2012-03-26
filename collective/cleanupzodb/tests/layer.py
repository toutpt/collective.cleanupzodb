from plone.testing import z2

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting

class Layer(PloneSandboxLayer):
    default_bases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.cleanupzodb
        self.loadZCML(package=collective.cleanupzodb)

        # Install product and call its initialize() function
        z2.installProduct(app, 'collective.cleanupzodb')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.cleanupzodb:default')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'collective.cleanupzodb')

FIXTURE = Layer()

INTEGRATION = IntegrationTesting(bases=(FIXTURE,),
                        name="collective.cleanupzodb:Integration")
FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,),
                        name="collective.cleanupzodb:Functional")
