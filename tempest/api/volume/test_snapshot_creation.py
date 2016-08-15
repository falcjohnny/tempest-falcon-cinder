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
import uuid
import base64

from oslo_log import log as logging
from tempest.common.utils import data_utils as utils
from tempest.api.volume import base
from tempest import config
from tempest import test

LOG = logging.getLogger(__name__)
CONF = config.CONF

@attr(type='falcon')
class VolumesV2SnapshotCreationTestJSON(base.BaseVolumeTest):

    @classmethod
    def skip_checks(cls):
        super(VolumesV2SnapshotCreationTestJSON, cls).skip_checks()
        if not CONF.volume_feature_enabled.snapshot:
            raise cls.skipException("Cinder volume snapshots are disabled")

    @classmethod
    def resource_setup(cls):
        super(VolumesV2SnapshotCreationTestJSON, cls).resource_setup()
	cls.name_field = cls.special_fields['name_field']
        cls.volume_type = CONF.volume.storage_protocol
	vol_name = utils.rand_name('Volume')
        params = {cls.name_field: vol_name,'volume_type': cls.volume_type}
        cls.volume_origin = cls.create_volume(**params)


    """def _encode_name(self,name):
    	uuid_str = name.replace("-", "")
    	vol_uuid = uuid.UUID('urn:uuid:%s' % uuid_str)
    	snap_id_encoded = base64.b64encode(vol_uuid.bytes)
    	newuuid = snap_id_encoded.replace("=", "")
    	return "cinder-" + newuuid
"""
    def test_snapshot_creation(self):
        # Create a snapshot
        s_name = utils.rand_name('snap')
        params = {self.name_field: s_name}
        snapshot = self.create_snapshot(self.volume_origin['id'], **params)

        # Get the snap and check for some of its details
        snap_get = self.snapshots_client.show_snapshot(snapshot['id'])
	for key, value in snap_get.iteritems() :
            print key, value
        print "-----------------------------------"
	#encode_snap_name = self._encode_name(snap_get['id'])
        
	self.assertEqual(self.volume_origin['id'],
                         snap_get['snapshot']['volume_id'],
                         "Referred volume origin mismatch")
	
	self.assertEqual(snap_get['snapshot']['metadata']['fss_tm_comment'],
			 snapshot['name'],
			 "snapshot name in timemark comment mismatch")


#class VolumesV1SnapshotTestJSON(VolumesV2SnapshotCreationTestJSON):
#    _api_version = 1
