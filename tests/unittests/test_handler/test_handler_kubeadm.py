# This file is part of cloud-init. See LICENSE file for license information.

from cloudinit.config import cc_kubeadm
from cloudinit.sources import DataSourceNone
from cloudinit import (distros, helpers, cloud)
from cloudinit.tests.helpers import CiTestCase, mock

import logging


LOG = logging.getLogger(__name__)


@mock.patch('cloudinit.config.cc_kubeadm._run_kubeadm')
class TestKubeadmHandle(CiTestCase):

    with_logs = True

    def setUp(self):
        super(TestKubeadmHandle, self).setUp()
        self.new_root = self.tmp_dir()
        self.conf = self.tmp_path('kubeadm.conf')

    def _get_cloud(self, distro):
        paths = helpers.Paths({'templates_dir': self.new_root})
        cls = distros.fetch(distro)
        mydist = cls(distro, {}, paths)
        myds = DataSourceNone.DataSourceNone({}, mydist, paths)
        return cloud.Cloud(myds, paths, {}, mydist, None)

    def test_handler_skips_missing_kubeadm_key_in_cloudconfig(self, m_auto):
        """Cloud-config containing no 'kubeadm' key is skipped."""
        mycloud = self._get_cloud('ubuntu')
        cfg = {}
        cc_kubeadm.handle('notimportant', cfg, mycloud, LOG, None)
        self.assertIn(
            "Skipping 'kubeadm' module, no config", self.logs.getvalue())
        self.assertEqual(0, m_auto.call_count)

    def test_handler_skips_missing_operation_key_in_cloudconfig(self, m_auto):
        """Cloud-config containing no 'kubeadm.operation' key is skipped."""
        mycloud = self._get_cloud('ubuntu')
        cfg = {'kubeadm': {'config': ''}}
        cc_kubeadm.handle('notimportant', cfg, mycloud, LOG, None)
        self.assertIn(
            "Skipping 'kubeadm' module, no operation specified",
            self.logs.getvalue())
        self.assertEqual(0, m_auto.call_count)

    def test_handler_skips_missing_config_key_in_cloudconfig(self, m_auto):
        """Cloud-config containing no 'kubeadm.config' key is skipped."""
        mycloud = self._get_cloud('ubuntu')
        cfg = {'kubeadm': {'operation': 'init'}}
        cc_kubeadm.handle('notimportant', cfg, mycloud, LOG, None)
        self.assertIn(
            "Skipping 'kubeadm' module, no config specified",
            self.logs.getvalue())
        self.assertEqual(0, m_auto.call_count)

    def test_handler_skips_unknown_operation_in_cloudconfig(self, m_auto):
        """Cloud-config containing unknown 'kubeadm.operation' value."""
        mycloud = self._get_cloud('ubuntu')
        cfg = {'kubeadm': {'operation': 'foo', 'config': ''}}
        cc_kubeadm.handle('notimportant', cfg, mycloud, LOG, None)
        self.assertIn(
            "Skipping 'kubeadm' module, unknown operation: foo",
            self.logs.getvalue())
        self.assertEqual(0, m_auto.call_count)
