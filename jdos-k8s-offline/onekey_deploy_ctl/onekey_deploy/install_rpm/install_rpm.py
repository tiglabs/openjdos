# -*- coding: utf-8 -*-


import ConfigParser
import os
from utils.simple_ansible import simple_ansible
import json


class install_rpm():

    def __init__(self, configure=None, install_confpath='/etc/onekey_deploy/install.ini', rpm_list=None,
                 private_key_file=None, ansible_ssh_user=None, ansible_sudo_pass=None):
        '''
        :param configure:
        :param install_confpath:  default use
        :param rpm_list:
        '''
        '''rpm_list {"ip":"home/etcd-3.2.18-1.el7.x86_64.rpm /home/ansible-2.5.3-1.el7.noarch.rpm"}'''
        'configure'
        '''etcd_list: {'ip':'pw',....}'''
        '''k8s_list: {'ip':'pw',....}'''
        '''all_host_list: {'ip':'pw',....}'''

        self.installlist = {}
        self.private_key_file = private_key_file
        self.ansible_ssh_user = ansible_ssh_user
        self.ansible_sudo_pass = ansible_sudo_pass

        if rpm_list:
            self.installlist = rpm_list
            self.install_type = 'rpm_path'
        else:
            if not os.access(install_confpath, os.F_OK):
                print 'file not exits'
            self.install_type = 'configfile'
            conf = ConfigParser.ConfigParser()
            conf.read(install_confpath)

            sections = conf.sections()
            for section in sections:
                if section not in configure.__dict__:  ##   遍历
                    print "cannot find node list"
                    continue
                else:
                    for node in configure.__dict__[section]:
                        for rpm in conf.options(section):
                            if self.installlist.has_key(node):
                                rpm_name = rpm + '-' + conf.get(section, rpm) + '.rpm'
                                if rpm_name not in self.installlist[node]:
                                    self.installlist[node] = self.installlist[node] + ' ' + rpm + '-' + conf.get(
                                        section, rpm) + '.rpm'
                            else:
                                self.installlist[node] = rpm + '-' + conf.get(section, rpm) + '.rpm'

            # print self.installlist

    def copy_and_install(self):
        if not self.installlist:
            return False, "install list is null"
        # import pdb;pdb.set_trace()
        if self.install_type == 'rpm_path':
            for (host, rpms) in self.installlist.items():

                for rpm in rpms:
                    if not os.access(rpm, os.F_OK):
                        return False, rpm + " rpm not exists"

                    rpm_copy_ansible = simple_ansible('copy python file ', '%s,' % host, 'no', 'copy',
                                                      'src=%s dest=/home/install_rpm owner=root group=root mode=0777' % rpm,
                                                      private_key_file=self.private_key_file,
                                                      ansible_ssh_user=self.ansible_ssh_user,
                                                      ansible_sudo_pass=self.ansible_sudo_pass)
                    rpm_copy_ansible.run()

                    rpm_name = ""
                    try:
                        rpm_name = rpm.split('/')[-1]
                    except:
                        pass
                    if not rpm_name:
                        return False, "split rpm name  error"

                    # print rpm_name
                    rpm_install_ansible = simple_ansible('install rpm ', '%s,' % host, 'no', 'shell',
                                                         'cd /home/install_rpm/%s && rpm -Uvh %s --force' % (
                                                         rpm_name, rpm_name), private_key_file=self.private_key_file,
                                                         ansible_ssh_user=self.ansible_ssh_user,
                                                         ansible_sudo_pass=self.ansible_sudo_pass)
                    rpm_install_ansible.run()

        else:
            for (node, rpms) in self.installlist.items():
                print "拷贝、升级安装节点" + node + " rpm包:"
                # import pdb;pdb.set_trace()
                rpm_copy_ansible = simple_ansible('copy python file ', '%s,' % node, 'no', 'copy',
                                                  'src=/etc/onekey_deploy/install_rpm/rpm/ dest=/home/install_rpm owner=root group=root mode=0777',
                                                  private_key_file=self.private_key_file,
                                                  ansible_ssh_user=self.ansible_ssh_user,
                                                  ansible_sudo_pass=self.ansible_sudo_pass)
                rpm_copy_ansible.run()
                print "拷贝结束, 开始安装"
                # print abc
                # ('get remote hostname', hosts, 'no', 'shell', 'hostname')
                rpm_install_ansible = simple_ansible('install rpm ', '%s,' % node, 'no', 'shell',
                                                     'cd /home/install_rpm && rpm -Uvh %s --force'
                                                     % rpms, private_key_file=self.private_key_file,
                                                     ansible_ssh_user=self.ansible_ssh_user,
                                                     ansible_sudo_pass=self.ansible_sudo_pass)
                abc = rpm_install_ansible.run()
                try:
                    # ret_str =  json.dumps(abc[node]).decode('unicode-escape')
                    ret_str = abc[node]
                    for res in ret_str:
                        print res
                    print "安装结束\n"
                except:
                    pass
        return True, ""
