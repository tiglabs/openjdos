package com.jd.jdos.sunshine.work;

import com.google.common.eventbus.EventBus;
import com.google.common.eventbus.Subscribe;
import org.springframework.beans.BeansException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.config.BeanPostProcessor;
import org.springframework.stereotype.Component;

import java.lang.annotation.Annotation;
import java.lang.reflect.Method;

/**
 * Created by zhangkai12 on 2018/6/13.
 */
@Component
public class EventSubscribeBeanPostProcessor implements BeanPostProcessor {
    @Autowired
    EventBus eventBus;

    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName)
            throws BeansException {
        Method[] methods = bean.getClass().getMethods();
        for (Method method : methods) {
            Annotation[] annotations = method.getAnnotations();
            for (Annotation annotation : annotations) {
                if (annotation.annotationType().equals(Subscribe.class)) {
                    eventBus.register(bean);
                    return bean;
                }
            }
        }
        return bean;
    }


}
