package com.example.ourchord_app;

import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;

import androidx.appcompat.app.AppCompatActivity;

public class find_pw extends AppCompatActivity {

    private Handler mHandler;
    private Socket socket;

    private BufferedReader networkReader;
    private PrintWriter networkWriter;

    private DataOutputStream dos = null;
    private DataInputStream dis;

    private String ip = "IP주소";            // IP 번호
    private int port = 9300;

    common UserInfo = new common();

    EditText ID, EMAIL;
    Button find_pw_btn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_find_pw);

        ID = (EditText)findViewById(R.id.id_input);
        EMAIL = (EditText)findViewById(R.id.email_input);

        final String activity = "find_pw";
        final String id = ID.getText().toString();
        final String email = EMAIL.getText().toString();

        find_pw_btn = (Button)findViewById(R.id.find_pw_btn);

        find_pw_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // 비밀번호 이메일로 전송
                Toast.makeText(find_pw.this, "입력한 이메일로 아이디가 전송되었습니다.", Toast.LENGTH_SHORT).show();
                connect_find_pw(activity, id, email);
            }
        });
    }
    // 데이터베이스(서버) 전송
    void connect_find_pw(final String Activity, final String Id, final String Email) {
        mHandler = new Handler();
        Log.w("connect", "연결 하는중");

        Thread FIND_PW = new Thread() {
            public void run() {
                try {
                    socket = new Socket(ip, port);
                    Log.w("서버 접속됨", "서버 접속됨");
                } catch (IOException e1) {
                    Log.w("서버접속못함", "서버접속못함");
                    e1.printStackTrace();
                }
                try {
                    dos = new DataOutputStream(socket.getOutputStream());   // output에 보낼꺼 넣음
                    dis = new DataInputStream(socket.getInputStream());

                    // input에 받을꺼 넣어짐
                    Log.w("Activity 확인 ", Activity);
                    Log.w("Id 확인 ", Id);
                    Log.w("Eamil 확인  ", Email);

                    String RegisterInfo = Activity + "-" + Id + "-" + Email;
                    dos.writeBytes(RegisterInfo);
                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼", "버퍼생성 잘못됨");
                }
                Log.w("버퍼", "버퍼생성 잘됨");
            }
        };
        FIND_PW.start();
        Log.w("버퍼", "check");
        try{
            FIND_PW.join();
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
