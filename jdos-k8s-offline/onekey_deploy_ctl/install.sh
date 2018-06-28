#!/bin/sh
root_dir=`dirname $0`
cd $root_dir
rm -rf build dist onekey_deploy.egg-info

which virtualenv &>/dev/null
[ $? -ne 0 ] && echo "Need to install virtualenv before install sunshinectl." && exit 1
VIRTUAL_ENV=/var/lib/sunshine/virtualenv/sunshinectl
rm -rf $VIRTUAL_ENV
[ ! -d $VIRTUAL_ENV ] && virtualenv $VIRTUAL_ENV
source $VIRTUAL_ENV/bin/activate

python setup.py sdist
pip install --ignore-installed dist/*.tar.gz
# If you have own pypi server, please use followin line.
#pip install --ignore-installed dist/*.tar.gz -i http://10.0.101.1/pypi/simple
