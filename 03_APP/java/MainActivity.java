package com.example.ourchord_app;

import android.os.Bundle;
import android.view.MenuItem;

import com.google.android.material.bottomnavigation.BottomNavigationView;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

public class MainActivity extends AppCompatActivity {

    private BottomNavigationView bottomNavigationView;
    private FragmentManager fm;
    private FragmentTransaction ft;
    private folder Folder;
    private conversion Conversion;
    private tune Tune;
    private setting Setting;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        bottomNavigationView = findViewById(R.id.bottom_layout);
        bottomNavigationView.setOnNavigationItemSelectedListener(new BottomNavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem menuItem) {
                switch (menuItem.getItemId()){
                    case R.id.sheet_folder_menu:
                        setFrag(0);
                        break;
                    case R.id.conversion_menu:
                        setFrag(1);
                        break;
                    case R.id.tuning_menu:
                        setFrag(2);
                        break;
                    case R.id.setting_menu:
                        setFrag(3);
                        break;
                }
                return true;
            }
        });
        Folder = new folder();
        Conversion = new conversion();
        Tune = new tune();
        Setting = new setting();
        setFrag(0); //첫 프래그먼트 화면 지정
    }
    //프레그먼트 교체
    private void setFrag(int n) {
        fm = getSupportFragmentManager();
        ft = fm.beginTransaction(); //실제적인 프레그먼트 교체
        switch (n) {
            case 0:
                ft.replace(R.id.main_layout, folder.newInstance());
                ft.commit(); //저장
                break;
            case 1:
                ft.replace(R.id.main_layout, Conversion);
                ft.commit(); //저장
                break;
            case 2:
                ft.replace(R.id.main_layout, Tune);
                ft.commit(); //저장
                break;
            case 3:
                ft.replace(R.id.main_layout, Setting);
                ft.commit();
        }
    }
}
