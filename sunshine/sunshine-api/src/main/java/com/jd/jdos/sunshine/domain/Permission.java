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
public class Permission implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId
    private String uuid;
    private String name;
    private String type;
    private String permission;
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

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getPermission() {
        return permission;
    }

    public void setPermission(String permission) {
        this.permission = permission;
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
        return "Permission{" +
        ", uuid=" + uuid +
        ", name=" + name +
        ", type=" + type +
        ", permission=" + permission +
        ", lastOpDate=" + lastOpDate +
        ", createDate=" + createDate +
        "}";
    }
}
