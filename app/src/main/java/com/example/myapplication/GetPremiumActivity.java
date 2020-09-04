package com.example.myapplication;

import android.app.Dialog;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.auth.api.signin.GoogleSignIn;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;
import com.stripe.android.ApiResultCallback;
import com.stripe.android.PaymentConfiguration;
import com.stripe.android.PaymentIntentResult;
import com.stripe.android.Stripe;
import com.stripe.android.model.ConfirmPaymentIntentParams;
import com.stripe.android.model.PaymentIntent;
import com.stripe.android.model.PaymentMethodCreateParams;
import com.stripe.android.view.CardInputWidget;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.lang.ref.WeakReference;
import java.util.Objects;
import java.util.concurrent.TimeUnit;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class GetPremiumActivity extends AppCompatActivity {

    private String paymentIntentClientSecret;
    private Stripe stripe;
    CardInputWidget cardInputWidget;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_get_premium);
        cardInputWidget = findViewById(R.id.cardInputWidget);
        PaymentConfiguration.init(
                getApplicationContext(),
                "pk_test_51HNFe4AqwyEMhL7ItJ6brCcWDmDkP4A7nVEhDbxW2VM8hzaXX63z8CkXVFZn7AcPXcrLh6MpKGgFrZPXqHmjfIx800mCB4mNsE"
        );

        startCheckout();


    }

    void startCheckout()
    {
        connectServer();
        Button payButton = findViewById(R.id.payButton);
        payButton.setOnClickListener((View view) -> {
            PaymentMethodCreateParams params = cardInputWidget.getPaymentMethodCreateParams();
            if (params != null) {
                ConfirmPaymentIntentParams confirmParams = ConfirmPaymentIntentParams
                        .createWithPaymentMethodCreateParams(params, paymentIntentClientSecret);
                final Context context = getApplicationContext();
                stripe = new Stripe(
                        context,
                        PaymentConfiguration.getInstance(context).getPublishableKey()
                );
                stripe.confirmPayment(this, confirmParams);
            }
        });
    }


    void connectServer(){


        String postUrl= "http://bac-advanced-compiler.herokuapp.com/get_payment_secret";

        postRequest(postUrl);
    }

    void postRequest(String postUrl) {

        OkHttpClient client = new OkHttpClient.Builder()
                .connectTimeout(0, TimeUnit.SECONDS)
                .writeTimeout(0, TimeUnit.SECONDS)
                .readTimeout(0, TimeUnit.SECONDS)
                .build();

        Request request = new Request.Builder()
                .url(postUrl)
                .get()
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, final IOException e) {
                call.cancel();

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
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {

                        try {
                            paymentIntentClientSecret = response.body().string();
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                        Toast.makeText(getApplicationContext(), "yay", Toast.LENGTH_LONG).show();
                    }
                });
            }
        });
    }

    void updatePremium_mongo()
    {


        GoogleSignInAccount account = GoogleSignIn.getLastSignedInAccount(this);

        String http_api = "http://bac-advanced-compiler.herokuapp.com/got_premium";


        final JSONObject data = new JSONObject();
        try {
            data.put("email", account.getEmail());
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
                    }
                });
            }

            @Override
            public void onResponse(Call call, final Response response) throws IOException {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        makeText("Connected, updated!");
                        StaticVariables app = (StaticVariables) getApplicationContext();
                        app.setAccountType("premium");
                    }
                });
            }
        });

    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        // Handle the result of stripe.confirmPayment
        stripe.onPaymentResult(requestCode, data, new PaymentResultCallback(this));
    }

    private final class PaymentResultCallback
            implements ApiResultCallback<PaymentIntentResult> {
        @NonNull private final WeakReference<GetPremiumActivity> activityRef;

        PaymentResultCallback(@NonNull GetPremiumActivity activity) {
            activityRef = new WeakReference<>(activity);
        }

        @Override
        public void onSuccess(@NonNull PaymentIntentResult result) {
            final GetPremiumActivity activity = activityRef.get();
            if (activity == null) {
                return;
            }

            PaymentIntent paymentIntent = result.getIntent();
            PaymentIntent.Status status = paymentIntent.getStatus();
            if (status == PaymentIntent.Status.Succeeded) {
                // Payment completed successfully
                makeText("Payment complete");
                updatePremium_mongo();
                /*Gson gson = new GsonBuilder().setPrettyPrinting().create();
                activity.displayAlert(
                        "Payment completed",
                        gson.toJson(paymentIntent),
                        true
                );*/
            } else if (status == PaymentIntent.Status.RequiresPaymentMethod) {
                // Payment failed
                makeText("Payment failed");
               /* activity.displayAlert(
                        "Payment failed",
                        Objects.requireNonNull(paymentIntent.getLastPaymentError()).getMessage(),
                        false
                );*/
            }
        }

        @Override
        public void onError(@NonNull Exception e) {
            final GetPremiumActivity activity = activityRef.get();
            if (activity == null) {
                return;
            }

            // Payment request failed – allow retrying using the same payment method
            makeText("Payment request failed");
        }
    }
    void makeText(String msg)
    {
        Toast.makeText(GetPremiumActivity.this, msg, Toast.LENGTH_LONG).show();
    }
}
