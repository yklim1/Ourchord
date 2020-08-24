package com.example.ourchord_app;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

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

        View folder_view = inflater.inflate(R.layout.fragment_folder, container, false);

        // 첫화면 업로드 폴더 지정
        final FragmentTransaction fragmenetTransaction = getChildFragmentManager().beginTransaction();
        fragmenetTransaction.add(R.id.file_layout, new upload_folder()).commit();

        // 악보 파일 업로드, MIDI 파일 확인 탭 구분
        final Button upload_tab, midiupload_tab;
        upload_tab = (Button) folder_view.findViewById(R.id.upload_tab);
        upload_tab.setOnClickListener(this);
        midiupload_tab = (Button) folder_view.findViewById(R.id.midiupload_tab);
        midiupload_tab.setOnClickListener(this);

        return folder_view;
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
