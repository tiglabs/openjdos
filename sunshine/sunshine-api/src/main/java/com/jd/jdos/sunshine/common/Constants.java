package com.jd.jdos.sunshine.common;

/**
 * Created by zhangkai12 on 2018/6/12.
 */
public class Constants {
    //默认的部署类型
    public static enum DeployType{
        single,cluster
    }


    //host支持的工作类型
    public static enum HostType{
        local,aws
    }

    /**
     * 环境状态
     */
    public static enum EnvStatus{
        installing,running,error
    }
}
