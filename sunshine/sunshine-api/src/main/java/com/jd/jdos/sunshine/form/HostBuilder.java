package com.jd.jdos.sunshine.form;

import com.jd.jdos.sunshine.common.Constants;
import com.jd.jdos.sunshine.common.Utils;
import com.jd.jdos.sunshine.domain.EnvsHost;
import com.jd.jdos.sunshine.exception.ParamException;
import org.apache.commons.lang3.StringUtils;

import java.util.Date;
import java.util.UUID;

/**
 * Created by zhangkai12 on 2018/6/14.
 */
public class HostBuilder {
    private String hostIp;
    private String hostType;

    public String getHostIp() {
        return hostIp;
    }

    public void setHostIp(String hostIp) {
        this.hostIp = hostIp;
    }

    public String getHostType() {
        return hostType;
    }

    public void setHostType(String hostType) {
        this.hostType = hostType;
    }

    public void valid(){
        if(!Utils.isIPv4Address(hostIp)){
            throw new ParamException("environment.deploy.host.error",new String[]{hostIp});
        }
        if(!StringUtils.equals(hostType, Constants.HostType.aws.name()) && !StringUtils.equals(hostType,Constants.HostType.local.name())){
            throw new ParamException("hosttype.not.exists",new String[]{hostType});
        }
    }

    public EnvsHost build(){
        EnvsHost environmentHost = new EnvsHost();
        environmentHost.setHostIp(this.hostIp);
        environmentHost.setHostType(this.hostType);
        environmentHost.setCreateTime(new Date());
        environmentHost.setHostId(UUID.randomUUID().toString());
        return environmentHost;
    }
}
