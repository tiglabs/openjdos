<template>
  <div style="padding-bottom:10px;">
    <div style="border-bottom: 1px solid #e9e9e9;padding-bottom:6px;margin-bottom:6px;">
        <Checkbox
            :indeterminate="indeterminate"
            :value="checkAll"
            @click.prevent.native="handleCheckAll">全选</Checkbox>
    </div>
    <CheckboxGroup v-model="checkAllGroup" @on-change="checkAllGroupChange">
        <Checkbox v-for="ip in value" :label="ip"></Checkbox>
    </CheckboxGroup>
  </div>
</template>
<script>
  export default {
    name:'EnvironmentAddIp',
    props:['value'],
    methods:{
      noticeIps(){
        this.$emit('on-ip',this.checkAllGroup);
      },
      handleCheckAll () {
          if (this.indeterminate) {
              this.checkAll = false;
          } else {
              this.checkAll = !this.checkAll;
          }
          this.indeterminate = false;

          if (this.checkAll) {
              this.checkAllGroup = this.value;
          } else {
              this.checkAllGroup = [];
          }
          this.noticeIps();
      },
      checkAllGroupChange (data) {
          if (data.length === this.value.length) {
              this.indeterminate = false;
              this.checkAll = true;
          } else if (data.length > 0) {
              this.indeterminate = true;
              this.checkAll = false;
          } else {
              this.indeterminate = false;
              this.checkAll = false;
          }
          this.noticeIps();
      }
    },
    data(){
      return {
        ips:this.value,
        indeterminate: false,
        checkAll: false,
        checkAllGroup: [],
      }
    }
  }
</script>
