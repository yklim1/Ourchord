package com.example.ourchord_app;

import android.app.ProgressDialog;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.Spinner;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;

import androidx.fragment.app.Fragment;

public class conversion extends Fragment {

    private Handler mHandler;
    private Socket socket;

    private BufferedReader networkReader;
    private PrintWriter networkWriter;

    private DataOutputStream dos = null;
    private DataInputStream dis;

    private String ip = "IP주소";
    private int port = 9300;
    String base = "";
    String change  = "";

    common UserInfo = new common();
    common FileList = new common();

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View con_activity = inflater.inflate(R.layout.fragment_conversion, container, false);
        final Button conversion = (Button)con_activity.findViewById(R.id.chord_conversion_btn);

        final String activity = "conversion";

        // 기존 코드 선택
        final CheckBox base_c, base_cup, base_d, base_dup, base_e, base_f, base_fup, base_g, base_gup, base_a, base_aup, base_b, base_bup;
        base_c = (CheckBox)con_activity.findViewById(R.id.C);
        base_cup = (CheckBox)con_activity.findViewById(R.id.Cup);
        base_d = (CheckBox)con_activity.findViewById(R.id.D);
        base_dup = (CheckBox)con_activity.findViewById(R.id.Dup);
        base_e = (CheckBox)con_activity.findViewById(R.id.E);
        base_f = (CheckBox)con_activity.findViewById(R.id.F);
        base_fup = (CheckBox)con_activity.findViewById(R.id.Fup);
        base_g = (CheckBox)con_activity.findViewById(R.id.G);
        base_gup = (CheckBox)con_activity.findViewById(R.id.Gup);
        base_a = (CheckBox)con_activity.findViewById(R.id.A);
        base_aup = (CheckBox)con_activity.findViewById(R.id.Aup);
        base_b = (CheckBox)con_activity.findViewById(R.id.B);
        base_bup = (CheckBox)con_activity.findViewById(R.id.Bup);

        // 변환할 코드 선택
        final CheckBox change_c, change_cup, change_d, change_dup, change_e, change_f, change_fup, change_g, change_gup, change_a, change_aup, change_b, change_bup;
        change_c = (CheckBox)con_activity.findViewById(R.id.cC);
        change_cup = (CheckBox)con_activity.findViewById(R.id.cCup);
        change_d = (CheckBox)con_activity.findViewById(R.id.cD);
        change_dup = (CheckBox)con_activity.findViewById(R.id.cDup);
        change_e = (CheckBox)con_activity.findViewById(R.id.cE);
        change_f = (CheckBox)con_activity.findViewById(R.id.cF);
        change_fup = (CheckBox)con_activity.findViewById(R.id.cFup);
        change_g = (CheckBox)con_activity.findViewById(R.id.cG);
        change_gup = (CheckBox)con_activity.findViewById(R.id.cGup);
        change_a = (CheckBox)con_activity.findViewById(R.id.cA);
        change_aup = (CheckBox)con_activity.findViewById(R.id.cAup);
        change_b = (CheckBox)con_activity.findViewById(R.id.cB);
        change_bup = (CheckBox)con_activity.findViewById(R.id.cBup);

        Spinner file_name_spinner = (Spinner)con_activity.findViewById(R.id.conviersion_sheet);
        ArrayAdapter<String> share_pdf_file_name = new ArrayAdapter<>(getContext(), android.R.layout.simple_list_item_1);

        final String[] pdf = {"스피너"};

        // 입력한 파일 선택 스피너
        final String[] select_file_list = FileList.Get_file_list();
        Spinner filespinner = (Spinner)con_activity.findViewById(R.id.conviersion_sheet);
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(getContext(), android.R.layout.simple_list_item_1, select_file_list);
        filespinner.setAdapter(adapter);
        filespinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long id) {
                pdf[0] = select_file_list[i];
                System.out.println("파일 이름 확인 : " + pdf[0]);
            }
            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {
            }
        });

        conversion.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (base_c.isChecked()) base += base_c.getText().toString();
                if (base_cup.isChecked()) base += base_cup.getText().toString();
                if (base_d.isChecked()) base += base_d.getText().toString();
                if (base_dup.isChecked()) base += base_dup.getText().toString();
                if (base_e.isChecked()) base += base_e.getText().toString();
                if (base_f.isChecked()) base += base_f.getText().toString();
                if (base_fup.isChecked()) base += base_fup.getText().toString();
                if (base_g.isChecked()) base += base_g.getText().toString();
                if (base_gup.isChecked()) base += base_gup.getText().toString();
                if (base_a.isChecked()) base += base_a.getText().toString();
                if (base_aup.isChecked()) base += base_aup.getText().toString();
                if (base_b.isChecked()) base += base_b.getText().toString();
                if (base_bup.isChecked()) base += base_bup.getText().toString();

                if (change_c.isChecked()) change += change_c.getText().toString();
                if (change_cup.isChecked()) change += change_cup.getText().toString();
                if (change_d.isChecked()) change += change_d.getText().toString();
                if (change_dup.isChecked()) change += change_dup.getText().toString();
                if (change_e.isChecked()) change += change_e.getText().toString();
                if (change_f.isChecked()) change += change_f.getText().toString();
                if (change_fup.isChecked()) change += change_fup.getText().toString();
                if (change_g.isChecked()) change += change_g.getText().toString();
                if (change_gup.isChecked()) change += change_gup.getText().toString();
                if (change_a.isChecked()) change += change_a.getText().toString();
                if (change_aup.isChecked()) change += change_aup.getText().toString();
                if (change_b.isChecked()) change += change_b.getText().toString();
                if (change_bup.isChecked()) change += change_bup.getText().toString();

                //조 변환 진행 중 알림
                new android.os.Handler().postDelayed(new Runnable() {
                    @Override
                    public void run() {
                            final ProgressDialog conversioning = new ProgressDialog(getContext());
                            conversioning.setIndeterminate(true);
                            conversioning.setMessage("조 변환 진행 중입니다.                 잠시만 기다려주세요!");
                            conversioning.show();
                    }
                }, 1);

                conversion(activity, base, change, pdf[0]);


                System.out.println("조변환 정보 : " + base + "+" + change + "+" + pdf[0]);
            }
        });
        return con_activity;
    }

    public static final int DEFAULT_BUFFER_SIZE = 10000;

    void conversion(final String Activity, final String Base, final String Change, final String Pdf) {
        mHandler = new Handler();
        Log.w("connect", "연결 하는중");
        System.out.println("파일 이름 확인 : " + Pdf);
        Thread checkUpdate = new Thread() {
            public void run() {
                //socket = new Socket(ip, port);
                try {
                    socket = new Socket(ip, port);
                    Log.w("서버 접속됨", "서버 접속됨");
                } catch (IOException e1) {
                    Log.w("서버접속못함", "서버접속못함");
                    e1.printStackTrace();
                }

                Log.w("서버 접속됨", "서버 접속됨");
                try {
                    dos = new DataOutputStream(socket.getOutputStream());   // output에 보낼꺼 넣음
                    dis = new DataInputStream(socket.getInputStream());

                    // input에 받을꺼 넣어짐
                    Log.w("Activity 확인", Activity);
                    Log.w("기존 코드 확인", Base);
                    Log.w("변환 코드 확인", Change);
                    Log.w("PDF 파일 확인", Pdf);

                    String ConversionInfo = Activity + "-" + UserInfo.GetUser_id() + "-" + Pdf + "-" + Base + "-" + Change + "+";
                    dos.writeBytes(ConversionInfo);
                    System.out.println("Conversion:" + ConversionInfo);

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
