package com.example.ourchord_app;

import android.content.Intent;
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

public class login extends AppCompatActivity {
    common UserInfo = new common();
    private Handler login_handler;
    private Socket login_socket;

    private BufferedReader networkReader;
    private PrintWriter networkWriter;

    private DataOutputStream dos = null;
    private DataInputStream dis;

    private String ip = "IP주소";            // IP 번호
    private int port = 9300;

    public String user_id_get = "";
    public String user_id_set = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        // 서버 전송 시 액티비티 구분용, 사용자 입력 ID, PWD
        final String activity = "login";
        final EditText ID, PWD;
        ID = (EditText)findViewById(R.id.id_input);
        final String input_id = ID.getText().toString();
        PWD = (EditText)findViewById(R.id.pwd_input);

        // 로그인, 회원가입, ID, 비밀번호 찾기 버튼
        Button login_btn, joinin_btn, find_id_btn, find_pw_btn;
        login_btn = (Button)findViewById(R.id.login_btn);
        joinin_btn = (Button)findViewById(R.id.go_join_btn);
        find_id_btn = (Button)findViewById(R.id.go_find_id_btn);
        find_pw_btn = (Button)findViewById(R.id.go_find_pw_btn);

        // 로그인 버튼 클릭
        login_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // 사용자가 입력한 ID, 비밀번호
                String input_id = (ID.getText().toString());
                UserInfo.SetUser_id(input_id);
                String input_pwd = PWD.getText().toString();

                // 앱 실행 시 입력값 제대로 받아졌는지 확인용 출력
                System.out.println("id check : " + input_id);
                System.out.println("pwd check : " + input_pwd);

                // 서버에 입력한 ID, 비밀번호 있는지 확인하기 위해 check 전송
                char user_check = login_check(activity, input_id, input_pwd);

                // 서버에서 s 돌아오면 로그인 O, f 돌아오면 로그인 X
                if(user_check == 's'){
                    Toast.makeText(getApplicationContext(), input_id + "님 환영합니다.", Toast.LENGTH_SHORT).show();
                    Intent intent = new Intent(getApplicationContext(), MainActivity.class);
                    startActivity(intent);
                }
                else if(user_check == 'f'){
                    Toast.makeText(getApplicationContext(), "올바른 ID 와 비밀번호를 입력해주세요.", Toast.LENGTH_SHORT).show();
                    ID.setText(null);
                    PWD.setText(null);
                }
                else{
                    // if 문 실행 안됬을 때 오류 확인용 출력
                    System.out.print("오류 확인용");
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

        // 아이디 찾기 클릭 시 아이디 찾기 창으로 넘어가는 부분
        find_id_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), find_id.class);
                startActivity(intent);
            }
        });

        // 비밀번호 찾기 클릭 시 비밀번호 찾기 창으로 넘어가는 부분
        find_pw_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), find_pw.class);
                startActivity(intent);
            }
        });
    }

    // 서버 전송 부분 login-id-pwd 전송 됨
    char login_check(final String Activity, final String Id, final String Pwd) {
        login_handler = new Handler();

        // 서버가 s, f 를 아스키코드로 보내기 때문에 s, f 받을 배열 생성
        final char[] receive_login = new char[1];
        Thread LOGIN = new Thread() {
            public void run() {
                // 서버 접속 됬는지 확인용
                try {
                    login_socket = new Socket(ip, port);
                    Log.w("서버 접속됨", "서버 접속됨");
                } catch (IOException e1) {
                    Log.w("서버 접속 못함", "서버 접속 못함");
                    e1.printStackTrace();
                }
                try {
                    // 앱에서 서버로 전송 dos, 서버에서 앱으로 전송 dis
                    dos = new DataOutputStream(login_socket.getOutputStream());
                    dis = new DataInputStream(login_socket.getInputStream());

                    // 서버로 전송할 내용 확인용 출력
                    Log.w("화면 확인 ", Activity);
                    Log.w("ID 확인 ", Id);
                    Log.w("PW 확인 ", Pwd);

                    String LoginInfo = Activity + "-" + Id + "-" + Pwd + "+";
                    dos.writeBytes(LoginInfo);

                    // 서버에서 앱으로 아스키 코드로 전송
                    int checked_login = dis.read();
                    // 아스키코드로 받았기 때문에 s, f 로 바꿈
                    receive_login[0] = (char)checked_login;
                    // 앱에서 서버에서 s, f 보냈는지 확인용 출력
                    System.out.println("확인"+ receive_login[0]);
                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼", "버퍼생성 잘못됨");
                }
                Log.w("버퍼", "버퍼생성 잘됨");
            }
        };
        LOGIN.start();
        Log.w("버퍼", "check");
        try{
            LOGIN.join();
        }catch (Exception e){
            e.printStackTrace();
        }
        return receive_login[0];
    }
}
