package com.jd.jdos.sunshine.api;

import com.jd.jdos.sunshine.domain.ApiResponse;
import com.jd.jdos.sunshine.exception.ApiRunningException;
import com.jd.jdos.sunshine.exception.DeployEnvironmentException;
import com.jd.jdos.sunshine.exception.HttpRequestExcetpion;
import com.jd.jdos.sunshine.exception.ParamException;
import com.sun.javafx.collections.MappingChange;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.support.ResourceBundleMessageSource;
import org.springframework.http.HttpStatus;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.Locale;

/**
 * Created by zhangkai12 on 2018/6/12.
 */
public class BaseController {

    Logger logger = LoggerFactory.getLogger(BaseController.class) ;

    @Autowired
    ResourceBundleMessageSource messageSource;

    /**
     * 构造返回结果
     * @param code
     * @param params
     * @return
     */
    public ApiResponse build(String code,Object... params){
        ApiResponse apiResponse = new ApiResponse();
        apiResponse.setCode(code);
        String message = messageSource.getMessage(code,params.clone(), Locale.getDefault());
        apiResponse.setMessage(message);
        return apiResponse;
    }


    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseBody
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ApiResponse notValidException(MethodArgumentNotValidException exception) {

        logger.error("MethodArgumentNotValidException",exception.getMessage());

        BindingResult bindingResult = exception.getBindingResult();
        for (FieldError fieldError : bindingResult.getFieldErrors()) {
            return build(fieldError.getDefaultMessage());
        }
        return build("system.parameter.error");
    }


    @ExceptionHandler
    @ResponseBody
    public ApiResponse exception(HttpServletRequest request, HttpServletResponse response, Exception exception) {

        logger.error("INTERNAL_SERVER_ERROR",exception);
        response.setStatus(HttpStatus.INTERNAL_SERVER_ERROR.value());
        if (exception instanceof ApiRunningException) {//登入异常
            ApiRunningException loginException = (ApiRunningException) exception;
            return build(loginException.getMessage(),loginException.getParams());
        }
        return build("system.internal.error");
    }

    public ApiResponse success(){
        return new ApiResponse("success","");
    }

    public ApiResponse success(Object data){
        return new ApiResponse("success","",data);
    }

    public ApiResponse failure(){
        return new ApiResponse("failure","");
    }

    public ApiResponse failure(String message){
        return new ApiResponse("failure",message);
    }

    public ApiResponse failure(String code,String message){
        return new ApiResponse(code,message);
    }

}
