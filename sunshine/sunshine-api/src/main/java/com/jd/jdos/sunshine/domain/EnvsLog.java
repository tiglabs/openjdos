package com.jd.jdos.sunshine.domain;

import com.baomidou.mybatisplus.enums.IdType;
import java.util.Date;
import com.baomidou.mybatisplus.annotations.TableId;
import java.io.Serializable;

/**
 * <p>
 * 环境部署操作表
 * </p>
 *
 * @author m8cool
 * @since 2018-06-26
 */
public class EnvsLog implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * ID
     */
    @TableId(value = "id", type = IdType.AUTO)
    private Integer id;
    /**
     * 环境id
     */
    private String envId;
    /**
     * 操作类型
     */
    private String operateType;
    /**
     * 操作人
     */
    private String operateOwner;
    /**
     * 操作描述
     */
    private String operateDesc;
    /**
     * 创建时间
     */
    private Date createTime;


    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getEnvId() {
        return envId;
    }

    public void setEnvId(String envId) {
        this.envId = envId;
    }

    public String getOperateType() {
        return operateType;
    }

    public void setOperateType(String operateType) {
        this.operateType = operateType;
    }

    public String getOperateOwner() {
        return operateOwner;
    }

    public void setOperateOwner(String operateOwner) {
        this.operateOwner = operateOwner;
    }

    public String getOperateDesc() {
        return operateDesc;
    }

    public void setOperateDesc(String operateDesc) {
        this.operateDesc = operateDesc;
    }

    public Date getCreateTime() {
        return createTime;
    }

    public void setCreateTime(Date createTime) {
        this.createTime = createTime;
    }

    @Override
    public String toString() {
        return "EnvsLog{" +
        ", id=" + id +
        ", envId=" + envId +
        ", operateType=" + operateType +
        ", operateOwner=" + operateOwner +
        ", operateDesc=" + operateDesc +
        ", createTime=" + createTime +
        "}";
    }
}
