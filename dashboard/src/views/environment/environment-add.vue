<style scoped>
	.step-show{
		display:block;
	}
	.step-hide{
		display: none;
	}
</style>
<template>
	<div id="addEnvironment">
		<Row>
			<Col span="24">
				<Card>
					<div style="margin-bottom:10px;">
						<span style="font-size:20px;font-weight:bold;">环境部署</span>
					</div>
					<Alert show-icon>
							友情提示
							<Icon type="ios-lightbulb-outline" slot="icon"></Icon>
							<template slot="desc">环境管理是用户能自主的对新的环境进行管理，包括能够添加远程的容器管理，比如aws、ec2等等，要求相关的环境安装机器能够网络互通，保证安装期间不会因为网络相关问题导致安装不成功. </template>
					</Alert>
					<Steps :current="current" style="margin-top:25px;">
				        <Step title="部署环境类型"></Step>
				        <Step title="环境信息"></Step>
				        <Step title="部署进度"></Step>
				  </Steps>
					<EnvironmentAddFirst v-model="current" @on-installing="queryDeployInstalling"></EnvironmentAddFirst>
					<EnvironmentAddLast :installing="envInstalling"  v-show="current == 2"></EnvironmentAddLast>
				</Card>
			</Col>
		</Row>
	</div>
</template>
<script>
	import EnvironmentAddFirst from './environment-add-first.vue'
	import EnvironmentAddLast from './environment-add-last.vue'
	export default {
		name:'environment_add',
		components:{
			EnvironmentAddFirst,EnvironmentAddLast
		},
		mounted(){
			this.queryCurrent();
		},
		data(){
			return {
				current:-1,
				envInstalling:{installProgress:0,logs:[]}
			};
		},
		methods:{
			queryDeployInstalling(taskId){
				this.$http.get('/api/environment/deploy/'+taskId).then((response)=>{
					this.envInstalling.installProcess = parseFloat(response.data.installProcess).toFixed(1);
					this.envInstalling.logs.push({
						execTime:response.data.execTime,
						desc:response.data.desc
					});
					if(this.envInstalling.installProcess<100 && document.getElementById('addEnvironment')){
						setTimeout(()=>{
							this.queryDeployInstalling(taskId);
						},1000);
					}else{
						setTimeout(()=>{
								this.$router.push({path:'/environment/index'})
						},3000);

					}

				})
			},
			queryCurrent(){
				if(this.$route.path.indexOf('/environment/install')>=0){
					this.current = 2;
					let taskId = this.$route.params.taskId;
					this.queryDeployInstalling(taskId);

				}else{
					this.current = 0;
				}
			}
		}
	}
</script>
