package com.example.myapplication;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Spinner;
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

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class Second extends AppCompatActivity{

    Button btn_next, btn_back;
    CodeEditText codeEditText;
    ImageView profilePicture;
    Spinner dropdown;

    GoogleSignInClient mGoogleSignInClient;
    GoogleSignInAccount account;
    TextView profileName;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);

        btn_next = findViewById(R.id.btn_next);
        btn_back = findViewById(R.id.btn_back);
        profilePicture = findViewById(R.id.profilePicture);
        codeEditText = (CodeEditText) findViewById(R.id.input_editText);
        profileName = findViewById(R.id.profileName);


        dropdown = findViewById(R.id.spinner_select_compiler);
        String[] items = new String[]{"C", "C++", "Pascal"};
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, items);
        dropdown.setAdapter(adapter);


        /*GoogleSignInOptions gso = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                .requestEmail()
                .build();

        mGoogleSignInClient = GoogleSignIn.getClient(this, gso);

        account = GoogleSignIn.getLastSignedInAccount(this);

        profileName.setText(account.getDisplayName());

        if(account.getPhotoUrl() != null)
            Picasso.get().load(account.getPhotoUrl()).into(profilePicture);

        profilePicture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), ProfileSettings.class);
                startActivity(intent);
            }
        });*/

        btn_back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), MainActivity.class);
                startActivity(intent);

            }
        });

        btn_next.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                sendForCompile();
                //Intent intent = new Intent(getApplicationContext(), ThirdScreen.class);
                //startActivity(intent);

            }
        });

    }

    void sendForCompile()
    {
        String http_api = "http://192.168.1.254:5000/compile";

        String code = codeEditText.getText().toString();
        String lang = dropdown.getSelectedItem().toString();
        if(lang.equals("C++"))
            lang = "CPP11";
        if(lang.equals("Pascal"))
            lang = "PASCAL";

        final JSONObject data = new JSONObject();
        try {
            data.put("source", code);
            //data.put("input", input);
            data.put("lang", lang);
        }catch(JSONException e){
            e.printStackTrace();
            return;
        }

        MediaType mediaType = MediaType.parse("application/json; charset=utf-8");
        RequestBody postBody = RequestBody.create(mediaType, data.toString());
        OkHttpClient client = new OkHttpClient();

        Request request = new Request.Builder()
                .url(http_api)
                .post(postBody)
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, final IOException e) {
                call.cancel();

                // In order to access the TextView inside the UI thread, the code is executed inside runOnUiThread()
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Toast.makeText(getApplicationContext(), "failed to connect", Toast.LENGTH_LONG).show();
                        codeEditText.setText(e.getMessage());
                    }
                });
            }

            @Override
            public void onResponse(Call call, final Response response) throws IOException {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        TextView responseText = findViewById(R.id.statusTextView);
                        try {
                            codeEditText.setText(response.body().string());
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                });
            }
        });

    }
}