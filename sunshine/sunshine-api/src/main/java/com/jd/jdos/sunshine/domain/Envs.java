package com.jd.jdos.sunshine.domain;

import com.baomidou.mybatisplus.enums.IdType;
import java.util.Date;
import com.baomidou.mybatisplus.annotations.TableId;
import java.io.Serializable;

/**
 * <p>
 * 环境部署表
 * </p>
 *
 * @author m8cool
 * @since 2018-06-26
 */
public class Envs implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * ID
     */
    @TableId(value = "id", type = IdType.AUTO)
    private Integer id;
    /**
     * 环境id
     */
    private String envId;
    /**
     * 环境名称
     */
    private String envName;
    /**
     * 环境描述
     */
    private String envDesc;
    /**
     * 部署类型
     */
    private String deployType;
    /**
     * 用户
     */
    private String owner;
    /**
     * 状态
     */
    private String status;
    /**
     * 创建时间
     */
    private Date createTime;
    private String userName;
    private String password;
    private String deployProcess;


    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getEnvId() {
        return envId;
    }

    public void setEnvId(String envId) {
        this.envId = envId;
    }

    public String getEnvName() {
        return envName;
    }

    public void setEnvName(String envName) {
        this.envName = envName;
    }

    public String getEnvDesc() {
        return envDesc;
    }

    public void setEnvDesc(String envDesc) {
        this.envDesc = envDesc;
    }

    public String getDeployType() {
        return deployType;
    }

    public void setDeployType(String deployType) {
        this.deployType = deployType;
    }

    public String getOwner() {
        return owner;
    }

    public void setOwner(String owner) {
        this.owner = owner;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public Date getCreateTime() {
        return createTime;
    }

    public void setCreateTime(Date createTime) {
        this.createTime = createTime;
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getDeployProcess() {
        return deployProcess;
    }

    public void setDeployProcess(String deployProcess) {
        this.deployProcess = deployProcess;
    }

    @Override
    public String toString() {
        return "Envs{" +
        ", id=" + id +
        ", envId=" + envId +
        ", envName=" + envName +
        ", envDesc=" + envDesc +
        ", deployType=" + deployType +
        ", owner=" + owner +
        ", status=" + status +
        ", createTime=" + createTime +
        ", userName=" + userName +
        ", password=" + password +
        ", deployProcess=" + deployProcess +
        "}";
    }
}
