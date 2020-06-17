package com.example.myapplication;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.content.ClipData;
import android.content.ContentValues;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Toast;

import java.io.FileNotFoundException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    public static final int PERMISSION_CODE = 1000;
    public static final int IMAGE_CAPTURE_CODE = 1001;
    public static final int GALLERY_PERMISSION_CODE = 1002;
    public static final int GALLERY_CODE = 1003;
    Button btn_start, btn_capture, btn_select;
    RadioGroup radioGroup;
    RadioButton selectedButton;
    ImageView imgView;
    Uri image_uri;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        btn_start = findViewById(R.id.button_start);
        radioGroup = findViewById(R.id.group_button);
        btn_capture = findViewById(R.id.btnCapture);
        imgView = findViewById(R.id.imgView);
        btn_select = findViewById(R.id.button_select);

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

        btn_start.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                int selectedRadio = radioGroup.getCheckedRadioButtonId();
                selectedButton = findViewById(selectedRadio);

                Toast.makeText(MainActivity.this, "You selected " + selectedButton.getText(), Toast.LENGTH_LONG).show();

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
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
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
        //Toast.makeText(MainActivity.this, "Result " + requestCode, Toast.LENGTH_LONG).show();
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

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == IMAGE_CAPTURE_CODE && resultCode == RESULT_OK)
            imgView.setImageURI(image_uri);
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