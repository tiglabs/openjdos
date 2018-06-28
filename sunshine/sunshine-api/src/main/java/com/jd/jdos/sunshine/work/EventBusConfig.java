package com.jd.jdos.sunshine.work;

import com.google.common.eventbus.AsyncEventBus;
import com.google.common.eventbus.EventBus;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.concurrent.Executor;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Created by zhangkai12 on 2018/6/13.
 */
@Configuration
public class EventBusConfig {
    private Executor executor = Executors.newFixedThreadPool(5);
    @Bean
    public EventBus eventBus() {
        return new AsyncEventBus(executor);
    }
}
