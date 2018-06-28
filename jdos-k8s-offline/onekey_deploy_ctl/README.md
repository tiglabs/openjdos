工程目录结构
    1：conf    存放 conf.ini 文件
        ---内容示例如下
        [etcd-cluster]       ### 集群名称
        10.8.14.200:111111   ### 主机列表  -》  ip:password
        10.8.14.201:111111
        10.8.14.202:111111
        [k8s-cluster]
        10.8.14.200:111111
        10.8.14.201:111111
        10.8.14.202:111111

    2：etcd_cluster  创建etcd 集群相关
    3：k8s_cluster   创建k8s 集群相关

    4：install_rpm   需要安装到rpm，根据install.ini  文件内容自动安装到目标主机
        ---内容示例如下
        [etcd-cluster]     ### 集群名称    与 conf.ini 对应
        etcd-3.2.18-1.el7.x86_64.rpm   ## 该集群主机需要安装到rpm包
        若不指定本地安装，默认使用yum安装相关组件

    5：api_servcice   restful 接收到任务主处理方法
    6：command 通过shell 调用时的主处理方法
    7：k8s_nodes 创建主机 目前支持 aws ec2


    拷贝整个工程目录到安装环境执行
    python main.py 即可
    按照conf.ini与install.ini 配置到信息
    安装rpm包，

    创建etcd
    创建k8s master
    创建k8s node

    日志  /var/log/onekey_deploy/onekey_deploy.log

    eg. 本地安装rpm并创建集群
    ./sunshine-installer-0.0.1.bin -K onekey_deploy_ctl -create_etcd_cluster --host-list root:111111@10.8.14.200 root:111111@10.8.14.201 root:111111@10.8.14.202 -f /home/install_rpm/etcd-3.2.18-1.el7.x86_64.rpm -create_k8s_cluster --master-host-list root:111111@10.8.14.200 -fm /home/install_rpm/docker-1.13.1-63.git94f4240.el7.centos.x86_64.rpm /home/install_rpm/docker-common-1.13.1-63.git94f4240.el7.centos.x86_64.rpm /home/install_rpm/docker-client-1.13.1-63.git94f4240.el7.centos.x86_64.rpm /home/install_rpm/container-selinux-2.55-1.el7.noarch.rpm /home/install_rpm/oci-systemd-hook-0.1.15-2.gitc04483d.el7.x86_64.rpm /home/install_rpm/oci-register-machine-0-6.git2b44233.el7.x86_64.rpm /home/install_rpm/skopeo-containers-0.1.29-3.dev.git7add6fc.el7.x86_64.rpm /home/install_rpm/kubernetes-1.5.2-0.7.git269f928.el7.x86_64.rpm /home/install_rpm/kubernetes-node-1.5.2-0.7.git269f928.el7.x86_64.rpm /home/install_rpm/kubernetes-client-1.5.2-0.7.git269f928.el7.x86_64.rpm /home/install_rpm/kubernetes-master-1.5.2-0.7.git269f928.el7.x86_64.rpm /home/install_rpm/socat-1.7.3.2-2.el7.x86_64.rpm /home/install_rpm/libnetfilter_cthelper-1.0.0-9.el7.x86_64.rpm /home/install_rpm/libnetfilter_cttimeout-1.0.0-6.el7.x86_64.rpm /home/install_rpm/libnetfilter_queue-1.0.2-2.el7_2.x86_64.rpm /home/install_rpm/conntrack-tools-1.4.4-3.el7_3.x86_64.rpm --node-host-list root:111111@10.8.14.200 root:111111@10.8.14.201 root:111111@10.8.14.202 -fn /home/install_rpm/docker-1.13.1-63.git94f4240.el7.centos.x86_64.rpm /home/install_rpm/docker-common-1.13.1-63.git94f4240.el7.centos.x86_64.rpm /home/install_rpm/docker-client-1.13.1-63.git94f4240.el7.centos.x86_64.rpm /home/install_rpm/container-selinux-2.55-1.el7.noarch.rpm /home/install_rpm/oci-systemd-hook-0.1.15-2.gitc04483d.el7.x86_64.rpm /home/install_rpm/oci-register-machine-0-6.git2b44233.el7.x86_64.rpm /home/install_rpm/skopeo-containers-0.1.29-3.dev.git7add6fc.el7.x86_64.rpm /home/install_rpm/kubernetes-1.5.2-0.7.git269f928.el7.x86_64.rpm /home/install_rpm/kubernetes-node-1.5.2-0.7.git269f928.el7.x86_64.rpm /home/install_rpm/kubernetes-client-1.5.2-0.7.git269f928.el7.x86_64.rpm /home/install_rpm/kubernetes-master-1.5.2-0.7.git269f928.el7.x86_64.rpm /home/install_rpm/socat-1.7.3.2-2.el7.x86_64.rpm /home/install_rpm/libnetfilter_cthelper-1.0.0-9.el7.x86_64.rpm /home/install_rpm/libnetfilter_cttimeout-1.0.0-6.el7.x86_64.rpm /home/install_rpm/libnetfilter_queue-1.0.2-2.el7_2.x86_64.rpm /home/install_rpm/conntrack-tools-1.4.4-3.el7_3.x86_64.rpm


    restful 接口：


    目前提供接口
1、创建部署的接口
2、查询部署进度的接口
3、查询服务状态的接口
4、删除添加k8s集群结点
5、创建aws Ec2 主机
6、查询EC2主机状态

restfull  消息协议
{
"environment_type": 1:n,                    #### environment  处理类型 。         （服务端用来判断做什么，整数 1:n）
"environment_params": parms	     #### environment操作需要的参数	   （具体跟操作有关）
"environment_progress":Progress,   ####       任务执行进度		           （操作进度    float）
"environment_status":status,	     #####    任务状态                                （按需，running、finished、stop）
"environment_result":result，           ### 任务执行结果 			            （按需True、False   boolen）
"environment_desc":desc,	             ####      任务的功能描述                      （非必须，或者其他信息，如任务执行失败，携带失败信息）
"environment_time":"time",	             ####      任务的功能描述                      （非必须，或者其他信息，如任务执行失败，携带失败信息）
"environment_err": 0			     ####      任务错误号                              （0:无错误，其他数字查找错误代码）
}
调用时可选取部分参数，返回的结果包含所有参数，调用者按需获取自己关心的参数


一: 创建ks8集群任务
post url/environments/environment_id
post 参数
{
"environment_type": 1,
"environment_params": { "master-host-list":["root:111111@10.8.14.201"],
       "etcd-host-list":["root:111111@10.8.14.201", "root:111111@10.8.14.202", "root:111111@10.8.14.203"]}
"environment_params":"create  k8s cluster"
}
证书登陆改为如下
{
"environment_type": 1,
"environment_params": { "master-host-list":["10.8.14.201"],
       "etcd-host-list":["10.8.14.201", "10.8.14.202", "10.8.14.203"],
"node-host-list":["10.8.14.201", "10.8.14.202", "10.8.14.203"],
"certificate_path":"/root/.ssh/id_rsa"}
"environment_params":"create  k8s cluster"
}
返回结果
任务创建成功
{
"environment_type": 1,
"environment_progress":0.0
"environment_time":"2018-06-11 23:03:28"，
"environment_err": 0
}
任务创建失败
{
"environment_type": 1,
"environment_result":False，
"environment_desc":"task_parms error"，
"environment_time":"2018-06-11 23:03:28"，
"environment_err": 1
}


 二： 查询创建ks8集群任务进度(查询任务 environments= environment_id 创建集群任务进度)
get url/environments/environment_id/1
返回结果
1）：执行中
{
"environment_type": 1,
"environment_progress"  : 10.0 ,                                       ##  10%
"environment_status":"running"，				     ## 执行了10%
"environment_desc":"任务运行时信息" ，                        ## 创建过程中的日志信息
"environment_time":"2018-06-11 23:03:28"
 }
2）：执行成功结束
{
"environment_type": 1,
"environment_progress"  : 100.0 ,                      ##  100%
"environment_status":"finished"，                     ### 完成
"environment_desc":"任务结束时信息"，
"environment_result":True ，                              ### 执行成功
"environment_time":"2018-06-11 23:03:28"，
"environment_err": 0
 }
3）：任务失败，原因见environment_desc
{
"environment_type": 1,
"environment_progress"  : 65.0 ,
"environment_status":"stop"，                                        ### 任务执行65.0% 中止
"environment_desc":"任务错误信息"，
"environment_result":False，   				           #### 任务失败
"environment_time":"2018-06-11 23:03:28"，
"environment_err": 1
 }

三：查询服务状态
get url/environments/environment_id/2
返回值
{
"environment_type": 2,
"environment_params"  : "ip"          ###此处返回创建改集群是，创建的参数（不需要忽略即可）
"environment__progress"  : 100.0 ,
"environment__status":"finished"，
"environment__result":True,
"environment__desc":{node} ,                                  ###服务状态信息
"environment_time":"2018-06-11 23:03:28"，
"environment_err": 0
 }

"environment__desc":
{
"nodestatus":{
"node_name1":{
"STATUS":"readly",
"AGE":"1h"
},
"node_name2":{
"STATUS":"readly",
"AGE":"1h"
}
},
"componentstatus":{
"component_name1":{
"STATUS":"Healthy",
"MESSAGE":"ok",
"ERROR":""
},
"component_name2":{
"STATUS":"Healthy",
"MESSAGE":"ok",
"ERROR":""
}
}
}

四： 增加k8s  节点
post url/environments/environment_id  向environment_id 增加节点
{
"environment_type": 3,
"environment_params": { "master-host-list":["10.8.14.204"],         ### 增加的master 节点
       "etcd-host-list":["10.8.14.204"],                           ### 增加的etcd 节点
"node-host-list":["10.8.14.201"],                          ### 增加的计算 节点
"certificate_path":"/root/.ssh/id_rsa"}                  ### 证书
"environment_desc":"add   k8s cluster node"
}###各个类型节点列表都可选，有的则加入；证书不指定默认使用创建集群时的路径。
任务创建成功
{
"environment_type": 3,
"environment_progress":0.0，
"environment_time":"2018-06-11 23:03:28"，
"environment_err": 0
}
任务创建失败
{
"environment_type": 3,
"environment_result":False，
"environment_desc":"task_parms error"，
"environment_time":"2018-06-11 23:03:28"，
"environment_err": 1
}
五： 查询添加节点任务进度
get url/environments/environment_id/3
返回结果
1）：执行中
{
"environment_type": 3,
"environment_progress"  : 10.0 ,                                       ##  10%
"environment_status":"running"，				     ## 执行了10%
"environment_desc":"任务运行时信息" ，                        ## 创建过程中的日志信息
"environment_time":"2018-06-11 23:03:28"
 }
2）：执行成功结束
{
"environment_type":3,
"environment_progress"  : 100.0 ,                      ##  100%
"environment_status":"finished"，                     ### 完成
"environment_desc":"任务结束时信息"，
"environment_result":True ，                              ### 执行成功
"environment_time":"2018-06-11 23:03:28"，
"environment_err": 0
 }
3）：任务失败，原因见environment_desc
{
"environment_type": 3,
"environment_progress"  : 65.0 ,
"environment_status":"stop"，                                        ### 任务执行65.0% 中止
"environment_desc":"任务错误信息"，
"environment_result":False，   				           #### 任务失败
"environment_time":"2018-06-11 23:03:28"，
"environment_err": 2
 }

六： 删除k8s  节点
post url/environments/environment_id  向environment_id 删除节点
{
"environment_type": 4,
"environment_params": { "master-host-list":["10.8.14.204"],         ### 删除10.8.14.204 master 节点
       "etcd-host-list":["10.8.14.204"],                           ### 删除 的etcd 节点
"node-host-list":["10.8.14.201"],                          ### 删除 的计算 节点
"certificate_path":"/root/.ssh/id_rsa"}                  ### 证书
"environment_desc":"del   k8s cluster node"
}###各个类型节点列表都可选，有列表的则删除；证书不指定默认使用创建集群时的路径。
任务创建成功
{
"environment_type": 4,
"environment_progress":0.0，
"environment_time":"2018-06-11 23:03:28"，
"environment_err": 0
}
任务创建失败
{
"environment_type": 4,
"environment_result":False，
"environment_desc":"task_parms error"
"environment_time":"2018-06-11 23:03:28"，
"environment_err": 1
}
七： 查询删除节点任务进度
get url/environments/environment_id/4
返回结果
1）：执行中
{
"environment_type": 4,
"environment_progress"  : 10.0 ,                                       ##  10%
"environment_status":"running"，				     ## 执行了10%
"environment_desc":"任务运行时信息" ，                        ## 创建过程中的日志信息
"environment_time":"2018-06-11 23:03:28"
 }
2）：执行成功结束
{
"environment_type":4,
"environment_progress"  : 100.0 ,                      ##  100%
"environment_status":"finished"，                     ### 完成
"environment_desc":"任务结束时信息"，
"environment_result":True ，                              ### 执行成功
"environment_time":"2018-06-11 23:03:28"，
"environment_err": 0
 }
3）：任务失败，原因见environment_desc
{
"environment_type": 4,
"environment_progress"  : 65.0 ,
"environment_status":"stop"，                                        ### 任务执行65.0% 中止
"environment_desc":"任务错误信息"，
"environment_result":False，   				           #### 任务失败
"environment_time":"2018-06-11 23:03:28"，
"environment_err": 3
 }

八： 新建主机（目前只支持aws   ec2主机，只新建并不会自动加入集群）
post url/environments/environment_id  创建主机
{
"environment_type":5,
"environment_params": { "ImageId":"ami-02de0cb5595f2050d",    ### 选取的镜像id，通过aws网站可以获取（ami-02de0cb5595f2050d 社区版 centos7 镜像） 必选
       "certificate_Name":"My_key",                      ### 选择ssh登陆的密钥名称														  必选
"MinCount":1,                                              ### 创建的实例最小个数
"MaxCount":1,				             ### 创建的实例最大个数       一般创建成功个数
"node_type":"EC2"				     ### 虚拟机类型
}
"environment_params":"create  ec2 node"
}
九： 查询新建主机任务进度
get url/environments/environment_id/5
返回结果
1）：执行中
{
"environment_type": 5,
"environment_progress"  : 10.0 ,                                       ##  10%
"environment_status":"running"，				     ## 执行了10%
"environment_desc":"任务运行时信息" ，                        ## 创建过程中的日志信息
"environment_time":"2018-06-11 23:03:28"，
 }
2）：执行成功结束
{
"environment_type":5,
"environment_progress"  : 100.0 ,                      ##  100%
"environment_status":"finished"，                     ### 完成
"environment_desc":vm_info，                           ### 返回创建的主机列表信息（见下示例）
"environment_result":True ，                              ### 执行成功
"environment_time":"2018-06-11 23:03:28"，
"environment_err": 0
 }

### 返回创建的主机列表信息（见下示例）
 "environment_desc":
{"i-0ae4a68e06dfed856":{     ## 主机的id
         "public_dns_name": "ec2-18-216-173-182.us-east-2.compute.amazonaws.com",    ##主机的公有域名
 "private_ip_address": "172.31.15.184", 									      ##主机的私有地址
 "public_ip_address": "18.216.173.182", 									      ##主机的公有地址
 "private_dns_name": "ip-172-31-15-184.us-east-2.compute.internal"}}                      ##主机名

aws .  api 可用的几个条件
1: 操作主机时区时间正常，若不正常需要设置时区时间
timedatectl set-timezone 'Asia/Shanghai'
date -s "2018-06-28 15:22:30" .    时间不要根标准时间偏差超过2分钟

2: 配置aws 账号api 访问id和密码,操作的机房区域
调用时默认使用当前用户目录下
~/.aws/config .
     [default]
region = us-east-2     ##机房区域
output = json		     ### api 返回数据格式
~/.aws/credentials
[default]
aws_access_key_id = AKIAJ4LS6DHSKA62LYMQ           ###id
aws_secret_access_key = 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   ##password

可以用来创建集群或加入已经存在的结点（使用公有域名）
curl -i -X POST -H 'Content-type':'application/json' -d   '''{"environment_type": 1,"environment_params": {"master-host-list": ["ec2-18-222-114-79.us-east-2.compute.amazonaws.com"],"node-host-list": ["ec2-18-222-114-79.us-east-2.compute.amazonaws.com","ec2-18-191-150-83.us-east-2.compute.amazonaws.com"],"etcd-host-list":  ["ec2-18-221-114-165.us-east-2.compute.amazonaws.com","ec2-18-216-173-182.us-east-2.compute.amazonaws.com"],"certificate_path":"/home/My_key.pem","ssh-user":"maintuser"},"environment_desc": "创建k8s集群"}''' http://10.8.64.233:8383/environments/1234

certificate_path： 注意要和创建结点时certificate_Name对应。
*** 一般时在本地生产一个密钥对，上传公钥到aws服务器、本地保留私钥（通过aws创建密钥对也可以，创建完下载私钥）并指明密钥名字（这里是My_key），创建主机时aws自动把指定的公钥倒入虚拟机，结果就是任何持有对应私钥的ssh 客户端都可以登陆（ssh -i /home/My_key.pem  ***）
ssh-user：maintuser 这个跟具体的镜像有关，"ImageId":"ami-02de0cb5595f2050d" 这个centos 制作时就不允许root用户登陆，而是maintuser 这个用户。选择其他镜像时，需要更改这个。默认是root

3）：任务失败，原因见environment_desc
{
"environment_type": 5,
"environment_progress"  : 65.0 ,
"environment_status":"stop"，                                        ### 任务执行65.0% 中止
"environment_desc":"任务错误信息"，
"environment_result":False，   				           #### 任务失败
"environment_time":"2018-06-11 23:03:28"，
"environment_err": 4
 }

