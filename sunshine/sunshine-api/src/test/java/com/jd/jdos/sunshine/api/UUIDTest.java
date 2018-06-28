package com.jd.jdos.sunshine.api;

import com.jd.jdos.sunshine.util.UUIDUtil;
import org.apache.commons.lang3.StringUtils;
import org.junit.Assert;
import org.junit.Test;

/**
 * Created by m8cool on 2018/6/28.
 */
public class UUIDTest {

    @Test
    public void testUUID(){
        String uuid = UUIDUtil.getUUID();
        System.out.println(uuid);
        Assert.assertTrue(StringUtils.length(uuid) == 32);
    }
}
