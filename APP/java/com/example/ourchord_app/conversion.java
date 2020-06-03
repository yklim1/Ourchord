package com.example.ourchord_app;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RadioGroup;
import android.widget.TextView;

import androidx.fragment.app.Fragment;

public class conversion extends Fragment {


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View fv = inflater.inflate(R.layout.fragment_conversion, container, false);

        final RadioGroup rg1 = (RadioGroup)fv.findViewById(R.id.radioGroup1);
        final RadioGroup rg2 = (RadioGroup)fv.findViewById(R.id.radioGroup2);
        final TextView tv = (TextView) fv.findViewById(R.id.output_chord_conversion);

        return fv;
    }
}
