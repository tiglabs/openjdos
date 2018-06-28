package com.jd.jdos.sunshine.domain;

/**
 * Created by m8cool on 2018/6/25.
 */

import org.hibernate.validator.constraints.NotEmpty;

import javax.validation.constraints.Digits;
import javax.validation.constraints.Min;

/**
 * 分页请求参数
 */
public class PageVo {

    @Min(1)
    int size ;

    @Min(1)
    int current;

    public int getSize() {
        return size;
    }

    public void setSize(int size) {
        this.size = size;
    }

    public int getCurrent() {
        return current;
    }

    public void setCurrent(int current) {
        this.current = current;
    }
}
