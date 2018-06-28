package com.jd.jdos.sunshine.domain;

import com.baomidou.mybatisplus.annotations.TableField;
import org.hibernate.validator.constraints.Length;
import org.hibernate.validator.constraints.NotBlank;

import java.io.Serializable;
import java.util.Date;

/**
 * <p>
 * 
 * </p>
 *
 * @author m8cool
 * @since 2018-06-22
 */
public class UserCreateRequest {

    @NotBlank
    @Length(min = 4,max = 32)
    private String name;

    @NotBlank
    @Length(min = 4,max = 32)
    private String password;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}
