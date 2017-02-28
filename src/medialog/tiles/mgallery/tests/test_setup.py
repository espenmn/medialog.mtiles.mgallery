# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from medialog.tiles.mgallery.testing import MEDIALOG_TILES_MGALLERY_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that medialog.tiles.mgallery is properly installed."""

    layer = MEDIALOG_TILES_MGALLERY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if medialog.tiles.mgallery is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'medialog.tiles.mgallery'))

    def test_browserlayer(self):
        """Test that IMedialogTilesMgalleryLayer is registered."""
        from medialog.tiles.mgallery.interfaces import (
            IMedialogTilesMgalleryLayer)
        from plone.browserlayer import utils
        self.assertIn(IMedialogTilesMgalleryLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = MEDIALOG_TILES_MGALLERY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['medialog.tiles.mgallery'])

    def test_product_uninstalled(self):
        """Test if medialog.tiles.mgallery is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'medialog.tiles.mgallery'))

    def test_browserlayer_removed(self):
        """Test that IMedialogTilesMgalleryLayer is removed."""
        from medialog.tiles.mgallery.interfaces import IMedialogTilesMgalleryLayer
        from plone.browserlayer import utils
        self.assertNotIn(IMedialogTilesMgalleryLayer, utils.registered_layers())
