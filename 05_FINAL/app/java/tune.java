package com.example.ourchord_app;

import android.media.MediaPlayer;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

public class tune extends Fragment {

    Button C, CUP, D, DUP, E, F, FUP, G, GUP, A, AUP, B;
    MediaPlayer mediaPlayer;

    private View tune;

    @NonNull
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @NonNull ViewGroup container, @NonNull Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        tune = inflater.inflate(R.layout.fragment_tune, container, false);

        C = (Button)tune.findViewById(R.id.C_chord);
        CUP = (Button)tune.findViewById(R.id.Cup_chord);
        D = (Button)tune.findViewById(R.id.D_chord);
        DUP = (Button)tune.findViewById(R.id.Dup_chord);
        E = (Button)tune.findViewById(R.id.E_chord);
        F = (Button)tune.findViewById(R.id.F_chord);
        FUP = (Button)tune.findViewById(R.id.Fup_chord);
        G = (Button)tune.findViewById(R.id.G_chord);
        GUP = (Button)tune.findViewById(R.id.Gup_chord);
        A = (Button)tune.findViewById(R.id.A_chord);
        AUP = (Button)tune.findViewById(R.id.Aup_chord);
        B = (Button)tune.findViewById(R.id.B_chord);

        C.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mediaPlayer = MediaPlayer.create(getContext(), R.raw.c);
                mediaPlayer.start();
            }
        });
        CUP.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mediaPlayer = MediaPlayer.create(getContext(), R.raw.cup);
                mediaPlayer.start();
            }
        });
        D.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mediaPlayer = MediaPlayer.create(getContext(), R.raw.d);
                mediaPlayer.start();
            }
        });
        DUP.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mediaPlayer = MediaPlayer.create(getContext(), R.raw.dup);
                mediaPlayer.start();
            }
        });
        E.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mediaPlayer = MediaPlayer.create(getContext(), R.raw.e);
                mediaPlayer.start();
            }
        });
        F.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mediaPlayer = MediaPlayer.create(getContext(), R.raw.f);
                mediaPlayer.start();
            }
        });
        FUP.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mediaPlayer = MediaPlayer.create(getContext(), R.raw.fup);
                mediaPlayer.start();
            }
        });
        G.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mediaPlayer = MediaPlayer.create(getContext(), R.raw.g);
                mediaPlayer.start();
            }
        });
        GUP.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mediaPlayer = MediaPlayer.create(getContext(), R.raw.gup);
                mediaPlayer.start();
            }
        });
        A.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mediaPlayer = MediaPlayer.create(getContext(), R.raw.a);
                mediaPlayer.start();
            }
        });
        AUP.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mediaPlayer = MediaPlayer.create(getContext(), R.raw.aup);
                mediaPlayer.start();
            }
        });
        B.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mediaPlayer = MediaPlayer.create(getContext(), R.raw.b);
                mediaPlayer.start();
            }
        });
        return tune;
    }
}