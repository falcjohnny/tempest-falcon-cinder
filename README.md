# tempest-falcon-cinder
Install tempest:
      yum update -y
      yum install epel-release -y
      yum install -y python-pip
      pip install --upgrade pip

      git clone http://git.openstack.org/openstack/tempest
      yum install python-devel
      cd tempest/
    
      yum install python-cffi
      
      yum install libffi-devel
      yum install openssl-devel -y

      pip install --upgrade cffi
      pip install .

------------------------
How to run tempest tests:

   # cd tempest/
   # mkdir watcher-cloud
   # tempest init --config-dir ./etc watcher-cloud
   #cd watcher-cloud/
   #cd etc/
   #cp tempest.conf.sample tempest.conf
   # vim tempest.conf (To set your configuration with Openstack)
   Copy your customized test scripts to /tempest/api/volume/
   
   Try to run tests:
   ./run_tempest.sh --config watcher-cloud/etc/tempest.conf -N -- tempest.api.volume.v2.test_volumes_list
   or
   nosetests  tempest.api.volume.test_volumes_creation

----------------------------
How to run specified type of test cases?
# pip install mock
# pip install oslotest
# pip install pep8
Put "from nose.plugins.attrib import attr" in the script
And then put @attr(type='falcon') in below:
1) Set @attr only on a method
2) @attr can be used on a class to set attributes on all its test methods at once

Run the tests with type is 'falcon'
# nosetests  -a type='falcon'
