package com.jd.jdos.sunshine.api;

import com.jd.jdos.sunshine.common.Utils;
import com.jd.jdos.sunshine.domain.ApiResponse;
import com.jd.jdos.sunshine.domain.Envs;
import com.jd.jdos.sunshine.domain.EnvsHost;
import com.jd.jdos.sunshine.form.EnvironmentBuilder;
import com.jd.jdos.sunshine.form.EnvironmentProcess;
import com.jd.jdos.sunshine.form.EnvironmentRunning;
import com.jd.jdos.sunshine.form.HostBuilder;
import com.jd.jdos.sunshine.service.EnvironmentService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

/**
 * 环境管理
 * Created by zhangkai12 on 2018/6/7.
 */
@Controller
@RequestMapping("/api/environment")
public class EnvironmentController extends BaseController{
    Logger logger = LoggerFactory.getLogger(EnvironmentController.class) ;

    @Autowired
    EnvironmentService environmentService;

    /**
     * 查询用户对应的所有环境
     * @return
     */
    @RequestMapping(value = {"","/"},method = RequestMethod.GET,produces = "application/json;charset=utf-8")
    @ResponseBody
    public List<Envs> queryEnvironments(){
        return this.environmentService.queryEnvironments();
    }

    /**
     * 部署新的环境
     * @param environmentBuilder
     * @return
     */
    @RequestMapping(value = {"","/"},method = RequestMethod.POST,produces = "application/json;charset=utf-8")
    @ResponseBody
    public Envs deployEnvironment(@Valid @RequestBody EnvironmentBuilder environmentBuilder){
        logger.info(Utils.json(environmentBuilder));
        return environmentService.deployEnvironment(environmentBuilder);
    }

    /**
     * 查询服务部署状态
     * @return
     */
    @RequestMapping(value = "/deploy/{envId}",method = RequestMethod.GET,produces = "application/json;charset=utf-8")
    @ResponseBody
    public EnvironmentProcess queryEnvironmentDeploy(@PathVariable("envId")String envId){
        return environmentService.queryDeploy(envId);
    }

    /**
     * 查询服务运行状态
     * @param envId
     * @return
     */
    @RequestMapping(value = "/info/{envId}",method = RequestMethod.GET,produces = "application/json;charset=utf-8")
    @ResponseBody
    public EnvironmentRunning queryEnvironmentInfo(@PathVariable("envId")String envId){
        return environmentService.queryEnvInfo(envId);
    }
    /**
     * 查询当前环境所有的主机信息
     * @return
     */
    @RequestMapping(value = "/host",method = RequestMethod.GET,produces = "application/json;charset=utf-8")
    @ResponseBody
    public List<EnvsHost> queryHosts(){
        return this.environmentService.queryHosts();
    }

    /**
     * 增加主机
     * @param builder
     * @return
     */
    @RequestMapping(value = "/host",method = RequestMethod.POST,produces = "application/json;charset=utf-8")
    @ResponseBody
    public ApiResponse addHost(@Valid @RequestBody HostBuilder builder){
        builder.valid();
        environmentService.addHost(builder);
        return build("host.add.success");
    }

    /**
     * 删除对应的主机
     * @return
     */
    @RequestMapping(value = "/host/{hostId}",method = RequestMethod.DELETE,produces = "application/json;charset=utf-8")
    @ResponseBody
    public ApiResponse deleteHost(@PathVariable("hostId")String hostId){
        this.environmentService.deleteHost(hostId);
        return build("host.delete.success",new String[]{hostId});
    }


}
