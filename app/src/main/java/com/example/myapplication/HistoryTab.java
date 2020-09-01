package com.example.myapplication;

import android.app.ActionBar;
import android.app.Dialog;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.Build;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.GridLayout;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.RelativeLayout.LayoutParams;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

import com.google.android.gms.auth.api.signin.GoogleSignIn;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;
import com.google.android.gms.auth.api.signin.GoogleSignInClient;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.makeramen.roundedimageview.RoundedTransformationBuilder;
import com.squareup.picasso.Picasso;
import com.squareup.picasso.Transformation;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class HistoryTab extends AppCompatActivity {

    TextView testHistoryTab, tv_date, tv_mark, tv_name;
    GridLayout gridLayout;
    GoogleSignInAccount account;
    GoogleSignInClient mGoogleSignInClient;
    List<String> codes;
    int tag_cardview = 0;
    TextView profileName;
    ImageView profilePicture;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_history_tab);
        codes = new ArrayList<String>();

        gridLayout = findViewById(R.id.grid_layout);
        testHistoryTab = findViewById(R.id.test_history_tab);
        profilePicture = findViewById(R.id.profilePicture);
        profileName = findViewById(R.id.profileName);

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


        profilePicture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), ProfileSettings.class);
                startActivity(intent);
            }
        });


        connectServer(account.getEmail());



    }

    void connectServer(String data){


        String postUrl= "http://bac-advanced-compiler.herokuapp.com//retrieve_history";


        JSONObject imageJSON = new JSONObject();
        try {
            imageJSON.put("email", data);
        } catch (JSONException e){
            e.printStackTrace();
        }



        MediaType mediaType = MediaType.parse("application/json; charset=utf-8");
        RequestBody postBody = RequestBody.create(mediaType, imageJSON.toString());


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
                        String res = null;
                        try {
                            res = response.body().string();
                            JSONArray historyArray = new JSONArray(res);
                            for(int i = 0; i < historyArray.length(); ++i){
                                JSONObject history_code = new JSONObject();
                                history_code = historyArray.getJSONObject(i);
                                String date = history_code.getString("date"), code = history_code.getString("code"), mark = history_code.getString("mark"), name = history_code.getString("name");
                                addCardView(date, code, mark, name);

                            }
                        } catch (IOException | JSONException e) {
                            e.printStackTrace();
                        }
                    }
                });
            }
        });

    }

    void addCardView(String date, String code, String mark, String name)
    {
        CardView cardView = new CardView(getApplicationContext());
        LayoutParams layoutparams = new LayoutParams(
                LayoutParams.MATCH_PARENT,
                200
        );

        layoutparams.setMargins(30, 30, 30, 30);

        cardView.setLayoutParams(layoutparams);


        tv_date = new TextView(getApplicationContext());
        tv_mark = new TextView(getApplicationContext());
        tv_name = new TextView(getApplicationContext());

        tv_date.setTextColor(getResources().getColor(R.color.colorWhite));
        tv_mark.setTextColor(getResources().getColor(R.color.colorWhite));
        tv_name.setTextColor(getResources().getColor(R.color.colorWhite));

        tv_date.setTextSize(20);
        tv_mark.setTextSize(20);
        tv_name.setTextSize(24);

        tv_date.setText(date);
        tv_mark.setText("Mark: " + mark);
        tv_name.setText(name);

        tv_date.setPadding(20, 0, 0, 20);
        tv_mark.setPadding(0, 0, 20, 0);
        tv_name.setPadding(20, 20, 0, 0);


        tv_mark.setGravity(Gravity.CENTER_VERTICAL | Gravity.END);
        tv_date.setGravity(Gravity.BOTTOM);

        cardView.setCardBackgroundColor(getResources().getColor(R.color.colorElevatedCard));
        cardView.addView(tv_date);
        cardView.addView(tv_mark);
        cardView.addView(tv_name);
        cardView.setTag(tag_cardview);
        tag_cardview++;
        codes.add(code);


        cardView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                int cardView_code_pos = (int) view.getTag();
                openPopup(codes.get(cardView_code_pos));

            }
        });

        gridLayout.addView(cardView);

    }

    void openPopup(final String code)
    {
        final Dialog input_popup = new Dialog(this);
        input_popup.setContentView(R.layout.history_popup);
        input_popup.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
        input_popup.show();

        Button code_btn_close, code_btn_second;
        final TextView code_tv;
        code_btn_close = input_popup.findViewById(R.id.button_popup_close);
        code_btn_second = input_popup.findViewById(R.id.button_popup_second);
        code_tv = input_popup.findViewById(R.id.tv_code);
        code_tv.setText(code);

        code_btn_close.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                input_popup.dismiss();
            }
        });

        code_btn_second.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), Second.class);
                intent.putExtra("compiled_code", code);
                startActivity(intent);
            }
        });

    }

}