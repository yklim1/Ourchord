package com.example.ourchord_app;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class faq extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_faq);

        final LinearLayout faq1_section, faq2_section, faq3_section, faq4_section, faq5_section;
        final TextView faq1, faq2, faq3, faq4, faq5;

        faq1_section = (LinearLayout)findViewById(R.id.faq1_section);
        faq2_section = (LinearLayout)findViewById(R.id.faq2_section);
        faq3_section = (LinearLayout)findViewById(R.id.faq3_section);
        faq4_section = (LinearLayout)findViewById(R.id.faq4_section);
        faq5_section = (LinearLayout)findViewById(R.id.faq5_section);

        faq1 = (TextView)findViewById(R.id.faq1);
        faq1.setOnClickListener(new View.OnClickListener(){
            @SuppressLint("ResourceAsColor")
            public void onClick(View view){
                if(faq1_section.getVisibility() == View.GONE){
                    faq1_section.setVisibility(View.VISIBLE);
                    faq1.setBackgroundColor(getResources().getColor(R.color.blue));
                }
                else {
                    faq1_section.setVisibility(View.GONE);
                    faq1.setBackgroundColor(getResources().getColor(R.color.trans));
                }
            }
        });
        faq2 = (TextView)findViewById(R.id.faq2);
        faq2.setOnClickListener(new View.OnClickListener(){
            public void onClick(View view){
                if(faq2_section.getVisibility() == View.GONE){
                    faq2_section.setVisibility(View.VISIBLE);
                    faq2.setBackgroundColor(getResources().getColor(R.color.blue));
                }
                else {
                    faq2_section.setVisibility(View.GONE);
                    faq2.setBackgroundColor(getResources().getColor(R.color.trans));
                }
            }
        });
        faq3 = (TextView)findViewById(R.id.faq3);
        faq3.setOnClickListener(new View.OnClickListener(){
            public void onClick(View view){
                if(faq3_section.getVisibility() == View.GONE){
                    faq3_section.setVisibility(View.VISIBLE);
                    faq3.setBackgroundColor(getResources().getColor(R.color.blue));
                }
                else {
                    faq3_section.setVisibility(View.GONE);
                    faq3.setBackgroundColor(getResources().getColor(R.color.trans));
                }
            }
        });
        faq4 = (TextView)findViewById(R.id.faq4);
        faq4.setOnClickListener(new View.OnClickListener(){
            public void onClick(View view){
                if(faq4_section.getVisibility() == View.GONE){
                    faq4_section.setVisibility(View.VISIBLE);
                    faq4.setBackgroundColor(getResources().getColor(R.color.blue));
                }
                else {
                    faq4_section.setVisibility(View.GONE);
                    faq4.setBackgroundColor(getResources().getColor(R.color.trans));
                }
            }
        });
        faq5 = (TextView)findViewById(R.id.faq5);
        faq5.setOnClickListener(new View.OnClickListener(){
            public void onClick(View view){
                if(faq5_section.getVisibility() == View.GONE){
                    faq5_section.setVisibility(View.VISIBLE);
                    faq5.setBackgroundColor(getResources().getColor(R.color.blue));
                }
                else {
                    faq5_section.setVisibility(View.GONE);
                    faq5.setBackgroundColor(getResources().getColor(R.color.trans));
                }
            }
        });
    }
}

