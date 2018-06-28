package com.jd.jdos.sunshine.domain;

import com.baomidou.mybatisplus.enums.IdType;
import java.util.Date;
import com.baomidou.mybatisplus.annotations.TableId;
import java.io.Serializable;

/**
 * <p>
 * 环境部署主机表
 * </p>
 *
 * @author m8cool
 * @since 2018-06-26
 */
public class EnvsHost implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * ID
     */
    @TableId(value = "id", type = IdType.AUTO)
    private Integer id;
    /**
     * 主机标识
     */
    private String hostId;
    /**
     * 主机IP
     */
    private String hostIp;
    /**
     * 环境id
     */
    private String envId;
    /**
     * 主机类型（标识主机是物理机 aws ec2）
     */
    private String hostType;
    /**
     * 服务状态（可用 不可用）
     */
    private String status;
    private String certificate;
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

    public String getHostId() {
        return hostId;
    }

    public void setHostId(String hostId) {
        this.hostId = hostId;
    }

    public String getHostIp() {
        return hostIp;
    }

    public void setHostIp(String hostIp) {
        this.hostIp = hostIp;
    }

    public String getEnvId() {
        return envId;
    }

    public void setEnvId(String envId) {
        this.envId = envId;
    }

    public String getHostType() {
        return hostType;
    }

    public void setHostType(String hostType) {
        this.hostType = hostType;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getCertificate() {
        return certificate;
    }

    public void setCertificate(String certificate) {
        this.certificate = certificate;
    }

    public Date getCreateTime() {
        return createTime;
    }

    public void setCreateTime(Date createTime) {
        this.createTime = createTime;
    }

    @Override
    public String toString() {
        return "EnvsHost{" +
        ", id=" + id +
        ", hostId=" + hostId +
        ", hostIp=" + hostIp +
        ", envId=" + envId +
        ", hostType=" + hostType +
        ", status=" + status +
        ", certificate=" + certificate +
        ", createTime=" + createTime +
        "}";
    }
}
