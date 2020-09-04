package com.example.myapplication;

import android.app.Application;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;

public class StaticVariables extends Application {
    private int mark = 10;
    private Integer maxMark = 10;
    private String code = "";
    private String input = "";
    private String accountType = "";

    public void resetMark() {
        mark = 10;
    }

    public int getMark(){
        return mark;
    }

    public void setMark(int mar){
        mark = mar;
    }

    public void resetMaxMark() {
        maxMark = 10;
    }

    public Integer getMaxMark() {
        return maxMark;
    }

    public void setMaxMark(Integer maxMark) {
        this.maxMark = maxMark;
    }

    public String getCode(){
        return code;
    }

    public void setCode(String str){
        code = str;
    }

    public void resetInput() {
        input = "";
    }

    public String getInput() {
        return input;
    }

    public void setInput(String input) {
        this.input = input;
    }

    public String getAccountType()
    {
        return accountType;
    }

    public void setAccountType(String str)
    {
        accountType = str;
    }

    public String getDate()
    {
        DateFormat df = new SimpleDateFormat("dd.MM.yyyy HH:mm");
        String date = df.format(Calendar.getInstance().getTime());
        return date;
    }
}
