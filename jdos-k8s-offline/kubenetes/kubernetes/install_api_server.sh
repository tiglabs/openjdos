#!/bin/bash

MASTER_ADDRESS=${1:-"$1"}
ETCD_SERVERS="http://${2}:2379"
SERVICE_CLUSTER_IP_RANGE=${3:-"$3"}
ADMISSION_CONTROL=${4:-"AlwaysAdmit"}
mkdir -p /etc/kubernetes
 
cat <<EOF >/etc/kubernetes/kube-apiserver
# --alsologtostderr=true: log to standard error as well as log file
KUBE_ALSO_LOGTOSTDERR="--alsologtostderr=true"
# --log-dir
KUBE_LOG_DIR="--log-dir=/var/log/kubernetes"
# --v=0: log level for V logs
KUBE_LOG_LEVEL="--v=2"
#stderrthreshold: only show log that over the threshold to stderr
STDERR_THRESHOLD="--stderrthreshold=2"
# --etcd-servers=[]: List of etcd servers to watch (http://ip:port),
# comma separated. Mutually exclusive with -etcd-config
KUBE_ETCD_SERVERS="--etcd-servers=${ETCD_SERVERS}"
# --etcd-cafile="": SSL Certificate Authority file used to secure etcd communication.
#KUBE_ETCD_CAFILE="--etcd-cafile=/srv/kubernetes/etcd/ca.pem"
# --etcd-certfile="": SSL certification file used to secure etcd communication.
#KUBE_ETCD_CERTFILE="--etcd-certfile=/srv/kubernetes/etcd/client.pem"
# --etcd-keyfile="": key file used to secure etcd communication.
#KUBE_ETCD_KEYFILE="--etcd-keyfile=/srv/kubernetes/etcd/client-key.pem"
# --insecure-bind-address=127.0.0.1: The IP address on which to serve the --insecure-port.
KUBE_API_ADDRESS="--insecure-bind-address=0.0.0.0"
# --insecure-port=8080: The port on which to serve unsecured, unauthenticated access.
KUBE_API_PORT="--insecure-port=8080"
# --kubelet-port=10250: Kubelet port
NODE_PORT="--kubelet-port=10250"
# --advertise-address=<nil>: The IP address on which to advertise
# the apiserver to members of the cluster.
KUBE_ADVERTISE_ADDR="--advertise-address=${MASTER_ADDRESS}"
# --allow-privileged=false: If true, allow privileged containers.
KUBE_ALLOW_PRIV="--allow-privileged=false"
# --service-cluster-ip-range=<nil>: A CIDR notation IP range from which to assign service cluster IPs.
# This must not overlap with any IP ranges assigned to nodes for pods.
KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range=${SERVICE_CLUSTER_IP_RANGE}"
# --admission-control="AlwaysAdmit": Ordered list of plug-ins
# to do admission control of resources into cluster.
# Comma-delimited list of:
#   LimitRanger, AlwaysDeny, SecurityContextDeny, NamespaceExists,
#   NamespaceLifecycle, NamespaceAutoProvision, AlwaysAdmit,
#   ServiceAccount, DefaultStorageClass, DefaultTolerationSeconds, ResourceQuota
KUBE_ADMISSION_CONTROL="--admission-control=${ADMISSION_CONTROL}"
# --client-ca-file="": If set, any request presenting a client certificate signed
# by one of the authorities in the client-ca-file is authenticated with an identity
# corresponding to the CommonName of the client certificate.
#KUBE_API_CLIENT_CA_FILE="--client-ca-file=/srv/kubernetes/ca.crt"
# --tls-cert-file="": File containing x509 Certificate for HTTPS.  (CA cert, if any,
# concatenated after server cert). If HTTPS serving is enabled, and --tls-cert-file
# and --tls-private-key-file are not provided, a self-signed certificate and key are
# generated for the public address and saved to /var/run/kubernetes.
#KUBE_API_TLS_CERT_FILE="--tls-cert-file=/srv/kubernetes/server.cert"
# --tls-private-key-file="": File containing x509 private key matching --tls-cert-file.
#KUBE_API_TLS_PRIVATE_KEY_FILE="--tls-private-key-file=/srv/kubernetes/server.key"
##enable RBAC add-by-myf5.net
KUBE_RBAC="--authorization-mode=RBAC"
EOF
 
 
KUBE_APISERVER_OPTS="   \${KUBE_ALSO_LOGTOSTDERR}    \\
                        \${STDERR_THRESHOLD}         \\
                        \${KUBE_LOG_DIR}             \\
                        \${KUBE_LOG_LEVEL}           \\
                        \${KUBE_ETCD_SERVERS}        \\
                        \${KUBE_API_ADDRESS}         \\
                        \${KUBE_API_PORT}            \\
                        \${NODE_PORT}                \\
                        \${KUBE_ADVERTISE_ADDR}      \\
                        \${KUBE_ALLOW_PRIV}          \\
                        \${KUBE_SERVICE_ADDRESSES}   \\
                        \${KUBE_ADMISSION_CONTROL}   \\
                        \${KUBE_RBAC}"
 
 
cat <<EOF >/usr/lib/systemd/system/kube-apiserver.service
[Unit]
Description=Kubernetes API Server
Documentation=https://github.com/kubernetes/kubernetes
[Service]
EnvironmentFile=-/etc/kubernetes/kube-apiserver
ExecStart=/usr/bin/kube-apiserver ${KUBE_APISERVER_OPTS}
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF
 
systemctl daemon-reload
systemctl enable kube-apiserver
systemctl restart kube-apiserver
