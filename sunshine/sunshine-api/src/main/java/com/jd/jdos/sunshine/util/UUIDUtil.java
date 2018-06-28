package com.jd.jdos.sunshine.util;


import com.sun.org.apache.bcel.internal.generic.RETURN;

import java.util.UUID;

import static java.util.UUID.randomUUID;

/**
 * Created by m8cool on 2018/6/28.
 */
public class UUIDUtil {
    public static String getUUID(){
        return UUID.randomUUID().toString().replaceAll("-","");
    }
}
