package com.jd.jdos.sunshine.service.impl;

import com.jd.jdos.sunshine.domain.User;
import com.jd.jdos.sunshine.dao.UserMapper;
import com.jd.jdos.sunshine.service.UserService;
import com.baomidou.mybatisplus.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

/**
 * <p>
 *  服务实现类
 * </p>
 *
 * @author m8cool
 * @since 2018-06-22
 */
@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {

}
