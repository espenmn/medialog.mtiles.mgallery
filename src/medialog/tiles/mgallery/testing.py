# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import medialog.tiles.mgallery


class MedialogTilesMgalleryLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=medialog.tiles.mgallery)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'medialog.tiles.mgallery:default')


MEDIALOG_TILES_MGALLERY_FIXTURE = MedialogTilesMgalleryLayer()


MEDIALOG_TILES_MGALLERY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEDIALOG_TILES_MGALLERY_FIXTURE,),
    name='MedialogTilesMgalleryLayer:IntegrationTesting'
)


MEDIALOG_TILES_MGALLERY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MEDIALOG_TILES_MGALLERY_FIXTURE,),
    name='MedialogTilesMgalleryLayer:FunctionalTesting'
)


MEDIALOG_TILES_MGALLERY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        MEDIALOG_TILES_MGALLERY_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='MedialogTilesMgalleryLayer:AcceptanceTesting'
)
