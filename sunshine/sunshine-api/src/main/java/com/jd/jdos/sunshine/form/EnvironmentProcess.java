package com.jd.jdos.sunshine.form;

import java.util.Date;

/**
 * Created by zhangkai12 on 2018/6/13.
 */
public class EnvironmentProcess {
    private String envId;
    private Double installProcess;
    private String desc;

    private String execTime;
    private String status;
    private Boolean result;
    public String getEnvId() {
        return envId;
    }

    public void setEnvId(String envId) {
        this.envId = envId;
    }

    public Double getInstallProcess() {
        return installProcess;
    }

    public void setInstallProcess(Double installProcess) {
        this.installProcess = installProcess;
    }

    public String getDesc() {
        return desc;
    }

    public void setDesc(String desc) {
        this.desc = desc;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public Boolean getResult() {
        return result;
    }

    public void setResult(Boolean result) {
        this.result = result;
    }

    public String getExecTime() {
        return execTime;
    }

    public void setExecTime(String execTime) {
        this.execTime = execTime;
    }
}
