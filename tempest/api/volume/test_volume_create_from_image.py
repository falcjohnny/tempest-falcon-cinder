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
import testtools
from testtools import matchers

from tempest.api.volume import base
from tempest.common.utils import data_utils
from tempest.common import waiters
from tempest import config
from tempest import test

CONF = config.CONF

@attr(type='falcon')
class VolumesV2CreateFromImageTest(base.BaseVolumeTest):

    @classmethod
    def setup_clients(cls):
        super(VolumesV2CreateFromImageTest, cls).setup_clients()
        cls.client = cls.volumes_client

    @classmethod
    def resource_setup(cls):
        super(VolumesV2CreateFromImageTest, cls).resource_setup()

        cls.name_field = cls.special_fields['name_field']
        cls.descrip_field = cls.special_fields['descrip_field']

    def _delete_volume(self, volume_id):
        self.client.delete_volume(volume_id)
        self.client.wait_for_resource_deletion(volume_id)

    def _volume_create_from_image(self, **kwargs):
        # Create a volume, Get it's details and Delete the volume
        volume = {}
        v_name = data_utils.rand_name('Volume')
        metadata = {'Type': 'Test'}
        # Create a volume
        kwargs[self.name_field] = v_name
        kwargs['metadata'] = metadata
        volume = self.client.create_volume(**kwargs)['volume']
        self.assertIn('id', volume)
        self.addCleanup(self._delete_volume, volume['id'])
        waiters.wait_for_volume_status(self.client, volume['id'], 'available')
        self.assertIn(self.name_field, volume)
        self.assertEqual(volume[self.name_field], v_name,
                         "The created volume name is not equal "
                         "to the requested name")
        self.assertTrue(volume['id'] is not None,
                        "Field volume id is empty or not found.")
        # Get Volume information
        fetched_volume = self.client.show_volume(volume['id'])['volume']
        self.assertEqual(v_name,
                         fetched_volume[self.name_field],
                         'The fetched Volume name is different '
                         'from the created Volume')
        self.assertEqual(volume['id'],
                         fetched_volume['id'],
                         'The fetched Volume id is different '
                         'from the created Volume')
        self.assertThat(fetched_volume['metadata'].items(),
                        matchers.ContainsAll(metadata.items()),
                        'The fetched Volume metadata misses data '
                        'from the created Volume')
        self.assertTrue(fetched_volume['metadata'].has_key('FSS-vid'))
        self.assertIsNotNone(fetched_volume['metadata']['FSS-vid'])
        self.assertEqual(CONF.compute.image_ref,
                         fetched_volume['volume_image_metadata']['image_id'],
                         'The fetched Volume image_id is different '
                         'from the created Image')

        if 'imageRef' in kwargs:
            self.assertEqual('true', fetched_volume['bootable'])
        if 'imageRef' not in kwargs:
            self.assertEqual('false', fetched_volume['bootable'])

    @test.services('image')
    def test_volume_create_from_image(self):
        image = self.compute_images_client.show_image(
            CONF.compute.image_ref)['image']
        min_disk = image.get('minDisk')
        disk_size = max(min_disk, CONF.volume.volume_size)
        self._volume_create_from_image(
            imageRef=CONF.compute.image_ref, size=disk_size)

#class VolumesV1CreateFromImageTest(VolumesV2CreateFromImageTest):
#    _api_version = 1
