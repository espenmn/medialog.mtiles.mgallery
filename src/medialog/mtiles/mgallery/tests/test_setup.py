# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from medialog.mtiles.mgallery.testing import MEDIALOG_MTILES_MGALLERY_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that medialog.mtiles.mgallery is properly installed."""

    layer = MEDIALOG_MTILES_MGALLERY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if medialog.mtiles.mgallery is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'medialog.mtiles.mgallery'))

    def test_browserlayer(self):
        """Test that IMedialogMTilesMgalleryLayer is registered."""
        from medialog.mtiles.mgallery.interfaces import (
            IMedialogMTilesMgalleryLayer)
        from plone.browserlayer import utils
        self.assertIn(IMedialogMTilesMgalleryLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = MEDIALOG_MTILES_MGALLERY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['medialog.mtiles.mgallery'])

    def test_product_uninstalled(self):
        """Test if medialog.mtiles.mgallery is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'medialog.mtiles.mgallery'))

    def test_browserlayer_removed(self):
        """Test that IMedialogMTilesMgalleryLayer is removed."""
        from medialog.mtiles.mgallery.interfaces import IMedialogMTilesMgalleryLayer
        from plone.browserlayer import utils
        self.assertNotIn(IMedialogMTilesMgalleryLayer, utils.registered_layers())
