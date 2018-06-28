<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
.error-tip{
  color: #ed3f14;
  padding-top:8px;
}
</style>
<template>
  <div style="float:left;">
    <div class="ip-inputs">
      <Input v-model="value1" @on-blur="checkIp" :maxlength="maxlength" style="width: 60px"></Input>
        .
      <Input v-model="value2" @on-blur="checkIp" :maxlength="maxlength" style="width: 60px"></Input>
        .
      <Input v-model="value3" @on-blur="checkIp" :maxlength="maxlength" style="width: 60px"></Input>
        .
      <Input v-model="value4" @on-blur="checkIp" :maxlength="maxlength" style="width: 60px"></Input>
    </div>
    <div class="ip-inputs-error">
      &nbsp;
      <transition name="fade">
        <span class="error-tip" v-if="message !=''">{{message}}</span>
      </transition>
    </div>
  </div>
</template>
<script>
  export default {
    name:'IpInput',
    props:['value','label'],
    data(){
        return {
            message:'',maxlength:3,
            value1:this.initIpValue(0),
            value2:this.initIpValue(1),
            value3:this.initIpValue(2),
            value4:this.initIpValue(3),
        }
    },
    methods:{
      checkIp(){
        if(this.value1 == ''||this.value2==''||this.value3==''||this.value4==''){
          return;
        }
        let ip = this.value1+'.'+this.value2+'.'+this.value3+'.'+this.value4;
        if(!this.validIp(ip)){
          this.message = '输入的ip不是合规的ip';
        }else{
          this.message = '';
          this.$emit('input', ip);
        }
      },
      initIpValue(position){
        if(this.validIp(this.value)!=true){
          return '';
        }
        let ips = this.value.split('.');
        if(ips.length==4){
          return ips[position];
        }else{
          return '';
        }
      },
      validIp(ip){
        let reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/
        return reg.test(ip);
      }
    }
  }
</script>
