package com.jd.jdos.sunshine.work.deploy;

import com.google.common.eventbus.Subscribe;
import com.jd.jdos.sunshine.common.Constants;
import com.jd.jdos.sunshine.domain.Envs;
import com.jd.jdos.sunshine.form.EnvironmentProcess;
import com.jd.jdos.sunshine.service.EnvironmentService;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * 自动处理
 * Created by zhangkai12 on 2018/6/13.
 */
@Component
public class DeployProcessListener {
    Logger logger = LoggerFactory.getLogger(DeployProcessListener.class) ;
    @Autowired
    EnvironmentService environmentService;
    @Subscribe
    public void listener(Envs event) {
        logger.debug(String.format("[check deploy]check deploy environment [%s] status",event.getEnvName()));
        EnvironmentProcess result =  environmentService.queryDeploy(event.getEnvId());
        if(result.getResult() == null){
            event.setDeployProcess(String.valueOf(result.getInstallProcess()));
            environmentService.updateEnvironment(event);
        }else if(result.getResult() == true){
            event.setStatus(Constants.EnvStatus.running.name());
            event.setDeployProcess(String.valueOf(result.getInstallProcess()));
            environmentService.updateEnvironment(event);
        }else{
            event.setStatus(Constants.EnvStatus.error.name());
            event.setDeployProcess(String.valueOf(result.getInstallProcess()));
            environmentService.updateEnvironment(event);
        }
    }
}
