# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
#
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

from tempest.common.utils import data_utils as utils
from tempest.api.volume import base
from tempest import config
from tempest import test
from tempest.common import waiters

CONF = config.CONF


class VolumeV2ManageTest(base.BaseVolumeTest):

    @classmethod
    def setup_clients(cls):
        super(VolumeV2ManageTest, cls).setup_clients()
        cls.client = cls.volume_manage_client
#    @classmethod
#    def skip_checks(cls):
#        super(VolumeV2ManageTest, cls).skip_checks()
#        if not CONF.volume_feature_enabled.snapshot:
#            raise cls.skipException("Cinder volume snapshots are disabled")

    @classmethod
    def resource_setup(cls):
        super(VolumeV2ManageTest, cls).resource_setup()
	#Create a volume
        cls.name_field = cls.special_fields['name_field']
        vol_name = utils.rand_name('Volume')
        params = {cls.name_field: vol_name,'volume_type': 'NSS'}
        cls.volume_origin = cls.create_volume(1,**params)
	#get fss_id
	cls.fetched_volume = cls.show_volume(cls.volume_origin['id'])
	cls.fss_id = cls.fetched_volume['metadata']['FSS-vid']
	#unmanage volume
	cls.unmanage_volume(cls.volume_origin['id'])

    def _delete_volume(self, volume_id):
        self.volumes_client.delete_volume(volume_id)
        self.volumes_client.wait_for_resource_deletion(volume_id)

    def test_manage_existing_volume(self):
        # Manage the existing volume.
	name = utils.rand_name("Volume")
        host_driver = "controller-h6-51@FSS#FSSFCDriver" 
        description = "manage_existing_volume"
	volume_type = "FSS-FC" 
        ref = {"ref": 
		{
            	"source-id": self.fss_id
        	}
	      }
        body = self.client.manage_existing_volume(name, host_driver, description, volume_type, **ref)
	waiters.wait_for_volume_status(body['id'], 'available')
        self.addCleanup(self._delete_volume, body['id'])
        self.volumes_client.wait_for_resource_deletion(body['id'])
	
	#self.assertRaises(KeyError, self.volumes_client.show_volume, body['id'])
        self.assertRaises(lib_exc.NotFound, self.volumes_client.show_volume, body['id'])

#class VolumeV1ManageTest(VolumeV2ManageTest):
#    _api_version = 1
