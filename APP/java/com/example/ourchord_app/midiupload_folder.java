package com.example.ourchord_app;

import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

public class midiupload_folder extends Fragment {
    public static midiupload_folder newInstance(){
        return new midiupload_folder();
    }

    public midiupload_folder() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View fv = inflater.inflate(R.layout.fragment_midiupload_folder, container, false);

        return fv;
    }
}
