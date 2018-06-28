package com.jd.jdos.sunshine.domain;

import java.util.Date;
import com.baomidou.mybatisplus.annotations.TableField;
import com.baomidou.mybatisplus.annotations.TableId;

import java.io.Serializable;

/**
 * <p>
 * 
 * </p>
 *
 * @author m8cool
 * @since 2018-06-22
 */
public class User implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId
    private String uuid;
    private String name;
    private String password;
    private String salt;
    private Integer locked;
    /**
     * last operation date
     */
    @TableField("lastOpDate")
    private Date lastOpDate;
    @TableField("createDate")
    private Date createDate;


    public String getUuid() {
        return uuid;
    }

    public void setUuid(String uuid) {
        this.uuid = uuid;
    }

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

    public String getSalt() {
        return salt;
    }

    public void setSalt(String salt) {
        this.salt = salt;
    }

    public Integer getLocked() {
        return locked;
    }

    public void setLocked(Integer locked) {
        this.locked = locked;
    }

    public Date getLastOpDate() {
        return lastOpDate;
    }

    public void setLastOpDate(Date lastOpDate) {
        this.lastOpDate = lastOpDate;
    }

    public Date getCreateDate() {
        return createDate;
    }

    public void setCreateDate(Date createDate) {
        this.createDate = createDate;
    }

    @Override
    public String toString() {
        return "User{" +
        ", uuid=" + uuid +
        ", name=" + name +
        ", password=" + password +
        ", salt=" + salt +
        ", locked=" + locked +
        ", lastOpDate=" + lastOpDate +
        ", createDate=" + createDate +
        "}";
    }
}
