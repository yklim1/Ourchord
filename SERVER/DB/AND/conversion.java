#conversion.java에서 mid송수신 test
package com.example.ourchord_app;

import android.content.Context;
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

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class conversion extends Fragment {

    private Handler mHandler;
    private String html = "";
    private Socket socket;

    private BufferedReader networkReader;
    private PrintWriter networkWriter;

    private DataOutputStream dos = null;
    private DataInputStream dis;

    private String ip = "";            // IP 번호
    private int port = ;

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

        Button upload_1_btn;
        upload_1_btn  = (Button) fv.findViewById(R.id.upload_1_btn);
        upload_1_btn.setOnClickListener(new View.OnClickListener(){
            public void onClick(View fv){
                System.out.println("1.pdf 변환");
                String mid = "12.mid"; ///위치: home/ec2-user/Ourchord/MIDI
                connect(mid);
            }
        });

        final TextView tv = (TextView) fv.findViewById(R.id.output_chord_conversion);

        Button base = (Button)fv.findViewById(R.id.chord_conversion_btn);
        return fv;
    }
    //size수정
    public static final int DEFAULT_BUFFER_SIZE = 1048576;

    void connect(final String Mid) { //String Mid에 12.mid
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

                try {
                    /*InputStream in = socket.getInputStream();
                    Log.d("바이트 단위로 읽었어", "읽음");
                    System.out.println(in);

                    BufferedInputStream bis = new BufferedInputStream(in);
                    Log.d("파일 읽었어", "읽음");
                    System.out.println(bis);*/
                    BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                    //한줄
                    String str = in.readLine();
                    //while(str!=null){
                        //Scanner scan = new Scanner(in);
                        System.out.println("수신중인 파일이름: " +str);
                    //}
                    //File f = new File("C:/file", "12.mid");
                    FileOutputStream output = new FileOutputStream("C://file//12.mid");
                    byte[] buf = new byte[1048576];
                    output.write(buf);
                    /*int readBytes;

                    while((readBytes = socket.getInputStream().read(buf))!=-1){
                        //output.write(buf,0,readBytes);
                        output.write(buf);
                    }*/

                    in.close();
                    output.close();
                    System.out.println(str+"수신완료");

                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼", "버퍼생성 잘못됨");
                }
                Log.w("버퍼", "버퍼생성 잘됨");

            }
        };
        checkUpdate.start();
        try{
            checkUpdate.join();
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
