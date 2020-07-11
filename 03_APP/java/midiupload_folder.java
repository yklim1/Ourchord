package com.example.ourchord_app;

import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.Charset;
import java.util.ArrayList;

import androidx.fragment.app.Fragment;

public class midiupload_folder extends Fragment {

    private Handler mHandler;
    private Socket socket;

    private BufferedReader networkReader;
    private PrintWriter networkWriter;

    private DataOutputStream dos = null;
    private DataInputStream dis;

    private String ip = "";            // IP 번호
    private int port = ;

    public static midiupload_folder newInstance(){
        return new midiupload_folder();
    }

    public midiupload_folder() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View fv = inflater.inflate(R.layout.fragment_midiupload_folder, container, false);

        final String activity = "midiupload_folder";

        //connect_midi(activity);
        String midiList =connect_midi(activity);
        System.out.println("리스트 모음 " + midiList);

        String[] arrayLi = midiList.split("-");

        int arrayLilen = arrayLi.length;

        // 파일 이름 추가 될 리스트
        ArrayList<String> arrayList = new ArrayList<String>();
        for(int i = 0 ; i < arrayLilen ; i++){
            arrayList.add(arrayLi[i]);
        }

        ArrayAdapter<String> Adapter;
        Adapter = new ArrayAdapter<String>(getContext(), android.R.layout.simple_list_item_1, arrayList);

        ListView listView = (ListView) fv.findViewById(R.id.midi_file_list);
        listView.setAdapter(Adapter);

        return fv;
    }
    String connect_midi(final String Activity) {
        mHandler = new Handler();
        Log.w("connect", "연결 하는중");
        final String[] fList = new String[1];
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
                    //InputStream receiver = socket.getInputStream();

                    // input에 받을꺼 넣어짐
                    Log.w("Activity 확인", Activity);
                    String checkpoint = "+";
                    String PDFInfo = Activity;
                    dos.writeBytes(PDFInfo);
                    dos.writeBytes(checkpoint);

                    String file_list = "";
                    byte[] data = new byte[4];
                    //ByteBuffer b = ByteBuffer.allocate(5);
                    //b.order(ByteOrder.LITTLE_ENDIAN);
                    //b.putInt(file_list.length());

                    dis.read(data, 0, 4);
                    //System.out.println("test 확인 : " + data);
                    ByteBuffer bb = ByteBuffer.wrap(data);
                    Charset charset = Charset.forName("UTF-8");
                    //String ttt = charset.decode(b).toString();
                    //System.out.println("test 확인용 : " + ttt);
                    bb.order(ByteOrder.LITTLE_ENDIAN);
                    int len123 = bb.getInt();
                    len123 = 255;
                    System.out.println("test 확인  : " + len123);
                    byte[] data3 = new byte[len123];

                    dis.read(data3, 0, len123);
                    //byte[] data4 = new byte[len123];

                    String msg = new String(data3, "UTF-8");
                    System.out.println("msg : " + msg);
                    fList[0] = msg;

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
        }catch (Exception e) {
            e.printStackTrace();
        }
        return fList[0];
    }
}
