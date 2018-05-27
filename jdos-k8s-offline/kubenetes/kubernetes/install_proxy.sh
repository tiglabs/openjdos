#!/bin/bash


MASTER_ADDRESS=${1:-"$1"}
NODE_ADDRESS=${2:-"$2"}

cat <<EOF >/etc/kubernetes/kube-proxy
# --logtostderr=true: log to standard error instead of files
KUBE_LOGTOSTDERR="--logtostderr=false"
KUBE_LOG_DIR="--log-dir=/var/log/kubernetes"
#  --v=0: log level for V logs
KUBE_LOG_LEVEL="--v=2"
# --hostname-override="": If non-empty, will use this string as identification instead of the actual hostname.
NODE_HOSTNAME="--hostname-override=${NODE_ADDRESS}"
# --master="": The address of the Kubernetes API server (overrides any value in kubeconfig)
KUBE_MASTER="--master=http://${MASTER_ADDRESS}:8080"
EOF

KUBE_PROXY_OPTS="   \${KUBE_LOGTOSTDERR} \\
                    \${KUBE_LOG_DIR}     \\
                    \${KUBE_LOG_LEVEL}   \\
                    \${NODE_HOSTNAME}    \\
                    \${KUBE_MASTER}"

cat <<EOF >/usr/lib/systemd/system/kube-proxy.service
[Unit]
Description=Kubernetes Proxy
After=network.target
[Service]
EnvironmentFile=-/etc/kubernetes/kube-proxy
ExecStart=/usr/bin/kube-proxy ${KUBE_PROXY_OPTS}
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable kube-proxy
systemctl restart kube-proxy
