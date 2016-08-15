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

from nose.plugins.attrib import attr
import time
from tempest.common.utils import data_utils as utils
from tempest.api.volume import base
from tempest import config
from tempest import test
from tempest.common import waiters
import testtools

import logging
logging.basicConfig(level=logging.INFO)
logger  = logging.getLogger(__name__)
CONF = config.CONF

@attr(type='falcon')
class VolumesV2CloneTest(base.BaseVolumeTest):

    @classmethod
    def setup_clients(cls):
        super(VolumesV2CloneTest, cls).setup_clients()
        cls.client = cls.volumes_client
      #  cls.image_client = cls.os.image_client

    @classmethod
    def resource_setup(cls):
        super(VolumesV2CloneTest, cls).resource_setup()
	# Create a volume
	cls.name_field = cls.special_fields['name_field']
        cls.volume_type = CONF.volume.storage_protocol
        vol_name = utils.rand_name('Volume')
        params = {cls.name_field: vol_name,'volume_type': cls.volume_type}
        cls.volume_origin = cls.create_volume(**params)

  #  @classmethod
#    def resource_cleanup(cls):
        # Delete the test instance

 #       super(VolumesV2CloneTest, cls).resource_cleanup()

    def _delete_volume(self, volume_id):
        self.client.delete_volume(volume_id)
        self.client.wait_for_resource_deletion(volume_id)

    def test_clone_volume(self):
	vol_name = utils.rand_name('Volume')
        params = {self.name_field: vol_name,'volume_type': self.volume_type, 'source_volid': self.volume_origin['id']} 
	#Bug : sync mirror and promote mirror issue
        new_volume = self.client.create_volume(**params)['volume']
        waiters.wait_for_volume_status(self.client, new_volume['id'], 'available')
	self.assertTrue(new_volume['id'] is not None,
                        "Field volume id is empty or not found.")

	# Get Volume information
        fetched_volume = self.client.show_volume(new_volume['id'])
	self.assertTrue(fetched_volume['volume']['metadata'].has_key('FSS-vid'))
	self.assertIsNotNone(fetched_volume['volume']['metadata']['FSS-vid'])
	#time.sleep(20)
	self.addCleanup(self._delete_volume, new_volume['id'])

