package com.jd.jdos.sunshine;

import com.baomidou.mybatisplus.generator.AutoGenerator;
import com.baomidou.mybatisplus.generator.InjectionConfig;
import com.baomidou.mybatisplus.generator.config.*;
import com.baomidou.mybatisplus.generator.config.builder.ConfigBuilder;
import com.baomidou.mybatisplus.generator.config.rules.DbType;
import com.baomidou.mybatisplus.generator.config.rules.NamingStrategy;
import com.baomidou.mybatisplus.toolkit.StringUtils;
import org.apache.commons.beanutils.MethodUtils;
import org.junit.Test;
import org.springframework.util.ClassUtils;
import org.springframework.util.ReflectionUtils;

import java.io.File;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Map;

/**
 * Created by m8cool on 2018/6/22.
 */
public class MpGenerator {

    @Test
    public void generateCode() {
        String packageName = "com.jd.jdos.sunshine";
        boolean serviceNameStartWithI = false;//user -> UserService, 设置成true: user -> IUserService
        generateByTables(serviceNameStartWithI, packageName, "envs", "envs_host","envs_log");
    }

    private void generateByTables(boolean serviceNameStartWithI, String packageName, String... tableNames) {
        GlobalConfig config = new GlobalConfig();
        String dbUrl = "jdbc:mysql://10.8.64.170:3306/sunshine_dashboard";
        DataSourceConfig dataSourceConfig = new DataSourceConfig();
        dataSourceConfig.setDbType(DbType.MYSQL)
                .setUrl(dbUrl)
                .setUsername("root")
                .setPassword("123456")
                .setDriverName("com.mysql.jdbc.Driver");
        StrategyConfig strategyConfig = new StrategyConfig();
        strategyConfig
                .setCapitalMode(true)
                .setEntityLombokModel(false)
                .setDbColumnUnderline(true)
                .setNaming(NamingStrategy.underline_to_camel)
                .setInclude(tableNames);//修改替换成你需要的表名，多个表名传数组
        config.setActiveRecord(false)
                .setEnableCache(false)
                .setAuthor("m8cool")
                .setOutputDir("D:\\GitHub\\sunshine\\sunshine\\sunshine-api\\src\\main\\java")
                .setFileOverride(true).setBaseResultMap(true).setBaseColumnList(true);
        if (!serviceNameStartWithI) {
            config.setServiceName("%sService");
        }
        AutoGenerator autoGenerator = new AutoGenerator().setGlobalConfig(config)
                .setDataSource(dataSourceConfig)
                .setStrategy(strategyConfig)
                .setPackageInfo(
                        new PackageConfig()
                                .setParent(packageName)
                                .setController("api")
                                .setMapper("dao")
                                .setEntity("domain")
                );

        // 不想在dao下面生成mapper
        /*try {
            Method method = ReflectionUtils.findMethod(AutoGenerator.class,"initConfig");
            method.setAccessible(true);
            method.invoke(autoGenerator,null) ;
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            e.printStackTrace();
        }*/
        /*ConfigBuilder configBuilder = autoGenerator.getConfig() ;
        Map<String,String> pathInfo = configBuilder.getPathInfo();
        Map<String,String> packageInfo = configBuilder.getPackageInfo();

        pathInfo.put(ConstVal.XML_PATH, "D:\\GitHub\\sunshine\\sunshine\\sunshine-build\\src\\main\\resources\\mapper");*/
        autoGenerator.execute();
    }

    private void generateByTables(String packageName, String... tableNames) {
        generateByTables(true, packageName, tableNames);
    }

}
