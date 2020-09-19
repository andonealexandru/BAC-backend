package com.example.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.ImageView;
import android.widget.ProgressBar;

import com.bumptech.glide.Glide;


public class StartingScreen extends Activity {

    /** Duration of wait **/
    private final int SPLASH_DISPLAY_LENGTH = 5000;
    ImageView gifLoading;
    ProgressBar pb;
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle icicle) {
        super.onCreate(icicle);
        setContentView(R.layout.starting_screen);
        pb = findViewById(R.id.progressBar2);
        pb.setVisibility(View.VISIBLE);

        /* New Handler to start the Menu-Activity
         * and close this Splash-Screen after some seconds.*/
        new Handler().postDelayed(new Runnable(){
            @Override
            public void run() {
                /* Create an Intent that will start the Menu-Activity. */
                Intent mainIntent = new Intent(StartingScreen.this, LogInScreen.class);
                StartingScreen.this.startActivity(mainIntent);
                StartingScreen.this.finish();
            }
        }, SPLASH_DISPLAY_LENGTH);
    }
}