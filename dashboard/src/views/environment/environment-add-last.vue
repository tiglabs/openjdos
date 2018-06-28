<template>
  <div>
    <Row style="padding:40px 0 0;">
      <Col span="24" style="text-align:center;">
        <i-circle :percent="installing.installProcess">
            <span class="demo-Circle-inner" style="font-size:24px">{{installing.installProcess}}%</span>
        </i-circle>
      </Col>
    </Row>
    <Row>
      <Col style="text-align:center;">
        <h4>安装进度</h4>
      </Col>
      <Col span="24">
        <EnvironmentTermial :logs="installing.logs"></EnvironmentTermial>
      </Col>
    </Row>
  </div>
</template>
<script>
import EnvironmentTermial from './environment-terminal.vue'
  export default {
    name:'EnvironmentAddLast',
    props:['installing'],
    components:{
			EnvironmentTermial
		},
    data(){
      return {
        installProgress:0,
        logs:[]
      }
    }
  }
</script>
