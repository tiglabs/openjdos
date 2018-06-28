package com.jd.jdos.sunshine.form;

import com.jd.jdos.sunshine.common.Constants;
import com.jd.jdos.sunshine.common.Utils;
import com.jd.jdos.sunshine.domain.Envs;
import com.jd.jdos.sunshine.exception.ParamException;
import org.hibernate.validator.constraints.NotBlank;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.UUID;

/**
 * Created by zhangkai12 on 2018/6/12.
 */
public class EnvironmentBuilder {


    @Pattern(regexp = "^[a-zA-Z][a-zA-Z0-9_-]{3,64}$",message = "environment.deploy.envname.error")
    private String envName;
    @NotBlank(message = "environment.deploy.deployType.blank")
    private String deployType;
    @NotNull(message = "environment.deploy.masterHost.null")
    private List<String> masterHost;
    @NotNull(message = "environment.deploy.nodeHost.null")
    private List<String> nodeHost;
    private List<String> storeHost;
//    @NotBlank(message = "environment.deploy.user.blank")
//    private String userName;
//    @NotBlank(message = "environment.deploy.password.blank")
//    private String password;

    Envs environment;


    public Envs getEnvironment() {
        return environment;
    }

    public void setEnvironment(Envs environment) {
        this.environment = environment;
    }

    public String getEnvName() {
        return envName;
    }

    public void setEnvName(String envName) {
        this.envName = envName;
    }

    public String getDeployType() {
        return deployType;
    }

    public void setDeployType(String deployType) {
        this.deployType = deployType;
    }

    public List<String> getMasterHost() {
        return masterHost;
    }

    public void setMasterHost(List<String> masterHost) {
        this.masterHost = masterHost;
    }

    public List<String> getNodeHost() {
        return nodeHost;
    }

    public void setNodeHost(List<String> nodeHost) {
        this.nodeHost = nodeHost;
    }

    public List<String> getStoreHost() {
        return storeHost;
    }

    public void setStoreHost(List<String> storeHost) {
        this.storeHost = storeHost;
    }

//    public String getUserName() {
//        return userName;
//    }
//
//    public void setUserName(String userName) {
//        this.userName = userName;
//    }
//
//    public String getPassword() {
//        return password;
//    }
//
//    public void setPassword(String password) {
//        this.password = password;
//    }

    /**
     * 验证部署环境参数的合法性
     */
    public void valid(){
        if(!deployType.equals(Constants.DeployType.single.name()) && !deployType.equals(Constants.DeployType.cluster.name())){
            throw new ParamException("environment.deploy.deployType.error",null);
        }
    }

    /**
     * 转换环境对象
     * @return
     */
    public Envs parseEnvironment(){
        Envs environment = new Envs();
        String taskId = UUID.randomUUID().toString();
        environment.setEnvId(taskId);
        environment.setStatus(Constants.EnvStatus.installing.name());
        environment.setEnvName(this.envName);
        environment.setCreateTime(new Date());
        environment.setDeployType(this.deployType);
//        environment.setUserName(this.userName);
//        environment.setPassword(this.password);
        setEnvironment(environment);
        return environment;
    }

}
