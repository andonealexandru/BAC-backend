package com.example.myapplication;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.gms.auth.api.signin.GoogleSignIn;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;
import com.google.android.gms.auth.api.signin.GoogleSignInClient;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.squareup.picasso.Picasso;

import org.json.JSONException;
import org.json.JSONObject;

public class ThirdScreen extends AppCompatActivity {

    Button btn_finish, btn_back;
    ImageView profilePicture;

    GoogleSignInClient mGoogleSignInClient;
    GoogleSignInAccount account;
    TextView profileName, tvOutput;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_third_screen);

        btn_finish = findViewById(R.id.btn_next3);
        btn_back = findViewById(R.id.btn_back3);
        profilePicture = findViewById(R.id.profilePicture);
        profileName = findViewById(R.id.profileName);
        tvOutput = findViewById(R.id.tvOutput);

        write_compile_result();


      GoogleSignInOptions gso = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                .requestEmail()
                .build();

        mGoogleSignInClient = GoogleSignIn.getClient(this, gso);

        account = GoogleSignIn.getLastSignedInAccount(this);

        profileName.setText(account.getDisplayName());

        if(account.getPhotoUrl() != null)
            Picasso.get().load(account.getPhotoUrl()).into(profilePicture);

        btn_back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(ThirdScreen.this, Second.class);
                startActivity(intent);

            }
        });

        profilePicture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), ProfileSettings.class);
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

    void write_compile_result()
    {

        Bundle extras = getIntent().getExtras();
        String json_as_string = extras.getString("compile_result");
        tvOutput.setText(json_as_string);
        try {
            JSONObject object = new JSONObject(json_as_string);
            String compile_status = object.getString("compile_status");
            if(compile_status.equals("OK"))
            {
                String output = object.getJSONObject("run_status").getString("output");
                String forTV = "Compile status: OK\n" + "Output: " + output;
                tvOutput.setText(forTV);
            }
            else{
                String forTV = "Compile status: " + compile_status;
                tvOutput.setText(forTV);
            }

        }catch(JSONException e){
            e.printStackTrace();
            return;
        }



    }
}