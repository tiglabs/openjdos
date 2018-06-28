<style lang="less">
    @import './login.less';
</style>

<template>
    <div class="login" @keydown.enter="handleSubmit">
        <div class="login-con">
            <Card :bordered="false">
                <p slot="title">
                    <Icon type="log-in"></Icon>
                    欢迎登录
                </p>
                <div class="form-con">
                    <Form ref="loginForm" :model="form" :rules="rules">
                        <FormItem prop="userName">
                            <Input v-model="form.userName" placeholder="请输入用户名">
                                <span slot="prepend">
                                    <Icon :size="16" type="person"></Icon>
                                </span>
                            </Input>
                        </FormItem>
                        <FormItem prop="password">
                            <Input type="password" v-model="form.password" placeholder="请输入密码">
                                <span slot="prepend">
                                    <Icon :size="14" type="locked"></Icon>
                                </span>
                            </Input>
                        </FormItem>
                        <FormItem>
                            <Button @click="handleSubmit" type="primary" long>登录</Button>
                        </FormItem>
                    </Form>
                    <p class="login-tip">输入任意用户名和密码即可</p>
                </div>
            </Card>
        </div>
    </div>
</template>

<script>
import Cookies from 'js-cookie'
import Util from '@/libs/util.js'
export default {
    data () {
        return {
            form: {
                userName: 'user',
                password: 'user'
            },
            rules: {
                userName: [
                    { required: true, message: '账号不能为空', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '密码不能为空', trigger: 'blur' }
                ]
            }
        };
    },
    methods: {
        handleSubmit () {
            this.$refs.loginForm.validate((valid) => {
                if (valid) {
                    Util.ajax.post("/api/user/login",
                            {'name':this.form.userName,'password':this.form.password}
                    ).then((response)=> {

                        let data = response.data ;

                        if(data.code !== "success"){
                            this.$Message.error('登录失败:' + data.message);
                            return ;
                        }

                        let authorization = data.data ;


                        Util.ajax.defaults.headers.common['Authorization'] = authorization;

                        Cookies.set('user', this.form.userName, {expires:0.125});
                        Cookies.set('password', this.form.password,{expires:0.125});
                        Cookies.set('authorization',authorization,{expires:0.125}) ;

                        this.$Message.success('登录成功');

                        this.$store.commit('setAvator', 'https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=3448484253,3685836170&fm=27&gp=0.jpg');
                        if (this.form.userName === 'iview_admin') {
                            Cookies.set('access', 0);
                        } else {
                            Cookies.set('access', 1);
                        }

                        setTimeout(()=>{
                            this.$router.push({
                                name: 'home_index'
                            });
                        },1000);

                    }).catch((error) => {
                        this.$Message.error('登录失败');
                    });
                }
            });
        }
    }
};
</script>

<style>

</style>
