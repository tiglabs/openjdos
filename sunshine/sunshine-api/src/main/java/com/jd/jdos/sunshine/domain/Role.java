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
public class Role implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId
    private String uuid;
    private String role;
    private String description;
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

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
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
        return "Role{" +
        ", uuid=" + uuid +
        ", role=" + role +
        ", description=" + description +
        ", lastOpDate=" + lastOpDate +
        ", createDate=" + createDate +
        "}";
    }
}
