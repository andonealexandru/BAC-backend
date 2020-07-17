package com.example.myapplication;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;

public class Second extends AppCompatActivity{

    Button btn_next, btn_back;
    Button btn_to_first_page, btn_to_third_page;
    CodeEditText codeEditText;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);

        btn_next = findViewById(R.id.btn_next);
        btn_back = findViewById(R.id.btn_back);
        btn_to_first_page = findViewById(R.id.btn_first_page);
        btn_to_third_page = findViewById(R.id.btn_third_page);
        codeEditText = (CodeEditText) findViewById(R.id.input_editText);


        Spinner dropdown = findViewById(R.id.spinner_select_compiler);
        String[] items = new String[]{"C", "C++", "Pascal"};
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, items);
        dropdown.setAdapter(adapter);

        btn_to_first_page.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(Second.this, MainActivity.class);
                startActivity(intent);
            }
        });
        btn_to_third_page.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
               // Intent intent = new Intent(Second.this, MainActivity.class);
               // startActivity(intent);
            }
        });

    }

}