package com.example.ourchord_app;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import android.os.Environment;
import android.os.Handler;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import org.w3c.dom.Text;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;

public class conversion extends Fragment {

    /*private Spinner basechord;
    private Spinner conversionchord;

    String choice_base="";
    String choice_conversion="";*/

    private Handler mHandler;
    private String html = "";
    private Socket socket;

    private BufferedReader networkReader;
    private PrintWriter networkWriter;

    private DataOutputStream dos = null;
    private DataInputStream dis;

    private String ip = "13.125.160.38";            // IP 번호
    private int port = 9300;

    public static upload_folder newInstance() {
        return new upload_folder();
    }

    public conversion() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View fv = inflater.inflate(R.layout.fragment_conversion, container, false);

        /*
        Spinner spin1 = (Spinner)fv.findViewById(R.id.spinner_basechord);
        Spinner spin2 = (Spinner)fv.findViewById(R.id.spinner_changechord);
        ArrayAdapter<String> basechord = new ArrayAdapter<String>(getActivity(), android.R.layout.simple_spinner_dropdown_item);
        ArrayAdapter<String> conversionchord = new ArrayAdapter<String>(getActivity(), android.R.layout.simple_spinner_dropdown_item);

        basechord.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        basechord.setAdapter(basechord);
        spin1.setAdapter(basechord);
        spin1.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                if(basechord.getItem(i).equals("C")){
                    choice_base = "C";
                    System.out.println("C");
                }
                else if(basechord.getItem(i).equals("C#")){
                    choice_base = "C#";
                    System.out.println("C#");
                }
                else if(basechord.getItem(i).equals("D")){
                    choice_base = "D";
                    System.out.println("D");
                }
                else if(basechord.getItem(i).equals("D#")){
                    choice_base = "D#";
                    System.out.println("D#");
                }
                else if(basechord.getItem(i).equals("F")){
                    choice_base = "F";
                    System.out.println("F");
                }
                else if(basechord.getItem(i).equals("F#")){
                    choice_base = "F#";
                    System.out.println("F#");
                }
                else if(basechord.getItem(i).equals("G")){
                    choice_base = "G";
                    System.out.println("G");
                }
                else if(basechord.getItem(i).equals("G#")){
                    choice_base = "G#";
                    System.out.println("G#");
                }
                else if(basechord.getItem(i).equals("A")){
                    choice_base = "A";
                    System.out.println("A");
                }
                else if(basechord.getItem(i).equals("A#")){
                    choice_base = "A#";
                    System.out.println("A#");
                }
                else if(basechord.getItem(i).equals("B")){
                    choice_base = "B";
                    System.out.println("B");
                }
                else if(basechord.getItem(i).equals("B#")){
                    choice_base = "B#";
                    System.out.println("b#");
                }
            }
            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {

            }
        });

        conversionchord=ArrayAdapter.createFromResource(getActivity(), R.array.changechord, android.R.layout.simple_spinner_dropdown_item);
        conversionchord.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spin2.setAdapter(conversionchord);
        spin2.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
                @Override
                public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                    if(conversionchord.getItem(i).equals("C")){
                        choice_conversion = "C";
                        System.out.println("C");
                    }
                    else if(conversionchord.getItem(i).equals("C#")){
                        choice_conversion = "C#";
                        System.out.println("C#");
                    }
                    else if(conversionchord.getItem(i).equals("D")){
                        choice_conversion = "D";
                        System.out.println("D");
                    }
                    else if(conversionchord.getItem(i).equals("D#")){
                        choice_conversion = "D#";
                        System.out.println("D#");
                    }
                    else if(conversionchord.getItem(i).equals("F")){
                        choice_conversion = "F";
                        System.out.println("F");
                    }
                    else if(conversionchord.getItem(i).equals("F#")){
                        choice_conversion = "F#";
                        System.out.println("F#");
                    }
                    else if(conversionchord.getItem(i).equals("G")){
                        choice_conversion = "G";
                        System.out.println("G");
                    }
                    else if(conversionchord.getItem(i).equals("G#")){
                        choice_conversion = "G#";
                        System.out.println("G#");
                    }
                    else if(conversionchord.getItem(i).equals("A")){
                        choice_conversion = "A";
                        System.out.println("A");
                    }
                    else if(conversionchord.getItem(i).equals("A#")){
                        choice_conversion = "A#";
                        System.out.println("A#");
                    }
                    else if(conversionchord.getItem(i).equals("B")){
                        choice_conversion = "B";
                        System.out.println("B");
                    }
                    else if(conversionchord.getItem(i).equals("B#")){
                        choice_conversion = "B#";
                        System.out.println("b#");
                    }
                }

            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {

            }
        });

        final Button chord_conversion = (Button)fv.findViewById(R.id.chord_conversion_btn);
        chord_conversion.setOnClickListener(new View.OnClickListener(){
            public void onClick(View fv){
                System.out.println(choice_base);
                System.out.println(choice_conversion);
            }
        }); */
        final RadioGroup rg1 = (RadioGroup)fv.findViewById(R.id.radioGroup1);
        final RadioGroup rg2 = (RadioGroup)fv.findViewById(R.id.radioGroup2);

        Button upload_1_btn, upload_2_btn, upload_3_btn;
        upload_1_btn  = (Button) fv.findViewById(R.id.upload_1_btn);
        upload_1_btn.setOnClickListener(new View.OnClickListener(){
            public void onClick(View fv){
                System.out.println("1.pdf 변환");
                int id1 = rg1.getCheckedRadioButtonId();
                int id2 = rg2.getCheckedRadioButtonId();
                RadioButton rb1 = (RadioButton) rg1.findViewById(id1);
                RadioButton rb2 = (RadioButton) rg2.findViewById(id2);
                String base = rb1.getText().toString();
                String change = rb2.getText().toString();
                connect(base,change);
            }
        });
        upload_2_btn  = (Button) fv.findViewById(R.id.upload_2_btn);
        upload_2_btn.setOnClickListener(new View.OnClickListener(){
            public void onClick(View fv){
                System.out.println("2.pdf 변환");
                int id1 = rg1.getCheckedRadioButtonId();
                int id2 = rg2.getCheckedRadioButtonId();
                RadioButton rb1 = (RadioButton) rg1.findViewById(id1);
                RadioButton rb2 = (RadioButton) rg2.findViewById(id2);
                String base = rb1.getText().toString();
                String change = rb2.getText().toString();
                connect(base,change);
            }
        });
        upload_3_btn  = (Button) fv.findViewById(R.id.upload_3_btn);
        upload_3_btn.setOnClickListener(new View.OnClickListener(){
            public void onClick(View fv){
                int id1 = rg1.getCheckedRadioButtonId();
                int id2 = rg2.getCheckedRadioButtonId();
                RadioButton rb1 = (RadioButton) rg1.findViewById(id1);
                RadioButton rb2 = (RadioButton) rg2.findViewById(id2);
                String base = rb1.getText().toString();
                String change = rb2.getText().toString();
                System.out.println("3.pdf 변환");
                connect(base,change);
            }
        });

        final TextView tv = (TextView) fv.findViewById(R.id.output_chord_conversion);

        Button base = (Button)fv.findViewById(R.id.chord_conversion_btn);
        base.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                int id1 = rg1.getCheckedRadioButtonId();
                int id2 = rg2.getCheckedRadioButtonId();
                RadioButton rb1 = (RadioButton) rg1.findViewById(id1);
                RadioButton rb2 = (RadioButton) rg2.findViewById(id2);
                tv.setText("결과 :"+ rb1.getText().toString() + rb2.getText().toString());

                System.out.println(toString());
            }
        });
        return fv;
    }
    public static final int DEFAULT_BUFFER_SIZE = 10000;

    void connect(final String Base,final String  Change) {
        mHandler = new Handler();

        Log.w("connect", "연결 하는중");
        // 받아오는거

        Thread checkUpdate = new Thread() {
            public void run() {

                try {
                    socket = new Socket(ip, port);
                    Log.w("서버 접속됨", "서버 접속됨");
                } catch (IOException e1) {
                    Log.w("서버접속못함", "서버접속못함");
                    e1.printStackTrace();
                }

                Log.w("edit 넘어가야 할 값 : ", "안드로이드에서 서버로 연결요청");

                // Buffered가 잘못된듯.

                try {
                    dos = new DataOutputStream(socket.getOutputStream());   // output에 보낼꺼 넣음
                    dis = new DataInputStream(socket.getInputStream());     // input에 받을꺼 넣어짐
                    Log.w("base확인", Base);
                    String pdf = "b"+Base;
                    Log.w("base확인", pdf);
                    //dos.writeBytes(pdf);

                    //////테스트
                    String a = "id";
                    String b = "bbbb";
                    String c = "cccc";

                    String totalstr = a + "-" + b + "-" + c;
                    dos.writeBytes(totalstr);


                    //dos.flush();
                    /*dos.writeBytes(change);
                    dos.flush();
                    dos.writeBytes(pdf);
                    dos.flush();
                    dos.writeUTF("4.pdf");
                    dos.flush();*/

                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼", "버퍼생성 잘못됨");
                }
                Log.w("버퍼", "버퍼생성 잘됨");

                /*int i = 0;
                while(i<5){

                    try {
                        int l = dis.read();
                        Log.w("버퍼", String.valueOf(l));
                        //Log.w("버퍼", l);
                    } catch (IOException e) {
                        e.printStackTrace();
                        Log.w("버퍼", "안됨");
                    }
                    Log.w("버퍼", "실행");
                    i++;
                }*/

            }
            // }

            // 소켓 접속 시도, 버퍼생성

        };
        Thread checkUpdate2 = new Thread() {
            public void run() {


                try {
                    socket = new Socket(ip, port);
                    Log.w("서버 접속됨", "서버2 접속됨");
                } catch (IOException e1) {
                    Log.w("서버접속못함", "서버2접속못함");
                    e1.printStackTrace();
                }

                Log.w("edit 넘어가야 할 값 : ", "안드로이드에서 서버로 연결요청");

                Log.w("Change확인", Change);
                String pdf = "c" + Change;
                Log.w("Change확인", pdf);
                try {
                    dos = new DataOutputStream(socket.getOutputStream());   // output에 보낼꺼 넣음
                    dis = new DataInputStream(socket.getInputStream());     // input에 받을꺼 넣어짐

                    dos.writeBytes(pdf);
                    //dos.flush();

                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼", "버퍼생성2 잘못됨");
                }
                Log.w("버퍼", "버퍼생성2 잘됨");
            }
        };
        Thread checkUpdate3 = new Thread() {
            public void run() {


                try {
                    socket = new Socket(ip, port);
                    Log.w("서버 접속됨", "서버3 접속됨");
                } catch (IOException e1) {
                    Log.w("서버접속못함", "서버3접속못함");
                    e1.printStackTrace();
                }

                Log.w("edit 넘어가야 할 값 : ", "안드로이드에서 서버로 연결요청");


                String pdf = "12.pdf";
                try {
                    dos = new DataOutputStream(socket.getOutputStream());   // output에 보낼꺼 넣음
                    dis = new DataInputStream(socket.getInputStream());     // input에 받을꺼 넣어짐

                    dos.writeBytes(pdf);
                    //dos.flush();

                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼", "버퍼생성3 잘못됨");
                }
                Log.w("버퍼", "버퍼생성3 잘됨");
            }
        };
        checkUpdate.start();
        Log.w("버퍼", "check1 실행");
        try{
            checkUpdate.join();
        }catch (Exception e){
            e.printStackTrace();
        }
        /*checkUpdate2.start();
        Log.w("버퍼", "check2 실행");
        try{
            checkUpdate2.join();
        }catch (Exception e){
            e.printStackTrace();
        }
        checkUpdate3.start();
        try{
            checkUpdate3.join();
        }catch (Exception e){
            e.printStackTrace();
        }*/
        Log.w("버퍼", "check3 실행");
    }

}
