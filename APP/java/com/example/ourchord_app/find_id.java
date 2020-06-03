package com.example.ourchord_app;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;


public class find_id extends Fragment {
    private View view;

    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @NonNull ViewGroup container, @NonNull  Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.fragment_find_id, container, false);
        return view;
    }
}
