package com.example.ourchord_app;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;

import androidx.appcompat.app.AppCompatActivity;

public class my extends AppCompatActivity {

    private Handler mHandler;
    private Socket socket;

    private BufferedReader networkReader;
    private PrintWriter networkWriter;

    private DataOutputStream dos = null;
    private DataInputStream dis;

    private String ip = "";            
    private int port = ;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_my);

        // 로그인, 로딩 화면으로 넘어가는 버튼
        ImageButton pre_btn, home_btn;
        pre_btn = (ImageButton) findViewById(R.id.pre_btn);

        Button modify;
        modify = (Button) findViewById(R.id.my_change_btn);

        // 로그인, 로딩 화면으로 넘어가는 부분
        pre_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), setting.class);
                startActivity(intent);
            }
        });
        modify.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                System.out.println("개인 정보 수정 정보 전송");
                EditText C_NAME, C_ID, C_EMAIL;
                C_NAME = (EditText) findViewById(R.id.input_change_name);
                C_ID = (EditText) findViewById(R.id.input_change_id);
                C_EMAIL = (EditText) findViewById(R.id.input_change_email);

                String C_name = C_NAME.getText().toString();
                String C_id = C_ID.getText().toString();
                String C_email = C_EMAIL.getText().toString();
                connect(C_name, C_id, C_email);

                Toast.makeText(getApplicationContext(), "개인 정보 수정이 완료되었습니다.",Toast.LENGTH_SHORT).show();
            }
        });
    }
    public static final int DEFAULT_BUFFER_SIZE = 10000;

    void connect(final String CName, final String CId, final String CEmail) {
        mHandler = new Handler();
        Log.w("connect", "연결 하는중");

        Thread checkUpdate = new Thread() {
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
                    Log.w("확인", CName);

                    // input에 받을꺼 넣어짐
                    Log.w("이름 수정 확인 ", CName);
                    Log.w("ID 수정 확인 ", CId);
                    Log.w("Eamil 수정 확인  ", CEmail);

                    String RegisterInfo = CName + "-" + CId + "-" + CEmail;
                    dos.writeBytes(RegisterInfo);
                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼", "버퍼생성 잘못됨");
                }
                Log.w("버퍼", "버퍼생성 잘됨");
            }
        };
        checkUpdate.start();
        Log.w("버퍼", "check");
        try{
            checkUpdate.join();
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
