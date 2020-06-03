package com.example.ourchord_app;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.google.android.material.badge.BadgeUtils;
import com.google.android.material.textfield.TextInputEditText;

public class login extends AppCompatActivity {

    String IDok = "";
    String PWDok = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        EditText ID, PWD;
        ID = (EditText) findViewById(R.id.id_input);
        PWD = (EditText) findViewById(R.id.pwd_input);

        Button login_btn, joinin_btn, find_idpw_btn;
        login_btn = (Button)findViewById(R.id.login_btn);
        joinin_btn = (Button)findViewById(R.id.go_join_btn);
        find_idpw_btn = (Button)findViewById(R.id.go_find_idpw_btn);

        // 로그인 버튼 클릭 시 메인으로 넘어가는 부분 (디비에서 받아오게 바꿔야함) - 05/21
        login_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                EditText ID, PWD;
                ID = (EditText) findViewById(R.id.id_input);
                PWD = (EditText) findViewById(R.id.pwd_input);

                if (ID.getText().toString().equals(IDok) && PWD.getText().toString().equals(PWDok)) {

                    Intent intent = new Intent(getApplicationContext(), MainActivity.class);
                    startActivity(intent);
                }
            }
        });

        // 회원가입 버튼 클릭 시 회원가입 창으로 넘어가는 부분
        joinin_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), register.class);
                startActivity(intent);
            }
        });

        // 아이디, 비밀번호 찾기 클릭 시 아이디, 비밀번호 찾기 창으로 넘어가는 부분
        find_idpw_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), find_idpw.class);
                startActivity(intent);
            }
        });
    }
}
