# tempest-falcon-cinder
## Install tempest:
```bash  
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
```

## How to run tempest tests:
```bash
  cd tempest/
  mkdir watcher-cloud
  tempest init --config-dir ./etc watcher-cloud
  cd watcher-cloud/
  cd etc/
  cp tempest.conf.sample tempest.conf
```
(To set your configuration with Openstack)
```bash
  vim tempest.conf 
```
  
  Copy your customized test scripts to /tempest/api/volume/
   
  Try to run tests:
  ```bash
  ./run_tempest.sh --config watcher-cloud/etc/tempest.conf -N -- tempest.api.volume.v2.test_volumes_list
  ```
   or
  ```bash
  nosetests  tempest.api.volume.test_volumes_creation
  ```

## How to run specified type of test cases:
```bash
  pip install mock
  pip install oslotest
  pip install pep8
```
Put "from nose.plugins.attrib import attr" in the script
And then put @attr(type='falcon') in below:
* Set @attr only on a method
* @attr can be used on a class to set attributes on all its test methods at once

Run the tests with type is 'falcon'
```bash
  nosetests  -a type='falcon'
```
