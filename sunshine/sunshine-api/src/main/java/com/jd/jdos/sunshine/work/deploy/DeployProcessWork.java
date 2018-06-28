package com.jd.jdos.sunshine.work.deploy;

import com.google.common.eventbus.EventBus;
import com.jd.jdos.sunshine.common.Constants;
import com.jd.jdos.sunshine.domain.Envs;
import com.jd.jdos.sunshine.service.EnvironmentService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.List;

/**
 * Created by zhangkai12 on 2018/6/13.
 */
@Component
public class DeployProcessWork{
    Logger logger = LoggerFactory.getLogger(DeployProcessWork.class) ;
    @Autowired
    EnvironmentService environmentService;
    @Autowired
    EventBus eventBus;
    /**
     * 每分钟检查是否有未完成部署的环境
     */
    @Scheduled(cron = "0 0/30 * * * ?")
    public void dispatchDeploys(){
        //查询安装中的环境
        List<Envs> environments = environmentService.queryEnvironments(Constants.EnvStatus.installing);
        if(environments == null || environments.size() == 0){
            return;
        }
        //推送环境信息
        for(Envs environment:environments){
            eventBus.post(environment);
        }

    }

}
