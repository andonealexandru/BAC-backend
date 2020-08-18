package com.example.myapplication;

import android.app.Application;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;

public class StaticVariables extends Application {
    private int mark = 10;
    private String code = "";

    public void reseetMark(){ mark = 10; }

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

    public String getDate()
    {
        DateFormat df = new SimpleDateFormat("dd.MM.yyyy HH:mm");
        String date = df.format(Calendar.getInstance().getTime());
        return date;
    }
}
