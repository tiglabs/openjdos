<template>
  <div>
		<Row>
			<Col span="24">
				<Card>
						<div style="margin-bottom:10px;">
							<span style="font-size:20px;font-weight:bold;">主机管理</span>
							<Button type="primary" icon="plus" @click="openModel">增加新主机</Button>
						</div>
		          <Alert show-icon>
					        友情提示
					        <Icon type="ios-lightbulb-outline" slot="icon"></Icon>
					        <template slot="desc">主机是使用OpenJDOS的进行资源运行的载体,具体可以是物理机、虚拟机或者是云主机,用户可以根据自身业务需求进行按需搭建,具体请看<a>环境部署</a>帮助手册. </template>
					    </Alert>
					    <div >
					    	<Table :data="hostList" :columns="hostCols" stripe></Table>
					    </div>
		        </Card>
			</Col>
		</Row>
    <Modal v-model="modal1" title="增加新主机" width="600" :loading="loading"
       @on-ok="handleSubmit('hostItem')"
       @on-cancel="handleReset('hostItem')">
       <Form ref="hostItem" :model="hostItem" :label-width="80">
           <FormItem label="主机IP">
               	<IpInput v-model="hostItem.hostIp"></IpInput>
           </FormItem>
           <FormItem label="主机类型">
               <Select v-model="hostItem.hostType">
                   <Option value="local">物理机</Option>
                   <Option value="aws">AWS</Option>
               </Select>
           </FormItem>
       </Form>
   </Modal>
	</div>
</template>
<script>
import IpInput from '@/views/form/inputs/ip-inputs.vue'
import util from '@/libs/util.js'
  export default {
    name:'HostIndex',
    components:{IpInput},
    mounted(){
      this.queryHosts();
    },
    methods:{
      openModel(){
        this.hostItem.hostIp='127.0.0.1';
        this.hostItem.hostType='local';
        this.modal1 = true;
      },
      handleSubmit (name) {
        setTimeout(() => {
            this.loading = false;
            this.$nextTick(() => {
                this.loading = true;
            });
        }, 1000);
        if(util.checkIp(this.hostItem.hostIp)){
          let ip = this.hostItem.hostIp;
          this.$http.post('/api/environment/host',this.hostItem).then((response)=>{
            this.$Notice.success({
                    title: '添加主机',
                    desc:'主机'+ip+'已经添加成功. '
                });
            this.modal1 = false;
            this.queryHosts();
          });
        }else{
          this.$Message.error('IP地址不合法');
        }
      },
      handleReset (name) {
          this.$refs[name].resetFields();
      },
      queryHosts(){
        this.$http.get('/api/environment/host').then((response)=>{
          this.hostList = response.data;
        });
      },
      deleteHost(row){
        this.$Modal.confirm({
                   title: '删除主机',
                   content: '<p>确定要删除主机'+row.hostIp+'</p>',
                   onOk: () => {
                     this.$http.delete('/api/environment/host/'+row.hostId).then((response)=>{
                       this.$Notice.success({
                               title: '删除主机',
                               desc:'主机'+row.hostIp+'已经删除成功. '
                           });
                       this.queryHosts();
                     })
                   }
               });
      }
    },
    data(){
      return {
        modal1:false,
        loading: true,
        hostList:[],
        hostCols:[
        {
          title:'主机IP',key:'hostIp'
        },{
          title:'主机类型',key:'hostType',render:(h,params)=>{
            let row = params.row;
            let Tag = 'Tag';
            if( row.hostType == 'local'){
              return (
                <Tag>物理机</Tag>
              );
            }else{
              return (
                <Tag>AWS</Tag>
              );
            }
          }
        },{
          title:'能否可用',key:'envId',render:(h,params)=>{
            let row = params.row;
              let Tag = 'Tag';
            if(row['envId'] == undefined || row['envId'] == null){
              return  (
                <Tag color="green">未使用</Tag>
              );
            }else{
              return (
                <Tag color="yellow">已使用</Tag>
              );
            }
          }
        },{
					title:'操作',key:'operate',render:(h,params)=>{
            let row = params.row;
            return h('Dropdown',{
              props:{
                trigger:'click'
              },
              style:{
                marginLeft:'5px'
              }
            },[
              h('a',{
                attrs:{
                  href:"javascript:void(0)"
                }
                },[h('span','管理'),h('Icon',{props:{type:'arrow-down-b'}})]
              ),
              h('DropdownMenu',{
                slot:'list'
              },[
                h('DropdownItem',[
                  h('span',{
                    on:{
                      click:()=>{
                        this.deleteHost(row)
                      }
                    }
                  },'删除')
                ])
              ])
            ]);
					}
				}],
        hostItem:{
          hostIp:'127.0.0.1',
          hostType:'local'
        }
      }
    }
  }
</script>
