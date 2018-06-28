package com.jd.jdos.sunshine.service.impl;

import com.baomidou.mybatisplus.mapper.Condition;
import com.baomidou.mybatisplus.mapper.Wrapper;
import com.baomidou.mybatisplus.plugins.Page;
import com.jd.jdos.sunshine.domain.*;
import com.jd.jdos.sunshine.service.*;
import com.jd.jdos.sunshine.util.UUIDUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Created by m8cool on 2018/6/22.
 */
@Service
public class UserManagerServiceImpl implements UserManagerService {

    @Autowired
    UserService userService ;

    @Autowired
    UserRoleRefService userRoleRefService ;

    @Autowired
    RoleService roleService;

    @Autowired
    PermissionService permissionService ;

    @Autowired
    RolePermissionRefService rolePermissionRefService ;

    public User findUserByUsername(String username){
        return userService.selectOne(Condition.create().eq("name",username)) ;
    }

    public List<Role> findRoles(String username){

        User user = findUserByUsername(username) ;

        if(user == null){
            return null ;
        }

        String userUuid = user.getUuid() ;
        List<UserRoleRef> userRoleRefList = findUserRoleRefByUserUuid(userUuid) ;

        if(CollectionUtils.isEmpty(userRoleRefList)){
            return null ;
        }

        List<String> roleUuidList = new ArrayList<String>() ;
        for(UserRoleRef ref: userRoleRefList){
            roleUuidList.add(ref.getRoleUuid()) ;
        }

        return findRoles(roleUuidList) ;
    }

    public List<UserRoleRef> findUserRoleRefByUserUuid(String userUuid){

        Wrapper wrapper = Condition.create().eq("userUuid",userUuid) ;

        return userRoleRefService.selectList(wrapper) ;
    }

    public List<Role> findRoles(List<String> roleUuidList){
        Wrapper wrapper = Condition.create().in("uuid",roleUuidList) ;


        List<Role> roleList = roleService.selectList(wrapper) ;

        if(CollectionUtils.isEmpty(roleList)){
            return null ;
        }

        return roleList;
    }

    public Set<String> findRolesByUsername(String username){

        List<Role> roleList = findRoles(username) ;

        if(CollectionUtils.isEmpty(roleList)){
            return null ;
        }

        Set<String> set = new HashSet<String>() ;
        for (Role r : roleList) {
            set.add(r.getRole()) ;
        }
        return set ;
    }



    public Set<String> findPermissionByUsername(String username){
        List<Permission> permissionList = findPermissions(username) ;

        if(CollectionUtils.isEmpty(permissionList)){
            return null ;
        }

        Set<String> set = new HashSet<String>() ;
        for (Permission p : permissionList) {
            set.add(p.getPermission()) ;
        }

        return set ;
    }

    public List<Permission> findPermissions(String username){

        List<Role> roleList = findRoles(username) ;

        if(CollectionUtils.isEmpty(roleList)){
            return null ;
        }

        List<String> roleUuidList = new ArrayList<String>() ;

        for(Role role:roleList){
            roleUuidList.add(role.getUuid()) ;
        }

        List<RolePermissionRef> rolePermissionRefList = findRolePermissionRefByRoleUuid(roleUuidList) ;

        if(CollectionUtils.isEmpty(rolePermissionRefList)){
            return null ;
        }


        List<String> permissionUuidList = new ArrayList<String>() ;

        for(RolePermissionRef rolePermissionRef:rolePermissionRefList){
            permissionUuidList.add(rolePermissionRef.getPermissionUuid()) ;
        }

        return findPermissions(permissionUuidList) ;
    }

    /**
     * 根据roleUuid查询RolePermissionRef
     * @param roleUuidList
     * @return
     */
    public List<RolePermissionRef> findRolePermissionRefByRoleUuid(List<String> roleUuidList){
        Wrapper wrapper = Condition.create().in("roleUuid",roleUuidList) ;

        return rolePermissionRefService.selectList(wrapper) ;
    }

    /**
     * 根据permissionUuid查询权限
     * @param permissionUuidList
     * @return
     */
    public List<Permission> findPermissions(List<String> permissionUuidList){
        Wrapper wrapper = Condition.create().in("uuid",permissionUuidList) ;

        return permissionService.selectList(wrapper) ;
    }

    @Override
    public Page<User> queryUserListByPage(Page<User> page) {

        return userService.selectPage(page);
    }

    @Override
    public boolean createUser(String username, String password) {
        User user = new User() ;
        user.setUuid(UUIDUtil.getUUID());
        user.setName(username);
        user.setPassword(password);
        user.setCreateDate(new java.util.Date());
        user.setLastOpDate(new java.util.Date());
        return userService.insert(user) ;
    }

    @Override
    public boolean deleteUserByUuids(List<String> uuids) {

        return userService.deleteBatchIds(uuids) ;
    }
}
