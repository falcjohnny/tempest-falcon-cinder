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
from tempest.common.utils import data_utils as utils
from tempest.common import waiters
from tempest.api.volume import base
from tempest import config
from tempest import test
from tempest.lib import exceptions as lib_exc
import testtools
import logging

CONF = config.CONF
#LOG = logging.getLogger(__name__)
@attr(type='falcon')
class VolumesV2DeletionTest(base.BaseVolumeTest):

    @classmethod
    def setup_clients(cls):
        super(VolumesV2DeletionTest, cls).setup_clients()
        cls.client = cls.volumes_client
      #  cls.image_client = cls.os.image_client

    @classmethod
    def resource_setup(cls):
        super(VolumesV2DeletionTest, cls).resource_setup()

	cls.name_field = cls.special_fields['name_field']
        cls.volume_type = CONF.volume.storage_protocol
        # Create a test volume
	vol_name = utils.rand_name('Volume')
        params = {cls.name_field: vol_name,'volume_type': cls.volume_type}
        cls.volume = cls.create_volume(**params)
        waiters.wait_for_volume_status(cls.client, cls.volume['id'], 'available')


    @classmethod
    def resource_cleanup(cls):
        # Delete the test instance

        super(VolumesV2DeletionTest, cls).resource_cleanup()


    def test_delete_volume(self):
	self.client.delete_volume(self.volume['id'])
        self.client.wait_for_resource_deletion(self.volume['id'])

	# Get Volume information and volume not found is expected.
	# Check if the expected raise eexception will show
	self.assertRaises(lib_exc.NotFound, self.client.show_volume,self.volume['id'])
	#self.assertRaises(KeyError, self.client.show_volume, self.volume['id'])
	
	#get_volume_info = self.client.show_volume(self.volume['id'])
        #self.assertEqual(get_volume_info['message'], "Volume '" + self.volume['id'] + "' could not be found.")



