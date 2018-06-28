package com.jd.jdos.sunshine.form;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.jd.jdos.sunshine.domain.Envs;

/**
 * Created by zhangkai12 on 2018/6/16.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public class EnvironmentRunning {
    private Envs environment;
    private String envId;
    @JsonProperty("environment_progress")
    private Double environmentProgress;
    @JsonProperty("environment_status")
    private String environmentStatus;
    @JsonProperty("environment_result")
    private String environmentResult;
    @JsonProperty("environment_time")
    private String environmentTime;
    @JsonProperty("environment_desc")
    private EnvironmentNodeDesc environmentNodeDesc;

    public EnvironmentRunning() {
    }

    public String getEnvId() {
        return envId;
    }

    public void setEnvId(String envId) {
        this.envId = envId;
    }

    public String getEnvironmentStatus() {
        return environmentStatus;
    }

    public void setEnvironmentStatus(String environmentStatus) {
        this.environmentStatus = environmentStatus;
    }

    public String getEnvironmentResult() {
        return environmentResult;
    }

    public void setEnvironmentResult(String environmentResult) {
        this.environmentResult = environmentResult;
    }

    public String getEnvironmentTime() {
        return environmentTime;
    }

    public void setEnvironmentTime(String environmentTime) {
        this.environmentTime = environmentTime;
    }

    public Double getEnvironmentProgress() {
        return environmentProgress;
    }

    public void setEnvironmentProgress(Double environmentProgress) {
        this.environmentProgress = environmentProgress;
    }

    public EnvironmentNodeDesc getEnvironmentNodeDesc() {
        return environmentNodeDesc;
    }

    public void setEnvironmentNodeDesc(EnvironmentNodeDesc environmentNodeDesc) {
        this.environmentNodeDesc = environmentNodeDesc;
    }

    public Envs getEnvironment() {
        return environment;
    }

    public void setEnvironment(Envs environment) {
        this.environment = environment;
    }
}
