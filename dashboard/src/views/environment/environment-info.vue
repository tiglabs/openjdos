<style scoped>
  .env-line{
    list-style: none;
  }
  .env-line li{
    display: inline-block;
    padding:0 10px;
  }
  .env-line li span{
    display: inline-block;
    padding:0 5px 0 0;
  }
  .env-line li span:first-child{
    font-size: 14px;
    font-weight: bold;
  }
  .env-line li span:last-child{
    background: #80848f;
    padding: 2px 10px;
    border-radius: 5px;
    color: #fff;
  }
  .env-info{
    margin:30px 0 10px;
  }
  .service-list,.node-list{
    list-style: none;
  }
  .service-list li{
    margin:7px auto;
    min-width: 345px;
  }
  .service-list li span{
    display: inline-block;
    padding:0 15px 0 0;
    width:150px;
  }
  .service-list,.node-list li span.info-title{
    font-weight: bold
  }

</style>
<template>
  <div>
    <Row>
			<Col span="24">
				<Card>
					<div style="margin-bottom:10px;">
						<span style="font-size:20px;font-weight:bold;">环境详情</span>
            <Tag color="green" v-if="running.environment.status=='running'">运行中</Tag>
            <Tag color="blue" v-if="running.environment.status=='installing'">部署中</Tag>
            <Tag color="red" v-if="running.environment.status=='error'">异常</Tag>
            <Tag color="yellow" v-if="running.environment.status=='deleting'">删除中</Tag>
            &nbsp;&nbsp;&nbsp;&nbsp;
            <Dropdown  @on-click="envHandler">
               <a href="javascript:void(0)">
                   操作
                   <Icon type="arrow-down-b"></Icon>
               </a>
               <DropdownMenu slot="list">
                   <DropdownItem name="addNode">增加节点</DropdownItem>
               </DropdownMenu>
           </Dropdown>
					</div>
					<Alert show-icon>
							友情提示
							<Icon type="ios-lightbulb-outline" slot="icon"></Icon>
							<template slot="desc">环境管理是用户能自主的对新的环境进行管理，包括能够添加远程的容器管理，比如aws、ec2等等，要求相关的环境安装机器能够网络互通，保证安装期间不会因为网络相关问题导致安装不成功。. </template>
					</Alert>

          <div class="env-info">
            <ul class="env-line">
              <li>
                <span>环境名</span><span>{{running.environment.envName}}</span>
              </li>
              <li>
                <span>类型</span><span v-if="running.environment.deployType=='single'">单节点部署</span><span v-else>集群部署</span>
              </li>
              <li>
                <span>创建人</span><span>{{running.environment.owner}}</span>
              </li>
              <li>
                <span>部署时间</span><span>{{running.environment.createTime}}</span>
              </li>
            </ul>
          </div>
				</Card>
			</Col>
		</Row>
    <Row  :gutter="5" style="margin-top:10px;">
      <Col span="10">
        <Card>
          <p slot="title">管理服务</p>
          <ul class="service-list">
            <li v-for="master in masters">
              <span class="info-title">{{master.name}}</span>
              <span class="info-col">
                <Tag color="green" v-if="master.health == 'Healthy'">正常</Tag>
                <Tag v-else color="yellow">{{master.message}}</Tag>
              </span>
              <span class="info-col">
                <Dropdown>
                 <a href="javascript:void(0)">
                     管理
                     <Icon type="arrow-down-b"></Icon>
                 </a>
                 <DropdownMenu slot="list">
                     <DropdownItem>停止服务</DropdownItem>
                     <DropdownItem>启动拉起</DropdownItem>
                     <DropdownItem>日志</DropdownItem>
                 </DropdownMenu>
             </Dropdown>
              </span>
            </li>
          </ul>
        </Card>
        <Card>
          <p slot="title">计算服务</p>
          <ul class="service-list">
            <li v-for="node in nodes">
              <span class="info-title">{{node.name}}</span>
              <span class="info-col">{{node.age}}</span>
              <span class="info-col">
                <Tag color="green" v-if="node.health == 'Ready'">正常</Tag>
                <Tag v-else color="yellow">{{master.message}}</Tag>
              </span>
              <span class="info-col">
                <Dropdown>
                 <a href="javascript:void(0)">
                     管理
                     <Icon type="arrow-down-b"></Icon>
                 </a>
                 <DropdownMenu slot="list">
                     <DropdownItem>摘除</DropdownItem>
                     <DropdownItem>日志</DropdownItem>
                 </DropdownMenu>
             </Dropdown>
              </span>
            </li>
          </ul>
        </Card>
      </Col>
      <Col span="14" >
        <Card>

        </Card>
      </Col>
    </Row>
    <Modal v-model="showAddModal" title="增加新节点" width="600" :loading="loading"
       @on-ok="handleSubmit('hostItem')"
       @on-cancel="handleReset('hostItem')">
       <Form ref="hostItem" :model="hostItem" :label-width="80">
           <FormItem label="主机IP">
             <Select v-model="hostItem.hostIp" style="width:200px">
                 <Option v-for="item in ips" :value="item.hostId" :key="item.hostId">{{ item.hostIp }}</Option>
             </Select>
           </FormItem>
           <FormItem label="类型">
             <Select v-model="hostItem.type" style="width:200px">
                 <Option v-for="tt in types" :value="tt.value" :key="tt.value">{{ tt.label }}</Option>
             </Select>
           </FormItem>
       </Form>
   </Modal>
  </div>
</template>
<script>
  export default {
    name:'EnvironmentInfo',
    mounted(){
      this.queryEnvinfo();
      this.queryIps();
    },
    computed:{
      nodes(){
        if(!this.running['environment_desc']){
          return []
        }
        let nodeStatus = this.running.environment_desc['nodestatus'];
        if(nodeStatus == undefined){
          return [];
        }
        let nodes = [];
        for(let key in nodeStatus){
          nodes.push({
            name:key,health:nodeStatus[key]['STATUS'],age:nodeStatus[key]['AGE']
          })
        }
        return nodes;
      },
      masters(){

        if(!this.running['environment_desc']){
          return []
        }
        let componentStatus = this.running['environment_desc']['componentstatus'];
        if(componentStatus == undefined){
          return []
        }
        let masters =  [];
        for(let key in componentStatus){
          masters.push({
            name:key,health:componentStatus[key]['STATUS'],message:componentStatus[key]['MESSAGE']
          });
        }
        return masters;
      }
    },
    methods:{
      queryIps(){
        this.$http.get('/api/environment/host_available/'+this.envId).then((response)=>{
          this.ips = response.data
        })
      },
      invokeAddNode(){
        setTimeout(() => {
            this.loading = false;
            this.$nextTick(() => {
                this.loading = true;
            });
        }, 1000);
        let data = {
          type:this.hostItem.type,ips:[this.hostItem.hostIp]
        }
        this.$http.post('/api/environment/node/'+this.envId,data).then((response)=>{
          this.$Notice.success({
                  title: '添加节点',
                  desc:'节点'+this.hostItem.hostIp+'已经添加成功. '
              });
          this.showAddModal = false;
          this.queryEnvinfo();
        });
      },
      handleReset(formName){
        this.$refs[formName].resetFields();
      },
      handleSubmit(formName){
        this.$Modal.confirm({
             title: '添加主机',
             content: '<p>确定要添加主机'+this.hostItem.hostIp+'</p>',
             onOk: () => {
               this.invokeAddNode();
             }
         });
      },
      queryEnvinfo(){
        this.$http.get('/api/environment/info/'+this.envId).then((response)=>{
          this.running = response.data;
        });
      },
      envHandler(name){
        if(name == 'addNode'){
          this.showAddModal = true;
        }
      }
    },
    data(){
      return {
        types:[
          {label:'控制节点',value:'master'},
          {label:'计算节点',value:'node'},
          {label:'存储节点',value:'store'}
        ],
        hostItem:{
          hostIp:'',type:'node'
        },
        loading: true,
        ips:[],
        showAddModal:false,
        envId:this.$route.params.id,
        running:{
          environment:{status:''}
        }
      }
    }
  }
</script>
