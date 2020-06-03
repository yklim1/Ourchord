package com.example.ourchord_app;

import android.media.SoundPool;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;


public class tune extends Fragment {

    SoundPool pool;
    int c, cup, d, dup, e, f, fup, g, gup, a, aup, b;

    Button C, Cup, D, Dup, E, F, Fup, G, Gup, A, Aup, B;

    private View tune;

    @NonNull
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @NonNull ViewGroup container, @NonNull  Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        tune = inflater.inflate(R.layout.fragment_tune, container, false);

        ClickedKeyboard(tune);

        return tune;
    }
    public void ClickedKeyboard(View tune){
        C = (Button)tune.findViewById(R.id.C_chord);
        Cup = (Button)tune.findViewById(R.id.Cup_chord);
        D = (Button)tune.findViewById(R.id.D_chord);
        Dup = (Button)tune.findViewById(R.id.Dup_chord);
        E = (Button)tune.findViewById(R.id.E_chord);
        F = (Button)tune.findViewById(R.id.F_chord);
        Fup = (Button)tune.findViewById(R.id.Fup_chord);
        G = (Button)tune.findViewById(R.id.G_chord);
        Gup = (Button)tune.findViewById(R.id.Gup_chord);
        A = (Button)tune.findViewById(R.id.A_chord);
        Aup = (Button)tune.findViewById(R.id.Aup_chord);
        B = (Button)tune.findViewById(R.id.B_chord);

        switch (tune.getId()){
            case R.id.C_chord:
                pool.play(c, 1, 1, 0, 0, 1);
                break;
            case R.id.Cup_chord :
                pool.play(cup, 1, 1, 0, 0, 1);
                break;
            case R.id.D_chord :
                pool.play(d, 1, 1, 0, 0, 1);
                break;
            case R.id.Dup_chord :
                pool.play(dup, 1, 1, 0, 0, 1);
                break;
            case R.id.E_chord :
                pool.play(e, 1, 1, 0, 0, 1);
                break;
            case R.id.F_chord :
                pool.play(f, 1, 1, 0, 0, 1);
                break;
            case R.id.Fup_chord :
                pool.play(fup, 1, 1, 0, 0, 1);
                break;
            case R.id.G_chord :
                pool.play(g, 1, 1, 0, 0, 1);
                break;
            case R.id.Gup_chord :
                pool.play(gup, 1, 1, 0, 0, 1);
                break;
            case R.id.A_chord :
                pool.play(a, 1, 1, 0, 0, 1);
                break;
            case R.id.Aup_chord :
                pool.play(aup, 1, 1, 0, 0, 1);
                break;
            case R.id.B_chord :
                pool.play(b, 1, 1, 0, 0, 1);
                break;
        }
    }
}