package com.jd.jdos.sunshine.shiro;

import com.jd.jdos.sunshine.domain.User;
import com.jd.jdos.sunshine.service.UserManagerService;
import com.jd.jdos.sunshine.service.UserService;
import com.jd.jdos.sunshine.util.JWTUtil;
import org.apache.shiro.authc.*;
import org.apache.shiro.authz.AuthorizationInfo;
import org.apache.shiro.authz.SimpleAuthorizationInfo;
import org.apache.shiro.realm.AuthorizingRealm;
import org.apache.shiro.subject.PrincipalCollection;
import org.apache.shiro.util.ByteSource;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Created by m8cool on 2018/6/13.
 */
public class SunshineRealm extends AuthorizingRealm {

    @Autowired
    UserManagerService userManagerService ;

    @Override
    public boolean supports(AuthenticationToken token) {
        return token instanceof JWTToken;
    }

    @Override
    protected AuthorizationInfo doGetAuthorizationInfo(PrincipalCollection principals) {

        String username = (String) principals.getPrimaryPrincipal();

        SimpleAuthorizationInfo authorizationInfo = new SimpleAuthorizationInfo();
        authorizationInfo.setRoles(userManagerService.findRolesByUsername(username));
        authorizationInfo.setStringPermissions(userManagerService.findPermissionByUsername(username));
        return authorizationInfo;
    }

    @Override
    protected AuthenticationInfo doGetAuthenticationInfo(AuthenticationToken auth) throws AuthenticationException {
        String token = (String) auth.getCredentials();

        String username = JWTUtil.getUsername(token);

        if (username == null) {
            throw new IncorrectCredentialsException();
        }

        User user = userManagerService.findUserByUsername(username);

        if(user == null) {
            //没找到帐号
            throw new UnknownAccountException();
        }

        if(Boolean.TRUE.equals(user.getLocked())) {
            //帐号锁定
            throw new LockedAccountException();
        }

        if (!JWTUtil.verify(token, username, user.getPassword())) {
            throw new ExpiredCredentialsException();
        }

        SimpleAuthenticationInfo authenticationInfo = new SimpleAuthenticationInfo(
                user.getName(),
                token,"sunshine_realm"
        );
        return authenticationInfo;
    }
}
