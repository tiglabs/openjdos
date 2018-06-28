<style lang="less">
    @import '../../styles/common.less';
</style>

<template>
    <div>
        <Row>
            <Button type="primary" @click="queryUserList"><Icon type="refresh" size="14"></Icon></Button>
            <Button type="primary" @click="showCreateModal">创建</Button>
            <!--<Button type="error" @click="showDeleteModal">删除</Button>-->
        </Row>
        <Row class="margin-top-10 searchable-table-con1">
            <Table border stripe show-header  :data="tableData" :columns="tableColumns"></Table>
            <div style="margin: 10px;overflow: hidden">
                <div style="float: right;">
                    <Page :total="total" :current="current"></Page>
                </div>
            </div>
        </Row>


        <Modal v-model="createModal" @on-ok="submitForm" title="添加用户" :loading="loading">

            <Form ref="form" :model="form" :rules="rule" :label-width="80">
                <Form-item label="用户名" prop="name">
                    <Input type="text" v-model="form.name"></Input>
                </Form-item>
                <Form-item label="密码" prop="passwd">
                    <Input type="password" v-model="form.passwd"></Input>
                </Form-item>
            </Form>
        </Modal>

    </div>

</template>
<script>
    import Util from '@/libs/util.js'

    const deleteButton = (vm, h, currentRow, index) => {
        return h('Poptip', {
            props: {
                confirm: true,
                title: '您确定要删除这条数据吗?',
                transfer: true
            },
            on: {
                'on-ok': () => {
                    Util.ajax.post('/api/user/delete',{'uuids':[vm.tableData[index].uuid]}).then((response) => {
                        let data = response.data ;
                        if(data.code !== 'success'){
                            vm.$Message.error('删除用户失败') ;
                        }else{
                            vm.$Message.success('删除用户成功') ;
                            vm.queryUserList();
                        }
                    })
                }
            }
        }, [
            h('Button', {
                style: {
                    margin: '0 5px'
                },
                props: {
                    type: 'error',
                    placement: 'top'
                }
            }, '删除')
        ]);
    };

    export default {
        data () {
            return {
                tableData: [
                 ],
                tableColumns:[
                    {
                        type:'selection',
                        width:60
                    },
                    {   title:'UUID',
                        key:'uuid'
                    },
                    {
                        title: '用户名',
                        key: 'name'
                    },
                    {
                        title: '禁用',
                        key: 'locked',
                        render: (h, params) => {
                            const row = params.row;
                            const color = row.locked === 0 ? 'green' : 'red';
                            const text = row.locked === 0 ? '可用' : '禁用中';

                            return h('Tag', {
                                props: {
                                    type: 'dot',
                                    color: color
                                }
                            }, text);
                        }
                    },
                    {
                        title: '更新时间',
                        key: 'lastOpDate',
                    },
                    {
                        title: '创建时间',
                        key: 'createDate',
                    },
                    {
                        title:'操作',
                        render: (h, param) => {
                            let currentRowData = this.tableData[param.index];
                            let children = [];
                            //children.push(editButton(this, h, currentRowData, param.index));
                            children.push(deleteButton(this, h, currentRowData, param.index));

                            return h('div', children);
                        }
                    }
                ],
                createModal:false,
                loading:false,
                form:{
                    name:'',
                    passwd:'',
                },
                rule:{
                    name: [
                        { required: true, message: '姓名不能为空', trigger: 'blur' }
                    ],
                    passwd: [
                        { required: true, message: '密码不能为空', trigger: 'blur' },
                    ],
                },
                current:1,
                size:20,
                total:0
            }
        },
        methods:{
            showCreateModal(){
                this.createModal = true ;
                this.$refs['form'].resetFields();
            },
            createUser(){
                Util.ajax.post('/api/user/create',{'name':this.form.name,'password':this.form.passwd}).then((response) => {
                    let data = response.data ;
                    if(data.code !== 'success'){
                        this.$Message.error('创建用户失败') ;
                    }else{
                        this.$Message.success('创建用户成功') ;
                        this.createModal = false;
                        this.queryUserList();
                    }
                })
            },
            submitForm(){
                setTimeout(() => {
                    this.loading = false;
                    this.$nextTick(() => {
                        this.loading = true;
                    });
                }, 1000);

                var createUser = this.createUser;
                this.$refs['form'].validate((valid) => {
                    if (valid) {
                        createUser();
                    }else{
                        $Message.error('用户名或者密码不合法');
                    }
                });

            },
            queryUserList(){
                Util.ajax.post('/api/user/list/',{current:this.current,size:this.size}).then((response)=>{
                    let data = response.data ;
                    /*{code: "success", message: "", data: {…}}*/

                    if(data.code !== 'success'){
                        this.$Message.error('查询用户列表失败') ;
                        return ;
                    }

                    let result = data.data ;

                    this.tableData = result.records ;
                    this.total = result.total ;
                })
            }
        },
        computed: {
        },
        mounted(){
            this.queryUserList();
        }
    }
</script>
