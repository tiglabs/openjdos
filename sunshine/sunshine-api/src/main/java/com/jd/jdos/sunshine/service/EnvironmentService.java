package com.jd.jdos.sunshine.service;

import com.baomidou.mybatisplus.mapper.Condition;
import com.baomidou.mybatisplus.mapper.Wrapper;
import com.jd.jdos.sunshine.common.Constants;
import com.jd.jdos.sunshine.common.HttpUtils;
import com.jd.jdos.sunshine.common.Utils;
import com.jd.jdos.sunshine.dao.EnvsHostMapper;
import com.jd.jdos.sunshine.dao.EnvsMapper;
import com.jd.jdos.sunshine.domain.Envs;
import com.jd.jdos.sunshine.domain.EnvsHost;
import com.jd.jdos.sunshine.exception.ApiRunningException;
import com.jd.jdos.sunshine.exception.DeployEnvironmentException;
import com.jd.jdos.sunshine.form.EnvironmentBuilder;
import com.jd.jdos.sunshine.form.EnvironmentProcess;
import com.jd.jdos.sunshine.form.EnvironmentRunning;
import com.jd.jdos.sunshine.form.HostBuilder;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Isolation;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.util.*;

/**
 * 环境控制服务
 * Created by zhangkai12 on 2018/6/11.
 */
@Service
public class EnvironmentService {
    Logger logger = LoggerFactory.getLogger(EnvironmentService.class) ;

    @Autowired
    EnvsMapper environmentMapper;

    @Autowired
    EnvsHostMapper environmentHostMapper;
    @Value("${deploy.url}")
    String deployUrl;
    @Value("${deploy.certificate}")
    String certificatePath;

    /**
     * 查询所有主机
     * @return
     */
    public List<EnvsHost> queryHosts(){
        Wrapper<EnvsHost> wrapper = Condition.empty();
        return this.environmentHostMapper.selectList(wrapper);
    }

    /**
     * 添加主机
     * @param builder
     */
    public void addHost(HostBuilder builder){
        EnvsHost environmentHost = builder.build();
        this.environmentHostMapper.insert(environmentHost);
    }

    /**
     * 查询主机
     * @param hostId
     * @return
     */
    public EnvsHost queryEnvironmentHost(String hostId){
        Wrapper<EnvsHost> wrapper = Condition.create().eq("host_id",hostId);
        List<EnvsHost> environmentHosts = this.environmentHostMapper.selectList(wrapper);
        return environmentHosts == null||environmentHosts.size() == 0?null:environmentHosts.get(0);
    }

    /**
     * 删除对应的主机
     * @param hostId
     */
    public void deleteHost(String hostId){
        EnvsHost environmentHost = queryEnvironmentHost(hostId);
        if(environmentHost == null){
            throw new DeployEnvironmentException("host.not.exist",null);
        }
        this.environmentHostMapper.deleteById(environmentHost.getId());
    }

    /**
     * 查询所有环境
     * @return
     */
    public List<Envs> queryEnvironments(){
        return this.environmentMapper.selectList(Condition.empty());
    }

    /**
     * 更新环境信息
     * @param environment
     */
    public void updateEnvironment(Envs environment){
        this.environmentMapper.updateById(environment);
    }


    /**
     * 根据环境状态查询对应的环境
     * @param status
     * @return
     */
    public List<Envs> queryEnvironments(Constants.EnvStatus status){
        Wrapper<Envs> wrapper = Condition.create().eq("status",status);
        return this.environmentMapper.selectList(wrapper);
    }

    /**
     * 调用后台接口查询服务的实际状态数据
     * @param envId
     * @return
     */
    public EnvironmentProcess queryDeploy(String envId){
        try {
            String result = HttpUtils.instance.get(deployUrl+"/environments/"+envId+"/1");
            Map json = Utils.json2Obj(result,Map.class);
            EnvironmentProcess environmentProcess = new EnvironmentProcess();
            environmentProcess.setEnvId(envId);
            environmentProcess.setStatus((String)json.get("environment_status"));
            environmentProcess.setDesc((String)json.get("environment_desc"));
            environmentProcess.setInstallProcess(json.get("environment_progress") == null?0.00:(Double)json.get("environment_progress"));
            environmentProcess.setExecTime((String)json.get("environment_time"));
            if(json.get("environment_result") != null){
                environmentProcess.setResult((Boolean)json.get("environment_result"));
            }
            if(environmentProcess.getInstallProcess() == 100.0){
                Envs environment = this.queryEnvironment(envId);
                environment.setDeployProcess("100.0");
                environment.setStatus(Constants.EnvStatus.running.name());
                this.updateEnvironment(environment);
            }

            return environmentProcess;
        } catch (Exception e) {
            logger.error("[deploy check]fail to query environment env id is  +"+envId,e);
            throw new DeployEnvironmentException("environment.deploy.query.error",new String[]{e.getMessage()});
        }
    }

    public Envs queryEnvironment(String envId){
        Wrapper<Envs> wrapper = Condition.create().eq("env_id",envId);
        List<Envs> environments = this.environmentMapper.selectList(wrapper);
        return environments == null || environments.size() == 0?null:environments.get(0);
    }

    public EnvironmentRunning queryEnvInfo(String envId){
        Envs environment = this.queryEnvironment(envId);
        if(environment == null){
            throw new DeployEnvironmentException("environment.no.exists",new String[]{envId});
        }
        try {
            String result = HttpUtils.instance.get(deployUrl+"/environments/"+envId+"/2");
            EnvironmentRunning environmentRunning = Utils.json2Obj(result,EnvironmentRunning.class);
            environmentRunning.setEnvironment(environment);
            return environmentRunning;
        } catch (IOException e) {
            logger.error("[deploy check]fail to check environment status env id is  +"+envId,e);
            throw new DeployEnvironmentException("environment.info.query.error",new String[]{"服务部署",e.getMessage()});
        }
    }

    /**
     * 部署新环境
     * @param builder
     */
    public Envs deployEnvironment(EnvironmentBuilder builder){
        logger.info(String.format("[deploy environment]start to deploy environment : %s,now check parameters",builder.getEnvName()));
        builder.valid();
        logger.info(String.format("[deploy environment]environment : %s allowed to deploy",builder.getEnvName()));
        saveEnvironment(builder);
        logger.info(String.format("[deploy environment]environment : %s start to deploy host",builder.getEnvName()));
        deploy(builder);
        return builder.getEnvironment();
    }

    private void deploy(EnvironmentBuilder builder){
        Map<String,Object> params = new HashMap<>();
        params.put("environment_type",1);
        params.put("environment_desc",builder.getEnvName());
        Map<String,Object> deployHosts = new HashMap<>();
        params.put("environment_params",deployHosts);
        List<String> handlerHosts = null;
        if(builder.getMasterHost() != null && builder.getMasterHost().size() > 0){
            handlerHosts = new ArrayList<>(builder.getMasterHost().size());
            for(String ip : builder.getMasterHost()){
                handlerHosts.add(ip);
                deployHosts.put("master-host-list",handlerHosts);
            }
        }
        if(builder.getNodeHost() != null && builder.getNodeHost().size() > 0){
            handlerHosts = new ArrayList<>(builder.getNodeHost().size());
            for(String ip : builder.getNodeHost()){
                handlerHosts.add(ip);
                deployHosts.put("node-host-list",handlerHosts);
            }
        }
        if(builder.getStoreHost() != null && builder.getStoreHost().size() > 0){
            handlerHosts = new ArrayList<>(builder.getStoreHost().size());
            for(String ip : builder.getStoreHost()){
                handlerHosts.add(ip);
                deployHosts.put("etcd-host-list",handlerHosts);
            }
        }
        deployHosts.put("certificate_path",certificatePath);

        logger.info(String.format("[deploy environment]environment : %s deploy environment [%s]",builder.getEnvName(), Utils.json(params)));
        Map response = null;
        try {
            String result = HttpUtils.instance.post(deployUrl + "/environments/" + builder.getEnvironment().getEnvId(), params);
            logger.info(String.format("[deploy environment]environment : %s deploy response is [%s]",builder.getEnvName(),result));
            response = Utils.json2Obj(result,Map.class);
        }catch(ApiRunningException ae){
            String[] aeParams = (String[])ae.getParams();
            String defaultMessage = aeParams[0];
            throw new DeployEnvironmentException(ae.getMessage(),new String[]{builder.getEnvName(),defaultMessage});
        }
        catch (IOException e) {
            throw new DeployEnvironmentException("environment.deploy.env.service.error",new String[]{builder.getEnvName(),e.getMessage()});
        }
        if(response == null){
            throw new DeployEnvironmentException("environment.deploy.env.service.blank",new String[]{builder.getEnvName()});
        }
        if(StringUtils.equals((String)response.get("environment_result"),"False")){
            throw new DeployEnvironmentException("environment.deploy.env.service.error",new String[]{builder.getEnvName(),(String)response.get("environment_desc")});
        }
    }




    /**
     * 保存环境部署信息至数据库
     * @param environmentBuilder
     */
    @Transactional(propagation = Propagation.REQUIRES_NEW,isolation = Isolation.READ_COMMITTED,rollbackFor = Exception.class)
    public void saveEnvironment(EnvironmentBuilder environmentBuilder){
        logger.info(String.format("[deploy environment]environment : %s save environment",environmentBuilder.getEnvName()));
        Integer updateSize = null;
        Integer resultSize = null;
        try{
            Envs environment = environmentBuilder.parseEnvironment();
            environmentMapper.insert(environment);
            List<String> ips = new ArrayList<>();
            if(environmentBuilder.getMasterHost()!= null && environmentBuilder.getMasterHost().size() > 0){
                ips.addAll(environmentBuilder.getMasterHost());
            }
            if(environmentBuilder.getNodeHost()!= null && environmentBuilder.getNodeHost().size() > 0){
                ips.addAll(environmentBuilder.getNodeHost());
            }
            if(environmentBuilder.getStoreHost()!= null && environmentBuilder.getStoreHost().size() > 0){
                ips.addAll(environmentBuilder.getStoreHost());
            }

            ips = Utils.removeDuplicate(ips);
            updateSize = ips.size();
            this.queryIdealHosts(ips);

            EnvsHost updateEnvironmentHost = new EnvsHost();
            updateEnvironmentHost.setEnvId(environment.getEnvId());
            Wrapper<EnvsHost> updateEnvironmentHostExample = Condition.create().in("host_ip",ips);
            resultSize = this.environmentHostMapper.update(updateEnvironmentHost,updateEnvironmentHostExample);
        }catch(DuplicateKeyException dke){
            logger.error("[deploy environment]environment :"+environmentBuilder.getEnvName()+" had been deploye before",dke);
            throw new DeployEnvironmentException("environment.deploy.env.exist",new String[]{environmentBuilder.getEnvName()});
        }
        if(updateSize != resultSize){
            throw new DeployEnvironmentException("environment.deploy.host.duplicate.use",new String[]{});
        }
    }

    /**
     * 查询对应的对应的
     * @param hostIps
     * @return
     */
    private List<EnvsHost> queryIdealHosts(List<String> hostIps){
        Wrapper<EnvsHost> updateEnvironmentHostExample = Condition.create().in("host_ip",hostIps);
        List<EnvsHost> hosts = this.environmentHostMapper.selectList(updateEnvironmentHostExample);
        for(EnvsHost host:hosts){
            if(StringUtils.isNotBlank(host.getEnvId())){
                throw new DeployEnvironmentException("deploy.host.busy",new String[]{host.getHostIp()});
            }
        }
        return hosts;
    }

}
