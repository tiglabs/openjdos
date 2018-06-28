package com.jd.jdos.sunshine.common;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.jd.jdos.sunshine.form.EnvironmentProcess;
import com.jd.jdos.sunshine.form.EnvironmentRunning;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;

import java.io.IOException;
import java.util.regex.Pattern;

/**
 * Created by zhangkai12 on 2018/6/12.
 */
public class Utils {
    private static final Pattern IPV4_PATTERN = Pattern.compile("^(25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)(\\.(25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)){3}$");
    private static ObjectMapper mapper = new ObjectMapper();
    /**
     * 判断ip是否合法
     * @param input
     * @return
     */
    public static boolean isIPv4Address(final String input) {
        return IPV4_PATTERN.matcher(input).matches();
    }

    /**
     * 格式化对象为字符串
     * @param t
     * @param <T>
     * @return
     */
    public static <T> String json(T t){
        String result = null;
        try {
            result = mapper.writeValueAsString(t);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
        return result;
    }

    /**
     * 反序列化
     * @param json
     * @param tClass
     * @param <T>
     * @return
     */
    public static <T> T json2Obj(String json,Class<T> tClass){
        T result = null;
        try {
            result = mapper.readValue(json,tClass);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return result;
    }

    /**
     * 字符串去重
     * @param list
     */
    public static List<String> removeDuplicate(List<String> list) {
        LinkedHashSet<String> set = new LinkedHashSet<String>(list.size());
        set.addAll(list);
        List<String> newList = new ArrayList<>();
        newList.addAll(set);
        return newList;
    }

    public static void main(String[] args){
        String values = "{\"environment_progress\": 100.0, \"environment_desc\": {\"nodestatus\": {}, \"componentstatus\": {}}, \"environment_params\": \"\", \"environment_result\": true, \"environment_type\": 3, \"environment_time\": \"2018-06-16 23:26:34\", \"environment_status\": \"finished\"}\n";
        EnvironmentRunning result = json2Obj(values,EnvironmentRunning.class);
        System.out.println(result);
    }
}
