package com.jd.jdos.sunshine.form;


import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.Map;

/**
 * Created by zhangkai12 on 2018/6/16.
 */
public class EnvironmentNodeDesc {
    @JsonProperty("componentstatus")
    private Map componentStatus;
    @JsonProperty("nodestatus")
    private Map nodeStatus;

    public Map getComponentStatus() {
        return componentStatus;
    }

    public void setComponentStatus(Map componentStatus) {
        this.componentStatus = componentStatus;
    }

    public Map getNodeStatus() {
        return nodeStatus;
    }

    public void setNodeStatus(Map nodeStatus) {
        this.nodeStatus = nodeStatus;
    }
}
