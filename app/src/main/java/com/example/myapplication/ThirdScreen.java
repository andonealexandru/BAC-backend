package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class ThirdScreen extends AppCompatActivity {

    Button btn_finish, btn_back;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_third_screen);

        btn_finish = findViewById(R.id.btn_next3);
        btn_back = findViewById(R.id.btn_back3);

        btn_back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(ThirdScreen.this, Second.class);
                startActivity(intent);

            }
        });

        btn_finish.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast.makeText(ThirdScreen.this, "Wooow", Toast.LENGTH_LONG).show();
            }
        });

    }
}