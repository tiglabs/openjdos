<template>
	<div>
		<Row>
			<Col span="24">
				<Card>
						<div style="margin-bottom:10px;">
							<span style="font-size:20px;font-weight:bold;">环境管理</span>
							<Button type="primary" icon="plus" @click="goDeploy">部署环境</Button>
						</div>
		          <Alert show-icon>
					        友情提示
					        <Icon type="ios-lightbulb-outline" slot="icon"></Icon>
					        <template slot="desc">环境是资源运行的边界，所有的资源必须包含在一个环境中，环境中的机器是用户自行准备对应的主机，然后由OpenJDOS自动的进行安装,具体请看<a>环境部署</a>帮助手册. </template>
					    </Alert>
					    <div >
					    	<Table :data="envsList" :columns="envsCols" stripe></Table>
					    </div>
		        </Card>
			</Col>
		</Row>
	</div>
</template>
<script>
	export default {
		name:"environment_index",
		mounted(){
			this.loadData();
		},
		data (){
			return {
				envsList:[],
				envsCols:[{
					title:'状态',key:'status',render:(h,params)=>{
						let row = params.row;
						let text = '';
						let color ='';
						switch(row.status){
							case 'running':
								text='运行中';
								color = 'green';
								break;
							case 'installing':
								text='部署中';
								color = 'blue';
								break;
							case 'error':
								text='异常';
								color='red';
								break;
							case 'deleting':
								text='删除中';
								color='yellow';
								break;
						}
						return h('Tag',{
							props: {
                                    type: 'dot',
                                    color: color
                                }
                            },text);
					}
				},{
					title:'环境标识',key:'envName'
				},{
					title:'部署类型',key:'deployType',render:(h,params)=>{
						let row = params.row;
						let text = row.deployType == 'single'?'单节点':'集群';
						return h('span',text);
					}
				},{
					title:'所属人',key:'owner'
				},{
					title:'创建时间',key:'createTime'
				},{
					title:'操作',key:'operate',render:(h,params)=>{
						let row = params.row;
						let taskId = row.envId;
						let subs = [
							h(
								'DropdownItem',[
									h('span',{
										on:{
											click:()=>{
												this.$router.push({path:'/environment/info/'+taskId})
											}
										}
									},'详情')
								]
							)

						];
						if(row.status == 'installing'){
							subs.push(
								h(
									'DropdownItem',[
										h('span',{
											on:{
												click:()=>{
													this.goInstalling(taskId)
												}
											}
										},'查询安装进度')
									]
								)
							)
						}
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
							},subs)
						]);
					}
				}]
			}
		},
		methods:{
			loadData(){
				this.$http.get('/api/environment').then((response)=>{
          this.envsList = response.data;
        });
			},goDeploy () {
          this.$router.push({path:'/environment/add'})
      },goInstalling(taskId){
				this.$router.push({path:'/environment/install/'+taskId})
			}
		}
	}
</script>
