package com.example.ourchord_app;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;

import androidx.appcompat.app.AppCompatActivity;

public class register extends AppCompatActivity {

    private Handler mHandler;
    private Socket socket;

    private BufferedReader networkReader;
    private PrintWriter networkWriter;

    private DataOutputStream dos = null;
    private DataInputStream dis;

    private String ip = "IP주소";            // IP 번호
    private int port = 9300;

    common UserInfo = new common();

    private String EmailVal = "^[_A-Za-z0-9-]+(\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})$";
    //private String PwdVal = "^.*?=^.{8, 16}$)(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$%^&+=]).*$";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        // 회원가입 입력
        final EditText NAME, ID, PWD, PWD_CHECK, EMAIL, AUTH;
        NAME = (EditText)findViewById(R.id.input_name);
        ID = (EditText)findViewById(R.id.input_id);
        PWD = (EditText)findViewById(R.id.input_pw);
        PWD_CHECK = (EditText)findViewById(R.id.input_pw_check);
        EMAIL = (EditText)findViewById(R.id.input_email);

        final String pwd_check = PWD_CHECK.getText().toString();
        final String complete = "register";
        final String Idcheck = "id_check";

        // 중복 확인, 비밀번호 정규 표현식, 비밀번호 확인, 회원가입 버튼
        Button double_btn, email_btn, email_check_btn, register_btn;
        double_btn = (Button)findViewById(R.id.checkid_btn);
        register_btn = (Button)findViewById(R.id.joinin_btn);

        final TextView pwd_reg, pwd_equal;
        pwd_reg = (TextView)findViewById(R.id.pw_check);
        pwd_equal = (TextView)findViewById(R.id.pw_correct_check);

        // 중복 확인 버튼 -> 데이터 베이스 확인 필요
        double_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String Id = ID.getText().toString();

                System.out.println("사용자 입력한 아이디 중복 확인 위해 전송" + Id);

                connect_id_check(Idcheck, Id);
            }
        });

        String Pwd = PWD.getText().toString();
        /* 비밀번호 특수문자, 영어, 8~16
        if(!Pattern.matches("^(?=.*\\d)(?=.*[~`!@#$%^&*()-])(?=.*[a-zA-Z]).{8,16}$", Pwd)){
            //pwd_reg.setTextColor(Integer.parseInt("#F9688C"));
        } */
        if(PWD_CHECK.getText().toString().length() != 0){
            Toast.makeText(register.this, "비밀번호 확인을 입력해주세요.", Toast.LENGTH_SHORT).show();
            PWD_CHECK.requestFocus();
            return;
        }
        // 비밀번호, 비밀번호 확인 일치
        if(PWD_CHECK.getText().toString().equals(PWD.getText().toString())){
            pwd_equal.setText("일치");
            return;
        }
        // 비밀번호, 비밀번호 확인 불일치
        if(!PWD_CHECK.getText().toString().equals(PWD.getText().toString())){
            pwd_equal.setText("불일치");
            PWD_CHECK.setText("");
            PWD_CHECK.requestFocus();
        }

        // 회원가입 버튼 클릭
        register_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
            System.out.println("회원가입 입력 정보 전송");

            // 모두 입력해야 함!
            if(NAME.getText().toString().length() == 0){
                Toast.makeText(register.this, "이름을 입력해주세요.", Toast.LENGTH_SHORT).show();
                NAME.requestFocus();
                return;
            }
            if(ID.getText().toString().length() == 0){
                Toast.makeText(register.this, "ID를 입력해주세요.", Toast.LENGTH_SHORT).show();
                ID.requestFocus();
                return;
            }
            if(PWD.getText().toString().length() == 0){
                Toast.makeText(register.this, "비밀번호를 입력해주세요.", Toast.LENGTH_SHORT).show();
                PWD.requestFocus();
                return;
            }
            if(EMAIL.getText().toString().length() == 0){
                Toast.makeText(register.this, "E-MAIL을 입력해주세요.", Toast.LENGTH_SHORT).show();
                EMAIL.requestFocus();
                return;
            }
            String Name = NAME.getText().toString();
            String Id = ID.getText().toString();
            String Pwd = PWD.getText().toString();
            String Email = EMAIL.getText().toString();

            // 모든 경우 통과하면 회원 가입 완료 페이지로 이동
            register(complete, Name, Id, Pwd, Email);
            Intent intent = new Intent(getApplicationContext(), register_complete.class);
            startActivity(intent);
            }
        });
    }

    public static final int DEFAULT_BUFFER_SIZE = 10000;

    // 중복 확인
    void connect_id_check(final String idcheck_click, final String id){
        mHandler = new Handler();
        Thread CHECKID = new Thread(){
            public void run(){
                try {
                    socket = new Socket(ip, port);
                    Log.w("서버 접속됨", "서버 접속됨");
                } catch (IOException e1) {
                    Log.w("서버접속못함", "서버 접속 못함");
                    e1.printStackTrace();
                }
                try {
                    dos = new DataOutputStream(socket.getOutputStream());   // output에 보낼꺼 넣음
                    dis = new DataInputStream(socket.getInputStream());

                    // input에 받을꺼 넣어짐
                    Log.w("Activity 확인 ", idcheck_click);
                    Log.w("ID 확인 ", id);
                    String checkpoint = "+";

                    String IDCheck = idcheck_click + "-" + id;
                    dos.writeBytes(IDCheck);
                    dos.writeBytes(checkpoint);

                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼", "버퍼생성 잘못됨");
                }
                Log.w("버퍼", "버퍼생성 잘됨");
            }
        };
        CHECKID.start();
        Log.w("버퍼", "check");
        try{
            CHECKID.join();
        }catch (Exception e){
            e.printStackTrace();
        }
    }

    // 데이터베이스(서버) 전송
    void register(final String Complete, final String Name, final String Id, final String Pwd, final String Email) {
        mHandler = new Handler();
        Log.w("connect", "연결 하는중");

        Thread REGISTER = new Thread() {
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
                    Log.w("화면 확인 ", Complete);
                    Log.w("이름 확인 ", Name);
                    Log.w("ID 확인 ", Id);
                    Log.w("PW 확인 ", Pwd);
                    Log.w("Eamil 확인  ", Email);
                    String checkpoint = "+";

                    String RegisterInfo = Complete + "-" + Name + "-" + Id + "-" + Pwd + "-" + Email + checkpoint;
                    dos.writeBytes(RegisterInfo);

                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼", "버퍼생성 잘못됨");
                }
                Log.w("버퍼", "버퍼생성 잘됨");
            }
        };
        REGISTER.start();
        Log.w("버퍼", "check");
        try{
            REGISTER.join();
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
