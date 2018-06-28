<style scoped>
.environment-terminal{
  margin:20px 0 ;
  height:300px;
  max-height: 400px;
  overflow-y: auto;
  background: #000;
  color:#fff;
}
.environment-terminal .ivu-row{
  padding:0 10px;
  margin:5px auto;
}
</style>
<template>
  <div class="environment-terminal">
    <Row v-for="log in logs">
      <Col span="24">
        [{{log.execTime}}]&nbsp;&gt;&nbsp;{{log.desc}}
      </Col>
    </Row>
  </div>
</template>
<script>
  export default {
    name:'EnvironmentTerminal',
    props:['logs']
  }
</script>
