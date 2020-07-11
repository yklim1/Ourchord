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

    private Handler mHandler;
    private Socket socket;

    private BufferedReader networkReader;
    private PrintWriter networkWriter;

    private DataOutputStream dos = null;
    private DataInputStream dis;

    private String ip = "";            // IP 번호
    private int port = ;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        final String activity = "login";
        final EditText ID, PWD;
        ID = (EditText)findViewById(R.id.id_input);
        PWD = (EditText)findViewById(R.id.pwd_input);

        Button login_btn, joinin_btn, find_id_btn, find_pw_btn;
        login_btn = (Button)findViewById(R.id.login_btn);
        joinin_btn = (Button)findViewById(R.id.go_join_btn);
        find_id_btn = (Button)findViewById(R.id.go_find_id_btn);
        find_pw_btn = (Button)findViewById(R.id.go_find_pw_btn);

        // 로그인 버튼 클릭 시 메인으로 넘어가는 부분 (디비에서 받아오게 바꿔야함) - 05/21
        login_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String id = ID.getText().toString();
                String pwd = PWD.getText().toString();

                System.out.println("id check : " + id);
                System.out.println("pwd check : " + pwd);
                char check = login(activity, id, pwd);

                if(check == 's'){
                    Toast.makeText(getApplicationContext(), id + "님 환영합니다.", Toast.LENGTH_SHORT).show();
                    Intent intent = new Intent(getApplicationContext(), MainActivity.class);
                    startActivity(intent);
                }
                else if(check == 'f'){
                    Toast.makeText(getApplicationContext(), "올바른 ID 와 비밀번호를 입력해주세요.", Toast.LENGTH_SHORT).show();
                    ID.setText(null);
                    PWD.setText(null);
                }
                else{
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

        find_pw_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), find_pw.class);
                startActivity(intent);
            }
        });
    }
    // 앱 -> 서버 Activity - ID - PWD / 서버 -> 앱 s ( 성공 ), f ( 실패 )
    char login(final String Activity, final String Id, final String Pwd) {
        mHandler = new Handler();

        // 서버 -> 앱에서 s, f 보낼 때 아스키코드 숫자로 오기 때문에 s, f 받을 배열 만듦
        final char[] check_login = new char[1];
        Thread LOGIN = new Thread() {
            public void run() {
                try {
                    socket = new Socket(ip, port);
                    Log.w("서버 접속됨", "서버 접속됨");
                } catch (IOException e1) {
                    Log.w("서버접속못함", "서버접속못함");
                    e1.printStackTrace();
                }
                try {
                    dos = new DataOutputStream(socket.getOutputStream());
                    dis = new DataInputStream(socket.getInputStream());

                    Log.w("화면 확인 ", Activity);
                    Log.w("ID 확인 ", Id);
                    Log.w("PW 확인 ", Pwd);

                    String LoginInfo = Activity + "-" + Id + "-" + Pwd + "+";
                    dos.writeBytes(LoginInfo);

                    // 서버 -> 앱 전송 받음
                    int checked_login = dis.read();
                    // 아스키코드로 받았기 때문에 s, f 로 바꿔야 함
                    check_login[0] = (char)checked_login;
                    // 앱에서 서버에서 s, f 보냈는지 확인용 PRINT
                    System.out.println("확인"+ check_login[0]);

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
        return check_login[0];
    }
}
