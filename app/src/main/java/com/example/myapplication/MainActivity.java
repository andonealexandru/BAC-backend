package com.example.myapplication;

import android.Manifest;
import android.content.ClipData;
import android.content.ContentValues;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
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

import java.io.ByteArrayOutputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
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

public class MainActivity extends AppCompatActivity {

    public static final int PERMISSION_CODE = 1000;
    public static final int IMAGE_CAPTURE_CODE = 1001;
    public static final int GALLERY_PERMISSION_CODE = 1002;
    public static final int GALLERY_CODE = 1003;
    Button btn_start, btn_capture, btn_select, btn_next, btn_send;
    RadioGroup radioGroup;
    RadioButton selectedButton;
    ImageView imgView, profilePicture;
    Uri image_uri;
    TextView profileName;
    GoogleSignInClient mGoogleSignInClient;
    GoogleSignInAccount account;
    ProgressBar progressBar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_gradient);


        btn_capture = findViewById(R.id.camera_button);
        btn_select = findViewById(R.id.gallery_button);
        imgView = findViewById(R.id.imgView_preview);
        profilePicture = findViewById(R.id.profilePicture);
        profileName = findViewById(R.id.profileName);
        progressBar = findViewById(R.id.progressBar);
        progressBar.setVisibility(View.INVISIBLE);


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
                        .cornerRadiusDp(30)
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

        btn_select.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) { // daca versiunea e mai mare decat marshmallow, trebuie ceruta permisiune de acces la camera
                    if (checkSelfPermission(Manifest.permission.READ_EXTERNAL_STORAGE) == PackageManager.PERMISSION_DENIED) {
                        String permissions[] = {Manifest.permission.READ_EXTERNAL_STORAGE};
                        requestPermissions(permissions, GALLERY_PERMISSION_CODE); // cerem acces la GALERIE

                    } else openGallery(); // deja avem acces, deschidem camera
                } else openGallery(); // nu e nevoie de acces, deschidem camera
            }
        });


        btn_capture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.M){ // daca versiunea e mai mare decat marshmallow, trebuie ceruta permisiune de acces la camera
                    if(checkSelfPermission(Manifest.permission.CAMERA) == PackageManager.PERMISSION_DENIED ||
                            checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_DENIED) // daca nu are deja acces
                    {
                        String permissions[] = {Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE};
                        requestPermissions(permissions, PERMISSION_CODE); // cerem acces la camera

                    }
                    else openCamera(); // deja avem acces, deschidem camera
                }
                else openCamera(); // nu e nevoie de acces, deschidem camera
            }
        });

    }

    private void openGallery(){
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, false);
        intent.setType("image/*");
        startActivityForResult(intent, GALLERY_CODE);
    }

    private void openCamera()
    {
        ContentValues values = new ContentValues();
        values.put(MediaStore.Images.Media.TITLE, "New Picture");
        values.put(MediaStore.Images.Media.DESCRIPTION, "From the camera");
        image_uri = getContentResolver().insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values);
        Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, image_uri);
        startActivityForResult(cameraIntent, IMAGE_CAPTURE_CODE);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        // vedem daca a fost permis sau nu accesul la camera
        if(requestCode == PERMISSION_CODE){
                if(grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED)
                    openCamera();
                else Toast.makeText(MainActivity.this, "Permission denied...", Toast.LENGTH_LONG).show();
            }
        if(requestCode == GALLERY_PERMISSION_CODE){
            if(grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED)
                openGallery();
            else Toast.makeText(MainActivity.this, "Permission denied...", Toast.LENGTH_LONG).show();
        }

    }

    void connectServer(String data){


        String postUrl= "http://192.168.1.12:5000/upload";


        JSONObject imageJSON = new JSONObject();
        try {
            imageJSON.put("key", data);
        } catch (JSONException e){
            e.printStackTrace();
        }



        MediaType mediaType = MediaType.parse("application/json; charset=utf-8");
        RequestBody postBody = RequestBody.create(mediaType, imageJSON.toString());


        postRequest(postUrl, postBody);
    }

    void postRequest(String postUrl, RequestBody postBody) {

        progressBar.setVisibility(View.VISIBLE);

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
                        progressBar.setVisibility(View.INVISIBLE);
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
                        progressBar.setVisibility(View.INVISIBLE);

                        try {
                            res = response.body().string();
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                        Intent sal = new Intent(getApplicationContext(), Second.class);
                        sal.putExtra("compiled_code", res);
                        startActivity(sal);
                    }
                });
            }
        });
    }

    public String BitMapToString(Bitmap bitmap){
        ByteArrayOutputStream baos=new  ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.PNG,100, baos);
        byte [] b=baos.toByteArray();
        String temp=Base64.encodeToString(b, Base64.DEFAULT);
        return temp;
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == IMAGE_CAPTURE_CODE && resultCode == RESULT_OK) {
            imgView.setImageURI(image_uri);
            InputStream is = null;
            try {
                is = getContentResolver().openInputStream(image_uri);
                Bitmap imgBitmap = BitmapFactory.decodeStream(is);
                connectServer(BitMapToString(imgBitmap));


            } catch (FileNotFoundException e) {
                Toast.makeText(MainActivity.this, "Oops", Toast.LENGTH_LONG).show();
                e.printStackTrace();
            }
        }
        if (requestCode == GALLERY_CODE && resultCode == RESULT_OK)
        {
            if(Build.VERSION.SDK_INT >= 16) {
                final List<Bitmap> bitmaps = new ArrayList<Bitmap>();
                ClipData clipData = data.getClipData();
                if(clipData != null)
                {
                    for(int i = 0; i < clipData.getItemCount(); ++i)
                    {
                        Uri imageURI = clipData.getItemAt(i).getUri();
                        try {
                            InputStream is = getContentResolver().openInputStream(imageURI);
                            Bitmap newBitmap = BitmapFactory.decodeStream(is);

                            bitmaps.add(newBitmap);
                        } catch (FileNotFoundException e) {
                            e.printStackTrace();
                        }
                    }
                }
                else {
                    Uri imageURI = data.getData();
                    try {
                        InputStream is = getContentResolver().openInputStream(imageURI);
                        Bitmap newBitmap = BitmapFactory.decodeStream(is);
                        connectServer(BitMapToString(newBitmap));
                        bitmaps.add(newBitmap);
                    } catch (FileNotFoundException e) {
                        e.printStackTrace();
                    }
                }

                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        for(final Bitmap b : bitmaps)
                        {
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    imgView.setImageBitmap(b);
                                }
                            });
                            try {
                                Thread.sleep(3000);
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            }
                        }
                    }
                }).start();
            }
        }
    }

}