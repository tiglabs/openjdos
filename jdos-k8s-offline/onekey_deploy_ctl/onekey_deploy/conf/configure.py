# -*- coding: utf-8 -*-
import ConfigParser
from utils.utils import merge_dicts

'''
    1通过conf.ini文件解析所要创建的集群节点信息
    2修改ansible 配置信息
    3通过snsible 完成集群创建
'''


class configure():
    '集群配置类'
    '''etcd_list: {'ip':'pw',....}'''
    '''k8s_list: {'ip':'pw',....}'''
    '''all_host_list: {'ip':'pw',....}'''

    def __init__(self, file_path):

        if not file_path:
            print 'file_path null'

        self.etcd_cluster = {}
        self.k8s_cluster = {}
        self.k8s_master = {}

        conf = ConfigParser.ConfigParser()
        conf.read(file_path)
        sections = conf.sections()
        for section in sections:
            if "etcd_cluster" == section:
                etcds = conf.options(section)
                for etcd in etcds:
                    self.etcd_cluster[etcd] = conf.get(section, etcd)

            if "k8s_cluster" == section:
                k8ss = conf.options(section)
                for k8s in k8ss:
                    self.k8s_cluster[k8s] = conf.get(section, k8s)

            if "k8s_master" == section:
                k8sms = conf.options(section)
                for k8sm in k8sms:
                    self.k8s_master[k8sm] = conf.get(section, k8sm)

            ## merge etcd node list and k8s node list
        self.all_host_list = merge_dicts(self.etcd_cluster, self.k8s_cluster, self.k8s_master)

    def check_configure(self):
        '''检查获取到到配置信息是否正确
        k8s_cluster 与 k8s_master 必须是 etcd_cluster 的子集
        存在不同cluster中的主机密码必须一致
        '''
        for (k8s_node_ip, k8s_node_passwd) in self.k8s_cluster.items():
            if not self.etcd_cluster.has_key(k8s_node_ip):
                return False, "k8s_cluster node:%s not belong to etcd_cluster" % k8s_node_ip
            if k8s_node_passwd != self.etcd_cluster.get(k8s_node_ip):
                return False, "k8s_cluster node:%s password difference with etcd_node" % k8s_node_ip

        for (k8sm_node_ip, k8sm_node_passwd) in self.k8s_master.items():
            if not self.etcd_cluster.has_key(k8sm_node_ip):
                return False, "k8s_master node:%s not belong to etcd_cluster" % k8sm_node_ip
            if k8sm_node_passwd != self.etcd_cluster.get(k8sm_node_ip):
                return False, "k8s_master node:%s password difference with etcd_node" % k8sm_node_ip
        return True, ''
