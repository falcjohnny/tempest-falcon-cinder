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
from tempest.api.volume import base
from tempest.common.utils import data_utils
from tempest.common import waiters
from tempest import config
from tempest.lib import decorators
from tempest import test

CONF = config.CONF

@attr(type='falcon')
class VolumesV2SnapshotTestJSON(base.BaseVolumeTest):

    @classmethod
    def skip_checks(cls):
        super(VolumesV2SnapshotTestJSON, cls).skip_checks()
        if not CONF.volume_feature_enabled.snapshot:
            raise cls.skipException("Cinder volume snapshots are disabled")

    @classmethod
    def resource_setup(cls):
        super(VolumesV2SnapshotTestJSON, cls).resource_setup()
        cls.volume_origin = cls.create_volume()

        cls.name_field = cls.special_fields['name_field']
        cls.volume_type = CONF.volume.storage_protocol
        #cls.descrip_field = cls.special_fields['descrip_field']
        # Create 1 snapshot
        #for _ in xrange(1):
        #cls.create_snapshot(cls.volume_origin['id'])

    
    @test.idempotent_id('677863d1-3142-456d-b6ac-9924f667a7f4')
    def test_volume_from_snapshot(self):
        # Create a temporary snap using wrapper method from base, then
        # create a snap based volume and deletes it
        snapshot = self.create_snapshot(self.volume_origin['id'])
        # NOTE(gfidente): size is required also when passing snapshot_id
        volume = self.volumes_client.create_volume(
            snapshot_id=snapshot['id'])['volume']
        waiters.wait_for_volume_status(self.volumes_client,
                                       volume['id'], 'available')
         # Get Volume information
        fetched_volume = self.volumes_client.show_volume(volume['id'])
        """print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        for key, value in fetched_volume.iteritems() :
            print key, value
        print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        """
        self.assertTrue(fetched_volume['volume']['metadata'].has_key('FSS-vid'))
        self.assertIsNotNone(fetched_volume['volume']['metadata']['FSS-vid'])

        self.cleanup_snapshot(snapshot)
        self.volumes_client.delete_volume(volume['id'])
        self.volumes_client.wait_for_resource_deletion(volume['id'])

    """@test.idempotent_id('db4d8e0a-7a2e-41cc-a712-961f6844e896')
    def test_snapshot_list_param_limit(self):
        # List returns limited elements
        self._list_snapshots_by_param_limit(limit=1, expected_elements=1)

    @test.idempotent_id('a1427f61-420e-48a5-b6e3-0b394fa95400')
    def test_snapshot_list_param_limit_equals_infinite(self):
        # List returns all elements when request limit exceeded
        # snapshots number
        snap_list = self.snapshots_client.list_snapshots()['snapshots']
        self._list_snapshots_by_param_limit(limit=100000,
                                            expected_elements=len(snap_list))

    @decorators.skip_because(bug='1540893')
    @test.idempotent_id('e3b44b7f-ae87-45b5-8a8c-66110eb24d0a')
    def test_snapshot_list_param_limit_equals_zero(self):
        # List returns zero elements
        self._list_snapshots_by_param_limit(limit=0, expected_elements=0)
    """
    def cleanup_snapshot(self, snapshot):
        # Delete the snapshot
        self.snapshots_client.delete_snapshot(snapshot['id'])
        self.snapshots_client.wait_for_resource_deletion(snapshot['id'])
        #self.snapshots.remove(snapshot)


#class VolumesV1SnapshotTestJSON(VolumesV2SnapshotTestJSON):
#    _api_version = 1
