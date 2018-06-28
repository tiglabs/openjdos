package com.jd.jdos.sunshine.exception;

/**
 * Created by zhangkai12 on 2018/6/16.
 */
public class ApiRunningException  extends RuntimeException {
    private Object[] params;

    public Object[] getParams() {
        return params;
    }

    public void setParams(Object[] params) {
        this.params = params;
    }

    public ApiRunningException(Object[] params) {
        this.params = params;
    }

    public ApiRunningException(String message, Object[] params) {
        super(message);
        this.params = params;
    }

    public ApiRunningException(String message, Throwable cause, Object[] params) {
        super(message, cause);
        this.params = params;
    }

    public ApiRunningException(Throwable cause, Object[] params) {
        super(cause);
        this.params = params;
    }

    public ApiRunningException(String message, Throwable cause, boolean enableSuppression, boolean writableStackTrace, Object[] params) {
        super(message, cause, enableSuppression, writableStackTrace);
        this.params = params;
    }
}
