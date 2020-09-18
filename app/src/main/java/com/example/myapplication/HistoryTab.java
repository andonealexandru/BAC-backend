package com.example.myapplication;

import android.app.ActionBar;
import android.app.Dialog;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Point;
import android.graphics.drawable.ColorDrawable;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
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

import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.ads.AdView;
import com.google.android.gms.ads.MobileAds;
import com.google.android.gms.ads.initialization.InitializationStatus;
import com.google.android.gms.ads.initialization.OnInitializationCompleteListener;
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
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.concurrent.TimeUnit;

import lecho.lib.hellocharts.model.Axis;
import lecho.lib.hellocharts.model.AxisValue;
import lecho.lib.hellocharts.model.Line;
import lecho.lib.hellocharts.model.LineChartData;
import lecho.lib.hellocharts.model.PointValue;
import lecho.lib.hellocharts.view.LineChartView;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

class GraphData{
    float mark;
    String date;

    public GraphData() {}
    public GraphData(float m, String d){
        mark = m;
        date = d;
    }
}


public class HistoryTab extends AppCompatActivity {

    TextView testHistoryTab, tv_date, tv_mark, tv_name;
    GridLayout gridLayout;
    GoogleSignInAccount account;
    GoogleSignInClient mGoogleSignInClient;
    List<String> codes;
    int tag_cardview = 0;
    TextView profileName;
    ImageView profilePicture;
    AdView mAdView;
    Button btn_grafic;
    List<GraphData> graphDataList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_history_tab);
        codes = new ArrayList<String>();

        gridLayout = findViewById(R.id.grid_layout);
        testHistoryTab = findViewById(R.id.test_history_tab);
        profilePicture = findViewById(R.id.profilePicture);
        profileName = findViewById(R.id.profileName);
        mAdView = findViewById(R.id.adView);
        btn_grafic = findViewById(R.id.btn_grafic);

        // initialize ads
        MobileAds.initialize(this, new OnInitializationCompleteListener() {
            @Override
            public void onInitializationComplete(InitializationStatus initializationStatus) {
            }
        });

        StaticVariables app = (StaticVariables) getApplicationContext();
        if(app.getAccountType().equals("basic"))
        {
            AdRequest adRequest = new AdRequest.Builder().build();
            mAdView.loadAd(adRequest);
        }

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


        profilePicture.setOnClickListener(view -> {
            Intent intent = new Intent(getApplicationContext(), ProfileSettings.class);
            startActivity(intent);
        });

        btn_grafic.setOnClickListener(view -> {
                openPopup_grafic();
        });

        connectServer(account.getEmail());



    }

    void openPopup_grafic() {
        for(int i = 0; i < graphDataList.size()-1; ++i)
            for(int j = i+1; j < graphDataList.size(); ++j)
                if(cmp(graphDataList.get(i).date, graphDataList.get(j).date))
                {
                    GraphData data = graphDataList.get(i);
                    graphDataList.get(i).date = graphDataList.get(j).date;
                    graphDataList.get(i).mark = graphDataList.get(j).mark;

                    graphDataList.get(j).date = data.date;
                    graphDataList.get(j).mark = data.mark;
                }

        final Dialog grafic = new Dialog(this);
        grafic.setContentView(R.layout.grafic_popup);
        grafic.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
        grafic.show();

        Button btn_grafic_finish;
        TextView text_grafic;
        LineChartView chart;

        btn_grafic_finish = grafic.findViewById(R.id.btn_grafic_finish);
        text_grafic = grafic.findViewById(R.id.text_view_grafic);
        chart = grafic.findViewById(R.id.chart);

        List marks = new ArrayList();
        List dates = new ArrayList();

        for(int i = 0; i < graphDataList.size(); ++i){
            marks.add(new PointValue(i, graphDataList.get(i).mark));
            dates.add(i, new AxisValue(i).setLabel(graphDataList.get(i).date));
        }

        Line line = new Line(marks).setColor(Color.parseColor("#000000"));
        List lines = new ArrayList();
        lines.add(line);

        LineChartData data = new LineChartData();
        data.setLines(lines);

        chart.setLineChartData(data);

        Axis axis = new Axis();
        axis.setValues(dates);
        data.setAxisXBottom(axis);
        axis.setTextColor(Color.parseColor("#000000"));
        axis.setName("Dates");

        Axis yAxis = new Axis();
        data.setAxisYLeft(yAxis);
        yAxis.setTextColor(Color.parseColor("#000000"));
        yAxis.setName("Marks %");



        btn_grafic_finish.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                grafic.dismiss();//easy
            }
        });



    }

    void connectServer(String data){


        String postUrl= "http://bac-advanced-compiler.herokuapp.com/retrieve_history";


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
                            graphDataList = new ArrayList<GraphData>();
                            res = response.body().string();
                            JSONArray historyArray = new JSONArray(res);
                            StaticVariables app = (StaticVariables) getApplicationContext();
                            int n = 0;
                            if(app.getAccountType().equals("basic"))
                                n = Math.min(3, historyArray.length());
                            else {
                                n = historyArray.length();
                            }

                            for(int i = historyArray.length() - 1; i >= historyArray.length() - n; --i){
                                JSONObject history_code = new JSONObject();
                                history_code = historyArray.getJSONObject(i);
                                String date = history_code.getString("date"), code = history_code.getString("code"), mark = history_code.getString("mark"), name = history_code.getString("name");
                                String maxMark = history_code.getString("maxMark");

                                graphDataList.add(new GraphData(procentaj(mark, maxMark), date));

                                addCardView(date, code, mark, name);
                                Log.d("history", i+"");
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

    float procentaj(String mark, String maxMark)
    {
        float i_mark = Float.parseFloat(mark);
        float i_maxMark = Float.parseFloat(maxMark);
        return (i_mark*100)/i_maxMark;
    }

    boolean cmp(String s1, String s2){
        DateFormat format = new SimpleDateFormat("dd.MM.yyyy HH:mm");
        try {
            Date date1 = format.parse(s1);
            Date date2 = format.parse(s2);
            return date1.after(date2);
        }catch (ParseException e){
            e.printStackTrace();
            return false;
        }

    }

}
