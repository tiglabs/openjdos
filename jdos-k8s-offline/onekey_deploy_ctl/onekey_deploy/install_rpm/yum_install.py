# -*- coding:utf-8 -*-
import os
from utils.simple_ansible import simple_ansible
import json
from global_params import logger


### install rpm by yum

class yum_install():

    def __init__(self, node_list, rpms_list, state="present", private_key_file=None, ansible_ssh_user=None,
                 ansible_sudo_pass=None):
        self.node_list = node_list  ##ip1,ip2
        self.rpm_list = rpms_list  ##rpm1,rpm2
        self.state = state
        self.private_key_file = private_key_file
        self.ansible_ssh_user = ansible_ssh_user
        self.ansible_sudo_pass = ansible_sudo_pass

    def install(self):
        logger.info("yum install rpm:{%s}={%s}" % (str(self.node_list), str(self.rpm_list)))
        return_list = {"success": [],
                       "failed": []}
        if (not self.node_list) or (not self.rpm_list):
            logger.error("nodes or rpm null")

        yum_install_ansible = simple_ansible('yum install rpms ', '%s' % self.node_list, 'no', 'yum', 'name=%s state=%s'
                                             % (self.rpm_list, self.state), private_key_file=self.private_key_file,
                                             ansible_ssh_user=self.ansible_ssh_user,
                                             ansible_sudo_pass=self.ansible_sudo_pass)

        yum_return = yum_install_ansible.run()

        # for (host,str) in yum_return.item():

        hosts = self.node_list.split(',')
        for host in hosts:
            if host:
                if host in yum_return and yum_return.get(host) == '':
                    return_list["success"].append(host)
                else:
                    return_list["failed"].append(host)

        return return_list
