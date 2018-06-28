package com.jd.jdos.sunshine.api;


import com.baomidou.mybatisplus.plugins.Page;
import com.jd.jdos.sunshine.domain.*;
import com.jd.jdos.sunshine.service.UserManagerService;
import com.jd.jdos.sunshine.util.JWTUtil;
import org.apache.shiro.authc.UnknownAccountException;
import org.apache.shiro.authz.UnauthorizedException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;

/**
 * <p>
 *  前端控制器
 * </p>
 *
 * @author m8cool
 * @since 2018-06-22
 */
@RestController
@RequestMapping("/api/user")
public class UserController extends BaseController {

    @Autowired
    UserManagerService userManagerService ;

    @RequestMapping("/login")
    @CrossOrigin
    public ApiResponse login(@RequestBody User userRequest){

        User user = userManagerService.findUserByUsername(userRequest.getName()) ;

        if(user == null){
            return failure("login failed") ;
        }

        if (user.getPassword().equals(userRequest.getPassword())) {
            return success(JWTUtil.sign(user.getName(), user.getPassword()));
        } else {
            throw new UnauthorizedException();
        }
    }

    @RequestMapping("list")
    public ApiResponse queryUserListByPage(@Valid @RequestBody PageVo pageVo){
        Page<User> page = new Page<>(pageVo.getCurrent(),pageVo.getSize()) ;

        userManagerService.queryUserListByPage(page) ;

        return success(page) ;
    }

    @RequestMapping("create")
    public ApiResponse createUser(@Valid @RequestBody UserCreateRequest userCreateRequest){

        boolean success = userManagerService.createUser(userCreateRequest.getName(), userCreateRequest.getPassword()) ;
        return success();
    }

    @RequestMapping("delete")
    public ApiResponse deleteUser(@Valid @RequestBody UserDeleteRequest request){

        boolean success = userManagerService.deleteUserByUuids(request.getUuids()) ;

        if(success){
            return success() ;
        }else{
            return failure() ;
        }
    }
}

