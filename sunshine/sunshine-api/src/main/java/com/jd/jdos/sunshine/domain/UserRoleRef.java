package com.jd.jdos.sunshine.domain;

import com.baomidou.mybatisplus.enums.IdType;
import java.util.Date;
import com.baomidou.mybatisplus.annotations.TableId;
import com.baomidou.mybatisplus.annotations.TableField;
import java.io.Serializable;

/**
 * <p>
 * 
 * </p>
 *
 * @author m8cool
 * @since 2018-06-22
 */
public class UserRoleRef implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(value = "id", type = IdType.AUTO)
    private Long id;
    @TableField("userUuid")
    private String userUuid;
    @TableField("roleUuid")
    private String roleUuid;
    /**
     * last operation date
     */
    @TableField("lastOpDate")
    private Date lastOpDate;
    @TableField("createDate")
    private Date createDate;


    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUserUuid() {
        return userUuid;
    }

    public void setUserUuid(String userUuid) {
        this.userUuid = userUuid;
    }

    public String getRoleUuid() {
        return roleUuid;
    }

    public void setRoleUuid(String roleUuid) {
        this.roleUuid = roleUuid;
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
        return "UserRoleRef{" +
        ", id=" + id +
        ", userUuid=" + userUuid +
        ", roleUuid=" + roleUuid +
        ", lastOpDate=" + lastOpDate +
        ", createDate=" + createDate +
        "}";
    }
}
