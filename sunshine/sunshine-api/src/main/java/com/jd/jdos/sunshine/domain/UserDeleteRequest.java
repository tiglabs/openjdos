package com.jd.jdos.sunshine.domain;

import org.hibernate.validator.constraints.NotBlank;

import java.util.List;

/**
 * <p>
 * 
 * </p>
 *
 * @author m8cool
 * @since 2018-06-22
 */
public class UserDeleteRequest {

    @NotBlank.List({})
    private List<String> uuids;

    public List<String> getUuids() {
        return uuids;
    }

    public void setUuids(List<String> uuids) {
        this.uuids = uuids;
    }
}