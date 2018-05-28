#!/bin/bash
 
 
MASTER_ADDRESS=${1:-"$1"}
 
cat <<EOF >/etc/kubernetes/kube-controller-manager
KUBE_LOGTOSTDERR="--logtostderr=false"
KUBE_LOG_DIR="--log-dir=/var/log/kubernetes"
KUBE_LOG_LEVEL="--v=4"
KUBE_MASTER="--master=${MASTER_ADDRESS}:8080"
 
KUBE_CLUSTER_CIDR="--cluster-cidr=10.1.0.0/16"
 
# --root-ca-file="": If set, this root certificate authority will be included in
# service account's token secret. This must be a valid PEM-encoded CA bundle.
#KUBE_CONTROLLER_MANAGER_ROOT_CA_FILE="--root-ca-file=/srv/kubernetes/ca.crt"
 
# --service-account-private-key-file="": Filename containing a PEM-encoded private
# RSA key used to sign service account tokens.
#KUBE_CONTROLLER_MANAGER_SERVICE_ACCOUNT_PRIVATE_KEY_FILE="--service-account-private-key-file=/srv/kubernetes/server.key"
 
# --leader-elect
KUBE_LEADER_ELECT="--leader-elect=false"
EOF
 
KUBE_CONTROLLER_MANAGER_OPTS="  \${KUBE_LOGTOSTDERR} \\
                                \${KUBE_LOG_DIR}     \\
                                \${KUBE_LOG_LEVEL}   \\
                                \${KUBE_MASTER}      \\
                                \${KUBE_CLUSTER_CIDR}\\
                                \${KUBE_LEADER_ELECT}"
 
cat <<EOF >/usr/lib/systemd/system/kube-controller-manager.service
[Unit]
Description=Kubernetes Controller Manager
Documentation=https://github.com/kubernetes/kubernetes
After=kube-apiserver.service
After=network.target
Requires=kube-apiserver.service
 
[Service]
EnvironmentFile=-/etc/kubernetes/kube-controller-manager
ExecStart=/usr/bin/kube-controller-manager ${KUBE_CONTROLLER_MANAGER_OPTS}
Restart=on-failure
 
[Install]
WantedBy=multi-user.target
EOF
 
systemctl daemon-reload
systemctl enable kube-controller-manager
systemctl restart kube-controller-manager
