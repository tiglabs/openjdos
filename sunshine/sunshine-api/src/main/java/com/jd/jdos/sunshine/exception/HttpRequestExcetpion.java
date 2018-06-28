package com.jd.jdos.sunshine.exception;

/**
 * Created by zhangkai12 on 2018/6/16.
 */
public class HttpRequestExcetpion  extends ApiRunningException {
    public HttpRequestExcetpion(Object[] params) {
        super(params);
    }

    public HttpRequestExcetpion(String message, Object[] params) {
        super(message, params);
    }

    public HttpRequestExcetpion(String message, Throwable cause, Object[] params) {
        super(message, cause, params);
    }

    public HttpRequestExcetpion(Throwable cause, Object[] params) {
        super(cause, params);
    }

    public HttpRequestExcetpion(String message, Throwable cause, boolean enableSuppression, boolean writableStackTrace, Object[] params) {
        super(message, cause, enableSuppression, writableStackTrace, params);
    }
}
