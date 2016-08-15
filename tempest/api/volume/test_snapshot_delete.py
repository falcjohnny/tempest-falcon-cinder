#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from nose.plugins.attrib import attr
import json
from oslo_log import log as logging
from tempest.common.utils import data_utils as utils
from tempest.lib import exceptions as lib_exc
from tempest.api.volume import base
from tempest import config
from tempest import test

LOG = logging.getLogger(__name__)
CONF = config.CONF

@attr(type='falcon')
class VolumesV2SnapshotDeleteTestJSON(base.BaseVolumeTest):

    @classmethod
    def skip_checks(cls):
        super(VolumesV2SnapshotDeleteTestJSON, cls).skip_checks()
        if not CONF.volume_feature_enabled.snapshot:
            raise cls.skipException("Cinder volume snapshots are disabled")

    @classmethod
    def setup_clients(cls):
        super(VolumesV2SnapshotDeleteTestJSON, cls).setup_clients()
        cls.client = cls.volumes_client

    @classmethod
    def resource_setup(cls):
        super(VolumesV2SnapshotDeleteTestJSON, cls).resource_setup()
	cls.name_field = cls.special_fields['name_field']
        cls.volume_type = CONF.volume.storage_protocol
	vol_name = utils.rand_name('Volume')
        params = {cls.name_field: vol_name,'volume_type': cls.volume_type}
        cls.volume_origin = cls.create_volume(**params)

	# Create a snapshot
        s_name = utils.rand_name('snap')
        params = {cls.name_field: s_name}
        cls.snapshot = cls.create_snapshot(cls.volume_origin['id'], **params)
	cls.snapshot1 = cls.create_snapshot(cls.volume_origin['id'], **params)
        
    def test_delete_one_snapshot_only(self):
        # delete one of snapshots - The timemark policy won't be disabled 
        self.snapshots_client.delete_snapshot(self.snapshot['id'])
        self.snapshots_client.wait_for_resource_deletion(self.snapshot['id'])

	#list snapshots
	list_snapshot = self.snapshots_client.list_snapshots()
        for key, value in list_snapshot.iteritems() :
            print key, value
	snaps_id_data = [(f['id']) for f in list_snapshot['snapshots']]
	self.assertEqual(snaps_id_data[0], self.snapshot1['id'])
        
        # Check if snapshot resource is deleted 
        self.assertRaises(lib_exc.NotFound, self.snapshots_client.show_snapshot,self.snapshot['id'])
    	
    def test_snapshot_delete(self):
        # delete all other snapshot - The timemark policy will be disabled 
        self.snapshots_client.delete_snapshot(self.snapshot1['id'])
        self.snapshots_client.wait_for_resource_deletion(self.snapshot1['id'])

        # Get Volume information
        fetched_volume = self.client.show_volume(self.volume_origin['id'])
        self.assertIsNone(fetched_volume['volume']['snapshot_id'])

        # Check if snapshot resource is deleted 
        self.assertRaises(lib_exc.NotFound, self.snapshots_client.show_snapshot,self.snapshot['id'])
        #self.assertTrue(self.snapshots_client.is_resource_deleted(self.snapshot['id']))
    

#class VolumesV1SnapshotTestJSON(VolumesV2SnapshotDeleteTestJSON):
#    _api_version = 1
