package com.example.ourchord_app;

import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;

import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentTransaction;

public class folder extends Fragment implements View.OnClickListener {


    public static folder newInstance() {
        return new folder();
    }

    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // Inflate the layout for this fragment

        View fv = inflater.inflate(R.layout.fragment_folder, container, false);

        // 첫화면 업로드 폴더 지정
        FragmentTransaction fragmenetTransaction = getChildFragmentManager().beginTransaction();
        fragmenetTransaction.add(R.id.file_layout, new upload_folder()).commit();

        ImageButton renew = (ImageButton) fv.findViewById(R.id.renew_btn);

        Button upload_tab, midiupload_tab;
        upload_tab = (Button) fv.findViewById(R.id.upload_tab);
        upload_tab.setOnClickListener(this);
        midiupload_tab = (Button) fv.findViewById(R.id.midiupload_tab);
        midiupload_tab.setOnClickListener(this);

        // 새로고침으로 바꿔야함!
        renew.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getContext(), upload_folder.class);
                intent.addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP);
                startActivity(intent);
            }
        });
        return fv;
    }
    @Override
    public void onClick(View view)
    {
        Fragment fg;
        switch (view.getId())
        {
            case R.id.upload_tab :
                fg = upload_folder.newInstance();
                setChildFragment(fg);
                break;
            case R.id.midiupload_tab :
                fg = midiupload_folder.newInstance();
                setChildFragment(fg);
                break;
        }
    }
    private void setChildFragment(Fragment child){
        FragmentTransaction childft = getChildFragmentManager().beginTransaction();

        if(!child.isAdded())
        {
            childft.replace(R.id.file_layout, child);
            childft.addToBackStack(null);
            childft.commit();
        }
    }
}
