package com.example.myapplication;

import android.app.Application;

public class StaticVariables extends Application {
    private int mark = 0;
    private String code = "";

    public int getMark(){
        return mark;
    }

    public void setMark(int mar){
        mark = mar;
    }

    public String getCode(){
        return code;
    }

    public void setCode(String str){
        code = str;
    }
}
