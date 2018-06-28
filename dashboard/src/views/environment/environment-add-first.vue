<style scoped>
  .main-title{
    padding:5px;
    font-size: 12px;
    color: #495060;
  }
</style>
<template>
  <div>
    <div v-if="value == 0">
      <Row style="margin:50px 0 20px;" >
        <Col span="14" offset="5">
          <Form ref="env" :model="env" :rules="ruleEnv" label-position="right" :label-width="100">
              <FormItem prop="envName" label="环境英文名">
                  <Input type="text" v-model="env.envName" size="large" placeholder="请给出合适的环境英文名"></Input>
              </FormItem>
          </Form>
        </Col>
      </Row>
      <Row>
        <Col span="11">
          <Card>
              <div style="text-align:center">
                  <div>
                    <Icon type="soup-can-outline" size="40"></Icon>
                    <span style="font-size:30px;font-weight:bold;">单节点部署</span>
                  </div>
                  <p style="margin:15px auto;">单节点部署是允许用户在单台机器、虚拟机或者云主机上进行安装部署kubenetes集群,其中安装的服务包括kubenetes、docker、dashboard等基础服务</p>
                  <Button @click="goToDeploy(1)">开始部署</Button>
              </div>
          </Card>
        </Col>
        <Col span="12" offset="1">
          <Card>
              <div style="text-align:center">
                  <div>
                    <Icon type="soup-can" size="40"></Icon>
                    <span style="font-size:30px;font-weight:bold;">集群部署</span>
                  </div>
                  <p style="margin:15px auto;">集群部署是允许用户部署一套高可用的kubenetes集群的方案，其中集群部署保证了整套环境的高可用、快速恢复等特性，一般生产环境都是使用集群方案部署</p>
                  <Button type="primary" @click="goToDeploy(2)">开始部署</Button>
              </div>
          </Card>
        </Col>
      </Row>
    </div>
    <div v-if="value == 1">
      <Row style="margin-top:40px;" >
        <Col span="24" v-if="env.deployType=='single'">
          <Alert type="warning" closable>
              <h4>环境部署-单节点</h4>
              <template slot="desc">单节点部署是允许用户在单台机器、虚拟机或者云主机上进行安装部署kubenetes集群,其中安装的服务包括kubenetes、docker、dashboard等基础服务. </template>
          </Alert>
        </Col>
        <Col span="24" v-if="env.deployType=='cluster'">
          <Alert type="warning" closable>
              <h4>环境部署-集群</h4>
              <template slot="desc">集群部署是允许用户在多台机器、虚拟机或者云主机上进行安装部署kubenetes集群,其中用户可以根据自己的要求进行合理安排分配机器安装的服务包括kubenetes、docker、dashboard等基础服务. </template>
          </Alert>
        </Col>
      </Row>
      <div  v-if="env.deployType=='single'">
        <Row>
          <Col span="1" offset="8" class="main-title" >
            *节点
          </Col>
          <Col span="13">
            <Select v-model="singleIp" style="width:200px">
              <Option v-for="ip in ips" :value="ip">
                  <span>{{ip}}</span>
              </Option>
          </Select>
          </Col>
        </Row>
      </div>
      <div v-else>
        <Row>
          <Col span="4">
            <Menu :active-name="currentName" @on-select="changeName">
                <MenuGroup title="配置主机">
                    <MenuItem name="master">
                        管理节点
                    </MenuItem>
                    <MenuItem name="node">
                        计算节点
                    </MenuItem>
                    <MenuItem name="store">
                        存储节点
                    </MenuItem>
                </MenuGroup>
            </Menu>
          </Col>
          <Col span="15">
            <div v-if="currentName=='master'">
              <EnvironmentAddIp v-model="ips" @on-ip="takeMaster" key="1"></EnvironmentAddIp>
              <Tag v-for="masterIp in masterHost">{{masterIp}}</Tag>
            </div>
            <div v-if="currentName=='node'">
              <EnvironmentAddIp v-model="ips" @on-ip="takeNode" key="2"></EnvironmentAddIp>
              <Tag v-for="nodeIp in nodeHost">{{nodeIp}}</Tag>
            </div>
            <div v-if="currentName=='store'">
              <EnvironmentAddIp v-model="ips" @on-ip="takeStore" key="3"></EnvironmentAddIp>
              <Tag v-for="storeIp in storeHost">{{storeIp}}</Tag>
            </div>
          </Col>
        </Row>
      </div>
      <Row>
        <Col span="24" style="text-align:center;margin-top:20px;">
          <Button @click="deployEnv">开始部署</Button>
        </Col>
      </Row>
    </div>
  </div>
</template>
<script>
import IpInput from '@/views/form/inputs/ip-inputs.vue'
import EnvironmentAddIp from './environment-add-ip.vue'
  export default {
    name:'EnvironmentAddFirst',
    props:["value"],
    components:{
			IpInput,EnvironmentAddIp
		},
    methods:{
      goToDeploy(deployType){
        this.$refs['env'].validate((valid) => {
            if (valid) {
              this.env.deployType = deployType == 1?'single':'cluster';
              this.$emit('input', 1);
              this.queryHost();
            }
        })
      },
      queryHost(){
        this.$http.get('/api/environment/host').then((response)=>{
          this.ips = response.data.filter((item)=>{
            return item.envId == null || item.envId == undefined;
          }).map((item)=>{
            return item.hostIp;
          });
        });
      },
      invokeCreateDeploy(param){
        this.$http.post('/api/environment',param).then((response)=>{
          this.$Notice.success({
                  title: '部署环境',
                  desc:'部署请求已经发送成功'
          });
          let taskId = response.data.envId;
          this.$emit('input', 2);
          this.$emit('on-installing', taskId);
          // this.$router.replace({path:'/environment/install/'+taskId})
        });
      },
      deploySingle(){
        let data = {
          envName:this.env.envName,deployType:this.env.deployType,masterHost:[this.singleIp],nodeHost:[this.singleIp],storeHost:[this.singleIp]
        }
        this.invokeCreateDeploy(data)
      },
      deployCluster(){
        let data = {
          envName:this.env.envName,deployType:this.env.deployType,masterHost:this.masterHost,nodeHost:this.nodeHost,storeHost:this.storeHost
        }
        this.invokeCreateDeploy(data)
      },
      deployEnv(){
        this.$Modal.confirm({
             title: '部署环境',
             content: '<p>确定要部署环境?</p>',
             onOk: () => {
               if(this.env.deployType == 'single'){
                  this.deploySingle();
               }else{
                  this.deployCluster();
               }
             }
         });
      },
      changeName(name){
        this.currentName = name;
      },
      takeMaster(ips){
        this.masterHost = ips;
      },
      takeNode(ips){
        this.nodeHost = ips;
      },
      takeStore(ips){
        this.storeHost = ips;
      }
    },
    data(){
      return {
        message:'',
        ips:[],
        singleIp:'',
        currentName:'master',
        masterHost:[],
        nodeHost:[],
        storeHost:[],
        env:{
          envName:'',deployType:''
        },ruleEnv:{
          envName:[
            { required: true, message: '请填写环境英文名称', trigger: 'blur' },
            {validator(rule, value, callback, source, options) {
              var errors = [];
              if(!/^[a-zA-Z][0-9a-zA-Z]{3,64}$/.test(value)) {
                errors.push(
                  new Error('请确保环境英文名字母开头,数字与字母组合的3-64位之内'));
              }
              callback(errors);
            }, trigger: 'blur'}
          ]
        }
      }
    }
  }
</script>
