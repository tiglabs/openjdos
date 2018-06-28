package com.jd.jdos.sunshine.exception;

/**
 * Created by zhangkai12 on 2018/6/12.
 */
public class ParamException extends ApiRunningException {
    public ParamException(Object[] params) {
        super(params);
    }

    public ParamException(String message, Object[] params) {
        super(message, params);
    }

    public ParamException(String message, Throwable cause, Object[] params) {
        super(message, cause, params);
    }

    public ParamException(Throwable cause, Object[] params) {
        super(cause, params);
    }

    public ParamException(String message, Throwable cause, boolean enableSuppression, boolean writableStackTrace, Object[] params) {
        super(message, cause, enableSuppression, writableStackTrace, params);
    }
}
