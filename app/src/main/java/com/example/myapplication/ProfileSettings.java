package com.example.myapplication;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

import com.google.android.gms.auth.api.signin.GoogleSignIn;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;
import com.google.android.gms.auth.api.signin.GoogleSignInClient;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.makeramen.roundedimageview.RoundedTransformationBuilder;
import com.squareup.picasso.Picasso;
import com.squareup.picasso.Transformation;

public class ProfileSettings extends AppCompatActivity {

    CardView signOutBtn, exitBtn, historyBtn;
    GoogleSignInClient mGoogleSignInClient;
    GoogleSignInAccount account;
    ImageView profile_picture;
    TextView profileName;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile_settings);
        signOutBtn = findViewById(R.id.card_log_out);
        exitBtn = findViewById(R.id.card_exit);
        historyBtn = findViewById(R.id.card_history);
        profileName = findViewById(R.id.profile_name);
        profile_picture = findViewById(R.id.profile_image);

        GoogleSignInOptions gso = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                .requestEmail()
                .build();

        mGoogleSignInClient = GoogleSignIn.getClient(this, gso);

        account = GoogleSignIn.getLastSignedInAccount(this);

        profileName.setText(account.getDisplayName());

        if(account.getPhotoUrl() != null){
            profile_picture.setImageURI(null);

            Transformation transformation = new RoundedTransformationBuilder()
                    .borderWidthDp(0)
                    .cornerRadiusDp(130)
                    .oval(false)
                    .build();


            Picasso.get()
                    .load(account.getPhotoUrl())
                    .transform(transformation)
                    .into(profile_picture);
        }


        signOutBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                signOut();

                Intent i=new Intent(getApplicationContext(), LogInScreen.class);
                i.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                finish();
                startActivity(i);
            }
        });

        exitBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(Intent.ACTION_MAIN);
                intent.addCategory(Intent.CATEGORY_HOME);
                intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                startActivity(intent);
            }
        });

        historyBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), HistoryTab.class);
                startActivity(intent);
            }
        });

    }

    private void signOut() {
        mGoogleSignInClient.signOut()
                .addOnCompleteListener(this, new OnCompleteListener<Void>() {
                    @Override
                    public void onComplete(@NonNull Task<Void> task) {
                        Toast.makeText(getApplicationContext(), "You've signed out", Toast.LENGTH_LONG).show();

                    }
                });
    }

}