package com.example.ourchord_app;

import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
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

    private String ip = "";            // IP 번호
    private int port = ;
    String base, change;
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View fv = inflater.inflate(R.layout.fragment_conversion, container, false);

        Button conversion = (Button)fv.findViewById(R.id.chord_conversion_btn);

        final String activity = "conversion";
        
        final String[] pdf = {"예제임 스피너 완성되면 바꾸기"};

        // 파일 나오도록 수정해야함...
        final String[] file_demo = {"9.pdf", "oldday_oldnight.pdf", "aroha.pdf", "gift.pdf"};
        Spinner filespinner = (Spinner)fv.findViewById(R.id.conviersion_sheet);
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(getContext(), android.R.layout.simple_list_item_1, file_demo);
        filespinner.setAdapter(adapter);
        filespinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long id) {
                pdf[0] = file_demo[i];
                System.out.println("파일 이름 확인 : " + pdf[0]);
            }

            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {

            }
        });

        conversion.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                base = "C";
                change = "D";
                conversion(activity, base, change, pdf[0]);


                // Toast.makeText(getContext(),base + "코드 에서" + change + "코드로 조 변환 완료 되었습니다.", Toast.LENGTH_SHORT).show();
            }
        });
        return fv;
    }

    public static final int DEFAULT_BUFFER_SIZE = 10000;

    void conversion(final String Activity, final String Base, final String Change, final String Pdf) {
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

                    // input에 받을꺼 넣어짐
                    Log.w("Activity 확인", Activity);
                    Log.w("기존 코드 확인", Base);
                    Log.w("변환 코드 확인", Change);
                    Log.w("PDF 파일 확인", Pdf);

                    String ConversionInfo = Activity + "-" + Base + "-" + Change + "-" + Pdf + "+";
                    dos.writeBytes(ConversionInfo);
                    System.out.println("Conversion:" +ConversionInfo);

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
