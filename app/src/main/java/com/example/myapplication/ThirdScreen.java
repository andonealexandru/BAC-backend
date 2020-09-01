package com.example.myapplication;

import android.app.Dialog;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.gms.auth.api.signin.GoogleSignIn;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;
import com.google.android.gms.auth.api.signin.GoogleSignInClient;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.makeramen.roundedimageview.RoundedTransformationBuilder;
import com.squareup.picasso.Picasso;
import com.squareup.picasso.Transformation;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

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
        if(account != null) {

            profileName.setText(account.getDisplayName());
            if (account.getPhotoUrl() != null) {
                profilePicture.setImageURI(null);

                Transformation transformation = new RoundedTransformationBuilder()
                        .borderWidthDp(0)
                        .cornerRadiusDp(130)
                        .oval(false)
                        .build();

                Picasso.get()
                        .load(account.getPhotoUrl())
                        .transform(transformation)
                        .into(profilePicture);
            }
        }

        btn_back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
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
                openPopup();
            }
        });

    }
    String history_name = "";
    void openPopup()
    {
        final Dialog input_popup = new Dialog(this);
        input_popup.setContentView(R.layout.history_name_popup);
        input_popup.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
        input_popup.show();

        Button input_btn_next;
        final EditText input_text;
        input_btn_next = input_popup.findViewById(R.id.button_popup_next);
        input_text = input_popup.findViewById(R.id.edit_text_input);

        input_btn_next.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                history_name = input_text.getText().toString();
                input_popup.dismiss();
                finish();
                Intent intent = new Intent(getApplicationContext(), MainActivity.class);
                startActivity(intent);
                StaticVariables app = (StaticVariables) getApplicationContext();
                connectServer();

                app.resetMark();
                app.resetInput();
                app.resetMaxMark();
            }
        });
    }


    void connectServer(){

        if(history_name.equals(""))
            history_name = "Unnamed";

        String postUrl= "https://bac-advanced-compiler.herokuapp.com/add_history";

        StaticVariables app = (StaticVariables) getApplicationContext();
        String code = app.getCode(), mark = app.getMark() + "", date = app.getDate();


        JSONObject historyJSON = new JSONObject();
        JSONObject history_data = new JSONObject();

        try{
            history_data.put("code", code);
            history_data.put("mark", mark);
            history_data.put("date", date);
            history_data.put("name", history_name);
        } catch(JSONException e){
            e.printStackTrace();
        }
        try {
            historyJSON.put("email", account.getEmail());
            historyJSON.put("history", history_data);

        } catch (JSONException e){
            e.printStackTrace();
        }



        MediaType mediaType = MediaType.parse("application/json; charset=utf-8");
        RequestBody postBody = RequestBody.create(mediaType, historyJSON.toString());


        postRequest(postUrl, postBody);
    }

    void postRequest(String postUrl, RequestBody postBody) {

        OkHttpClient client = new OkHttpClient.Builder()
                .connectTimeout(0, TimeUnit.SECONDS)
                .writeTimeout(0, TimeUnit.SECONDS)
                .readTimeout(0, TimeUnit.SECONDS)
                .build();

        Request request = new Request.Builder()
                .url(postUrl)
                .post(postBody)
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, final IOException e) {
                // Cancel the post on failure.
                call.cancel();

                // In order to access the TextView inside the UI thread, the code is executed inside runOnUiThread()
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Toast.makeText(getApplicationContext(), "Failed to connect", Toast.LENGTH_LONG).show();
                        e.printStackTrace();
                    }
                });
            }

            @Override
            public void onResponse(Call call, final Response response) throws IOException {
                // In order to access the TextView inside the UI thread, the code is executed inside runOnUiThread()
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {

                    }
                });
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
            StaticVariables app = (StaticVariables) getApplicationContext();
            if(compile_status.equals("OK"))
            {
                String output = object.getJSONObject("run_status").getString("output");
                String forTV = "Compile status: OK\n" + "Output: " + output + "\n Mark:" + app.getMark();
                tvOutput.setText(forTV);
            }
            else{

                String forTV = "Compile status: " + compile_status;
                app.setMark(app.getMark() - 1);

                tvOutput.setText(forTV + '\n' + "Mark:" + app.getMark());
            }

        }catch(JSONException e){
            e.printStackTrace();
            return;
        }



    }
}