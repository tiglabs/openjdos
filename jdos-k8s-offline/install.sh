#!/bin/sh

# k8s all in one install script

echo 'welcome to install k8s all-in-one '
MASTER_ADDRESS="127.0.0.1"
NODE_LIST="127.0.0.1"
DNS_SERVER_IP=""
SERVICE_CLUSTER_IP_RANGE="10.0.0.0/16"
INSTALL_HOME=$(cd `dirname $0`; pwd)
INSTALL_ETCD_HOME="$INSTALL_HOME/etcd/v3.3.5"
INSTALL_K8S_HOME="$INSTALL_HOME/kubenetes/kubernetes"
INSTALL_DOCKER_HOME="$INSTALL_HOME/docker"
INSTALL_K8S_HOME="$INSTALL_HOME/kubenetes/kubernetes"

#install etcd
INSTALL_ETCD (){
    echo "start install etcd"
    cp -f $INSTALL_ETCD_HOME/etcd /usr/local/bin
    cp -f $INSTALL_ETCD_HOME/etcdctl /usr/local/bin
    mkdir -p /var/lib/etcd/
    mkdir -p /etc/etcd
    cp -f $INSTALL_ETCD_HOME/etcd.conf /etc/etcd
    cp -f $INSTALL_ETCD_HOME/etcd.service /usr/lib/systemd/system
    echo "etcd has installed,now begin to start"
    systemctl daemon-reload
    systemctl start etcd
    systemctl enable etcd
}

#install docker
INSTALL_DOCKER (){
    echo "start install docker"
    cd $INSTALL_DOCKER_HOME
    yum localinstall -y docker-engine*
    cp -f $INSTALL_DOCKER_HOME/docker.service /usr/lib/systemd/system/
    systemctl daemon-reload
    systemctl enable docker
}

#install kube master
INSTALL_MASTER (){
    echo "start install kube master , master ip is $MASTER_ADDRESS"
    cp -r $INSTALL_K8S_HOME/server/kubernetes/server/bin/* /usr/bin
    cd $INSTALL_K8S_HOME
    ./install_api_server.sh "$MASTER_ADDRESS" "$MASTER_ADDRESS" "$SERVICE_CLUSTER_IP_RANGE"
    echo "api server installed"
    ./install_controller_manager.sh "$MASTER_ADDRESS"
    echo "controller manager installed"
    ./install_shceduler.sh  "$MASTER_ADDRESS"
    echo "schedulder installed"
}

#install kube node
INSTALL_NODE (){
    echo "install kube node ,current node address $1"
    CURRENT_NODE_ADDRESS=$1
    cp -r $INSTALL_K8S_HOME/server/kubernetes/server/bin/* /usr/bin
    ./install_kubelet.sh "$MASTER_ADDRESS" "$CURRENT_NODE_ADDRESS" "$DNS_SERVER_IP"
    echo "kubelet installed"
    ./install_proxy.sh "$MASTER_ADDRESS" "$CURRENT_NODE_ADDRESS"
    echo "proxy installed"

}

#while getopts "m:s:n:d:" opt; do
#    case $opt in
#       m)
#         MASTER_ADDRESS="$OPTARG"
#         ;;
#       n)
#         NODE_LIST="$OPTARG"
#         ;;
#       s)
#         SERVICE_CLUSTER_IP_RANGE="$OPTARG"
#         ;;
#       d)
#         DNS_SERVER_IP="$OPTARG"
#         ;;
#       \?)
#         echo "Invalid option - $OPTARG"
#         exit 0
#         ;;
#     esac
#done
#if [ ! -n $MASTER_ADDRESS ];then
#    echo "kube master address can not be none"
#    exit 0
#fi

#stop firewall
systemctl disable firewalld.service
systemctl stop firewalld.service
INSTALL_ETCD
INSTALL_DOCKER
INSTALL_MASTER

for s in `echo "$NODE_LIST"|sed 's/,/\n/g'`
do
    INSTALL_NODE "$s"
done
exit 0

