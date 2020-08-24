package com.example.ourchord_app;

import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import androidx.fragment.app.Fragment;

public class setting extends Fragment {
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {

        View fv = inflater.inflate(R.layout.fragment_setting, container, false);

        Button my, notice, faq;
        my = (Button) fv.findViewById(R.id.my_tab);
        notice = (Button) fv.findViewById(R.id.notice_tab);
        faq = (Button) fv.findViewById(R.id.faq_tab);

        my.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getContext(), my.class);
                startActivity(intent);
            }
        });
        notice.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getContext(), notice.class);
                startActivity(intent);
            }
        });
        faq.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getContext(), faq.class);
                startActivity(intent);
            }
        });
        return fv;
    }
}
