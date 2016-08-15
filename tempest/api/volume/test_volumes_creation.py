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
from tempest.api.volume import base
from tempest import config
from tempest import test
from tempest.common import waiters
import testtools

import logging

CONF = config.CONF
#LOG = logging.getLogger(__name__)
@attr(type='falcon')
class VolumesV2CreationTest(base.BaseVolumeTest):

    @classmethod
    def setup_clients(cls):
        super(VolumesV2CreationTest, cls).setup_clients()
        cls.client = cls.volumes_client
      #  cls.image_client = cls.os.image_client

    @classmethod
    def resource_setup(cls):
        super(VolumesV2CreationTest, cls).resource_setup()

	cls.name_field = cls.special_fields['name_field']
        cls.volume_type = CONF.volume.storage_protocol
        # Create a test shared volume for attach/detach tests
        #cls.volume = cls.create_volume()
        #cls.client.wait_for_volume_status(cls.volume['id'], 'available')


    @classmethod
    def resource_cleanup(cls):
        # Delete the test instance

        super(VolumesV2CreationTest, cls).resource_cleanup()

    def _delete_volume(self, volume_id):
        self.client.delete_volume(volume_id)

    @test.idempotent_id('8596b978-89e9-4f55-ae70-4e4ec4158e8d')
    def test_create_volume(self):
	vol_name = utils.rand_name('Volume')
        params = {self.name_field: vol_name,'volume_type': self.volume_type}
        new_volume = self.client.create_volume(**params)['volume']
        waiters.wait_for_volume_status(self.client, new_volume['id'], 'available')
        #self.client.wait_for_volume_status(new_volume['id'], 'available')
	#self.assertNotEqual(new_volume['metadata'],{})
	self.assertTrue(new_volume['id'] is not None,
                        "Field volume id is empty or not found.")

	# Get Volume information
        fetched_volume = self.client.show_volume(new_volume['id'])
	print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        for key, value in fetched_volume.iteritems() :
            print key, value
        print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
	
	self.assertTrue(fetched_volume['volume']['metadata'].has_key('FSS-vid'))
	self.assertIsNotNone(fetched_volume['volume']['metadata']['FSS-vid'])

	self.addCleanup(self._delete_volume, new_volume['id'])
        #self.client.wait_for_volume_status(new_volume['id'], 'available')
        waiters.wait_for_volume_status(self.client, new_volume['id'], 'available')

    def test_create_thin_volume(self):
        vol_size = 10
        vol_name = utils.rand_name('Volume')
        metadata = {
                     "thinprovisioned": "true",
                     "thinsize": "1"
                   }
        params = {'size': vol_size,self.name_field: vol_name,'volume_type': self.volume_type,'metadata': metadata}
        new_volume = self.client.create_volume(**params)['volume']
        waiters.wait_for_volume_status(self.client, new_volume['id'], 'available')
        #self.assertNotEqual(new_volume['metadata'],{})
        self.assertTrue(new_volume['id'] is not None,
                        "Field volume id is empty or not found.")

        # Get Volume information
        fetched_volume = self.client.show_volume(new_volume['id'])
        print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        for key, value in fetched_volume.iteritems() :
            print key, value
        print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

        self.assertTrue(fetched_volume['volume']['metadata'].has_key('FSS-vid'))
        self.assertTrue(fetched_volume['volume']['metadata']['thinprovisioned'])
        self.assertIsNotNone(fetched_volume['volume']['metadata']['FSS-vid'])

        self.addCleanup(self._delete_volume, new_volume['id'])
        #self.client.wait_for_volume_status(new_volume['id'], 'available')
        waiters.wait_for_volume_status(self.client, new_volume['id'], 'available')
