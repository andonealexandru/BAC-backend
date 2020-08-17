package com.example.myapplication;

import android.app.ActionBar;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.GridLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.RelativeLayout.LayoutParams;

import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

import com.google.android.gms.auth.api.signin.GoogleSignIn;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;
import com.google.android.gms.auth.api.signin.GoogleSignInClient;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class HistoryTab extends AppCompatActivity {

    TextView testHistoryTab, tv_date, tv_mark;
    GridLayout gridLayout;
    GoogleSignInAccount account;
    GoogleSignInClient mGoogleSignInClient;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_history_tab);


        gridLayout = findViewById(R.id.grid_layout);
        testHistoryTab = findViewById(R.id.test_history_tab);

       /* GoogleSignInOptions gso = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                .requestEmail()
                .build();

        mGoogleSignInClient = GoogleSignIn.getClient(this, gso);

        account = GoogleSignIn.getLastSignedInAccount(this);*/

       // connectServer(account.getEmail());

        addCardView("azi", "yay", "-1");
        addCardView("maine", "y", "1");
        addCardView("ieri", "yay", "-1");

    }

    void connectServer(String data){


        String postUrl= "http://192.168.1.3:5000/retrieve_history";


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
                            testHistoryTab.setText(res);
                            JSONArray historyArray = new JSONArray(res);
                            for(int i = 0; i < historyArray.length(); ++i){
                                JSONObject history_code = new JSONObject();
                                history_code = historyArray.getJSONObject(i);
                                String date = history_code.getString("date"), code = history_code.getString("code"), mark = history_code.getString("mark");
                                addCardView(date, code, mark);
                                //Toast.makeText(getApplicationContext(), "yay obiect json", Toast.LENGTH_LONG).show();

                            }
                        } catch (IOException | JSONException e) {
                            e.printStackTrace();
                        }
                    }
                });
            }
        });

    }

    void addCardView(String date, String code, String mark)
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

        tv_date.setTextColor(Color.WHITE);
        tv_mark.setTextColor(Color.WHITE);

        tv_date.setTextSize(20);
        tv_mark.setTextSize(20);

        tv_date.setText(date);
        tv_mark.setText(mark);

        tv_date.setPadding(20, 0, 0, 0);
        tv_mark.setPadding(0, 0, 20, 0);


        tv_date.setGravity(Gravity.CENTER_VERTICAL);
        tv_mark.setGravity(Gravity.CENTER_VERTICAL);
        tv_mark.setGravity(Gravity.END);

        cardView.setCardBackgroundColor(Color.MAGENTA);
        cardView.addView(tv_date);
        cardView.addView(tv_mark);

        gridLayout.addView(cardView);

    }

}
