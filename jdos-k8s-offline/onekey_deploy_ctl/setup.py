from setuptools import setup, find_packages
import sys, os

version = '1.0.0'

os.system("chmod +x ./onekey_deploy_ctl")
os.system("chmod +x ./onekey_deploy/onekey_deploy")
os.system("chmod +x ./onekey_deploy/onekey_deploy.service")
setup(name='onekey_deploy',
      version=version,
      description="onekey_deploy management tool",
      long_description="""\
onekey_deploy management tool""",
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='onekey_deploy',
      author='jd',
      author_email='abc@jd.com',
      url='',
      license='Apache 2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      # package_data={'':['onekey_deploy/conf/*', 'onekey_deploy/utils_bin/bin/*']},
      zip_safe=True,
      install_requires=[
          'argparse',
          'pexpect',
          'flask',
          'flask_restful',
          'termcolor',
          # 'ansible < 2.0',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      data_files=[('//usr/bin', ['onekey_deploy_ctl', 'onekey_deploy/utils_bin/bin/calicoctl']),
                  ('//etc/onekey_deploy', ['onekey_deploy/conf/conf.ini', 'onekey_deploy/conf/install.ini',
                                           'onekey_deploy/conf/calico-node.service']),
                  ('//etc/init.d', ['onekey_deploy/onekey_deploy']),
                  ('//usr/lib/systemd/system', ['onekey_deploy/onekey_deploy.service']),
                  ('//opt/cni/bin', ['onekey_deploy/utils_bin/bin/calico', 'onekey_deploy/utils_bin/bin/calico-ipam',
                                     'onekey_deploy/utils_bin/bin/loopback']),
                  ('//tmp', ['onekey_deploy/utils_bin/bin/nodemonitor-v1.0.0.tar.gz'])
                  ]
      )
