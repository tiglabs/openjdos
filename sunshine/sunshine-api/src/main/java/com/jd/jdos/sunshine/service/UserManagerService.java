package com.jd.jdos.sunshine.service;

import com.baomidou.mybatisplus.plugins.Page;
import com.jd.jdos.sunshine.domain.User;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Set;

/**
 * Created by m8cool on 2018/6/22.
 */
public interface UserManagerService {


    User findUserByUsername(String name);

    Set<String> findRolesByUsername(String username);

    Set<String> findPermissionByUsername(String username);

    /**
     * 分页查询用户列表
     * @param page
     * @return
     */
    Page<User> queryUserListByPage(Page<User> page) ;


    /**
     * 创建用户
     */
    boolean createUser(String username,String password) ;

    boolean deleteUserByUuids(List<String> uuids);
}
