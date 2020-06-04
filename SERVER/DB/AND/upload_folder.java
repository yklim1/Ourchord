//기존 upload_folder.java에서 mid송수신 test 작업
package com.example.ourchord_app;

import android.app.DownloadManager;
import android.content.DialogInterface;
import android.graphics.Color;
import android.os.Bundle;

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
import android.widget.EditText;
import android.widget.GridView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.Toolbar;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;

import static com.example.ourchord_app.R.*;

public class upload_folder extends Fragment {

    private Handler mHandler;
    private String html = "";
    private Socket socket;

    private BufferedReader networkReader;
    private PrintWriter networkWriter;

    private DataOutputStream dos;
    private DataInputStream dis;

    private String ip = "";            // IP 번호
    private int port = ;

    public static upload_folder newInstance() {
        return new upload_folder();
    }

    public upload_folder() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View fv = inflater.inflate(layout.fragment_upload_folder, container, false);

        Button upload_1_btn, upload_2_btn, upload_3_btn;
        upload_1_btn  = (Button) fv.findViewById(id.upload_1_btn);
        upload_1_btn.setOnClickListener(new View.OnClickListener(){
            public void onClick(View fv){
                System.out.println("1.pdf 변환");
                connect();
            }
        });

        return fv;
    }
    void connect(){
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

                    while((readBytes =socket.getInputStream().read(buf))!=-1){
                        //output.write(buf,0,readBytes);
                        output.write(buf);
                    }*/

                    in.close();
                    output.close();
                    System.out.println(str+"수신완료");

                    /*dos = new DataOutputStream(socket.getOutputStream());   // output에 보낼꺼 넣음
                    dis = new DataInputStream(socket.getInputStream());     // input에 받을꺼 넣어짐
                    Log.d("Mid확인", Mid);*/

                    /*BufferedInputStream bis = new BufferedInputStream(socket.getInputStream());
                    DataInputStream dis = new DataInputStream(bis);*/
                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼", "버퍼생성 잘못됨");
                }
                Log.w("버퍼", "버퍼생성 잘됨");

                }
            };
        }
    }
