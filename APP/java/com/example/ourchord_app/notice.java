package com.example.ourchord_app;

import android.os.Bundle;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class notice extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notice);
        
        final LinearLayout important1_section, important2_section, notice1_section, notice2_section, notice3_section;
        final TextView important1, important2, notice1, notice2, notice3;

        important1_section= (LinearLayout)findViewById(R.id.important1_section);
        important2_section = (LinearLayout)findViewById(R.id.important2_section);
        notice1_section = (LinearLayout)findViewById(R.id.notice1_section);
        notice2_section = (LinearLayout)findViewById(R.id.notice2_section);
        notice3_section = (LinearLayout)findViewById(R.id.notice3_section);

        important1 = (TextView)findViewById(R.id.important1);
        important1.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v){
                if(important1_section.getVisibility() == View.GONE){
                    important1_section.setVisibility(View.VISIBLE);
                    important1.setBackgroundColor(getResources().getColor(R.color.pink_2));
                }
                else {
                    important1_section.setVisibility(View.GONE);
                    important1.setBackgroundColor(getResources().getColor(R.color.trans));
                }
            }
        });
        important2 = (TextView)findViewById(R.id.important2);
        important2.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v){
                if(important2_section.getVisibility() == View.GONE){
                    important2_section.setVisibility(View.VISIBLE);
                    important2.setBackgroundColor(getResources().getColor(R.color.pink_2));

                }
                else {
                    important2_section.setVisibility(View.GONE);
                    important2.setBackgroundColor(getResources().getColor(R.color.trans));
                }
            }
        });
        notice1 = findViewById(R.id.notice1);
        notice1.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v){
                if(notice1_section.getVisibility() == View.GONE){
                    notice1_section.setVisibility(View.VISIBLE);
                    notice1.setBackgroundColor(getResources().getColor(R.color.pink_2));
                }
                else {
                    notice1_section.setVisibility(View.GONE);
                    notice1.setBackgroundColor(getResources().getColor(R.color.trans));
                }
            }
        });
        notice2 = findViewById(R.id.notice2);
        notice2.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v){
                if(notice2_section.getVisibility() == View.GONE){
                    notice2_section.setVisibility(View.VISIBLE);
                    notice2.setBackgroundColor(getResources().getColor(R.color.pink_2));
                }
                else {
                    notice2_section.setVisibility(View.GONE);
                    notice2.setBackgroundColor(getResources().getColor(R.color.trans));
                }
            }
        });
        notice3 = findViewById(R.id.notice3);
        notice3.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v){
                if(notice3_section.getVisibility() == View.GONE){
                    notice3_section.setVisibility(View.VISIBLE);
                    notice3.setBackgroundColor(getResources().getColor(R.color.pink_2));
                }
                else {
                    notice3_section.setVisibility(View.GONE);
                    notice3.setBackgroundColor(getResources().getColor(R.color.trans));
                }
            }
        });
    }
}

