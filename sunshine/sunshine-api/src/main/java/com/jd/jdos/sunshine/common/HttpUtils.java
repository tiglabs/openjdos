package com.jd.jdos.sunshine.common;

import com.jd.jdos.sunshine.exception.ApiRunningException;
import com.jd.jdos.sunshine.exception.DeployEnvironmentException;
import okhttp3.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.Map;

/**
 * Created by zhangkai12 on 2018/6/13.
 */
public class HttpUtils {
    Logger logger = LoggerFactory.getLogger(HttpUtils.class);

    public static HttpUtils instance = new HttpUtils();

    private final OkHttpClient client = new OkHttpClient();
    public static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");


    /**
     * 发送get请求(JSON)
     *
     * @param url
     * @return
     * @throws IOException
     */
    public String get(String url) throws IOException {
        Request request = new Request.Builder().url(url).get().build();
        Response response = null;
        String result = null;
        response = client.newCall(request).execute();
        result = response.body().string();
        if(response.code() >299){
            throw new ApiRunningException("service.invoke.error",new String[]{result});
        }
        return result;
    }

    /**
     * 发送post请求
     * @param url
     * @param params
     * @return
     * @throws IOException
     */
    public String post(String url, Map params) throws IOException {
        RequestBody requestBody = RequestBody.create(JSON, Utils.json(params));
        Request request = new Request.Builder().url(url).post(requestBody).build();
        Response response = null;
        String result = null;
        response = client.newCall(request).execute();
        result = response.body().string();
        if(response.code() >299){
            throw new ApiRunningException("service.invoke.error",new String[]{result});
        }

        return result;
    }

}
