package com.example.ourchord_app;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class find_idpw extends AppCompatActivity{

    find_id fragment1;
    find_pw fragment2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_find_idpw);

        fragment1 = new find_id();
        fragment2 = new find_pw();

        Button find_id, find_pw;
        find_id = (Button)findViewById(R.id.find_id_tab);
        find_pw = (Button)findViewById(R.id.find_pw_tab);

        find_id.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v){
                getSupportFragmentManager().beginTransaction().replace(R.id.find_layout, fragment1).commit();
            }
        });
        find_pw.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v){
                getSupportFragmentManager().beginTransaction().replace(R.id.find_layout, fragment2).commit();
            }
        });
    }
    public void onFragmentChange(int index){
        if(index == 0){
            getSupportFragmentManager().beginTransaction().replace(R.id.find_layout, fragment1).commit();
        }
        else if(index == 1){
            getSupportFragmentManager().beginTransaction().replace(R.id.find_layout, fragment2).commit();
        }
        else{
            getSupportFragmentManager().beginTransaction().replace(R.id.find_layout, fragment1).commit();
        }
    }
}
