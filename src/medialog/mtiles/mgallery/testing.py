# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import medialog.mtiles.mgallery


class MedialogMTilesMgalleryLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=medialog.mtiles.mgallery)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'medialog.mtiles.mgallery:default')


MEDIALOG_MTILES_MGALLERY_FIXTURE = MedialogMTilesMgalleryLayer()


MEDIALOG_MTILES_MGALLERY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEDIALOG_MTILES_MGALLERY_FIXTURE,),
    name='MedialogMTilesMgalleryLayer:IntegrationTesting'
)


MEDIALOG_MTILES_MGALLERY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MEDIALOG_MTILES_MGALLERY_FIXTURE,),
    name='MedialogMTilesMgalleryLayer:FunctionalTesting'
)


MEDIALOG_MTILES_MGALLERY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        MEDIALOG_MTILES_MGALLERY_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='MedialogMTilesMgalleryLayer:AcceptanceTesting'
)
