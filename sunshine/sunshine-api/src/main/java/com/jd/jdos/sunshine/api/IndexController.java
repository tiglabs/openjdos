package com.jd.jdos.sunshine.api;

import com.baomidou.mybatisplus.mapper.Condition;
import com.baomidou.mybatisplus.mapper.EntityWrapper;
import com.jd.jdos.sunshine.domain.ResponseBean;
import com.jd.jdos.sunshine.domain.User;
import com.jd.jdos.sunshine.service.UserManagerService;
import com.jd.jdos.sunshine.service.UserService;
import com.jd.jdos.sunshine.util.JWTUtil;
import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authz.UnauthorizedException;
import org.apache.shiro.authz.annotation.RequiresAuthentication;
import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.apache.shiro.authz.annotation.RequiresUser;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;

/**
 *
 * @author m8cool
 * @date 2018/4/26
 */
@RestController
public class IndexController {

    Logger logger = LoggerFactory.getLogger(IndexController.class) ;

    @Autowired
    UserManagerService userManagerService ;

    @RequestMapping("/health")
    public String health(){
        logger.info("log4j2 test for {}", "m8cool");
        logger.warn("log4j2 test for {} warn", "m8cool");
        logger.error("log4j2 test for {} error", "m8cool");
        return "ok" ;
    }

    @RequiresPermissions("project:*")
    @RequestMapping("project")
    public String project(){
        return "project permission project:*" ;
    }

    @RequiresPermissions("project:view")
    @RequestMapping("project2")
    public String project2(){
        return "user permission project:view" ;
    }

    @RequestMapping(path = "/401")
    @ResponseStatus(HttpStatus.UNAUTHORIZED)
    public ResponseBean unauthorized() {
        return new ResponseBean(401, "Unauthorized", null);
    }



}
