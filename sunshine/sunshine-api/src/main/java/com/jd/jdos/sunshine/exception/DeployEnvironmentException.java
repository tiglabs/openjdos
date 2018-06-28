package com.jd.jdos.sunshine.exception;

/**
 * Created by zhangkai12 on 2018/6/13.
 */
public class DeployEnvironmentException extends ApiRunningException {
    public DeployEnvironmentException(Object[] params) {
        super(params);
    }

    public DeployEnvironmentException(String message, Object[] params) {
        super(message, params);
    }

    public DeployEnvironmentException(String message, Throwable cause, Object[] params) {
        super(message, cause, params);
    }

    public DeployEnvironmentException(Throwable cause, Object[] params) {
        super(cause, params);
    }

    public DeployEnvironmentException(String message, Throwable cause, boolean enableSuppression, boolean writableStackTrace, Object[] params) {
        super(message, cause, enableSuppression, writableStackTrace, params);
    }
}
