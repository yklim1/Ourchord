package com.example.ourchord_app;

import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;

import androidx.fragment.app.Fragment;

public class midiupload_folder extends Fragment {

    private Handler mHandler;
    private Socket socket;

    private BufferedReader networkReader;
    private PrintWriter networkWriter;

    private DataOutputStream dos = null;
    private DataInputStream dis;

    private String ip = "IP주소";            // IP 번호
    private int port = 9300;

    public static midiupload_folder newInstance(){
        return new midiupload_folder();
    }

    public midiupload_folder() {
        // Required empty public constructor
    }

    Uri file_name;

    common UserInfo = new common();
    common MidiFile = new common();

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View mi_folder = inflater.inflate(R.layout.fragment_midiupload_folder, container, false);

        final String activity = "midiupload_folder";
        final String seperate = "sendto_eamil";
        String User_Id = UserInfo.GetUser_id();

        String midiList = connect_midi(activity, User_Id);
        final String[] server_output_midi = midiList.split("-");
        System.out.println("server  :  "  +  server_output_midi);
        System.out.println("server len :  "  +  server_output_midi[1]);
        int midilist_len = server_output_midi.length;
        System.out.println("server len :  "  +  midilist_len);
        String[] teststr = server_output_midi[midilist_len-1].split(".mid");
        String resu = teststr[0] + ".mid";
        server_output_midi[midilist_len-1] = resu;
        System.out.println("server len :  "  +  server_output_midi[midilist_len-1]);
        MidiFile.Set_midi_list(server_output_midi);

        ArrayList<String> arrayList = new ArrayList<String>();
        for(int i = 0 ; i < midilist_len ; i++){
            arrayList.add(server_output_midi[i]);
        }

        ArrayAdapter<String> Adapter;
        Adapter = new ArrayAdapter<String>(getContext(), android.R.layout.simple_list_item_1, arrayList);

        ListView listView = (ListView) mi_folder.findViewById(R.id.midi_file_list);
        listView.setAdapter(Adapter);

        // 리스트 클릭하면 미디 파일 이메일 전송
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                Send_Email(seperate, UserInfo.GetUser_id(), server_output_midi[i]);
            }
        });
        return mi_folder;
    }

    String connect_midi(final String Activity, final String User_id) {
        mHandler = new Handler();
        Log.w("connect", "연결 하는중");
        final String[] update_midi_list = new String[1];
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
                    dos = new DataOutputStream(socket.getOutputStream());
                    dis = new DataInputStream(socket.getInputStream());

                    // input에 받을꺼 넣어짐
                    Log.w("Activity 확인", Activity);

                    String checkpoint = "+";
                    String PDFInfo = Activity + "-" + UserInfo.GetUser_id() + "-" + checkpoint;
                    dos.writeBytes(PDFInfo);

                    int file_len = 70;
                    byte[] data3 =  new  byte[file_len];
                    dis.read(data3,  0, file_len);

                    String msg =new String(data3, "UTF-8");
                    System.out.println("msg  :  "  + msg);
                    update_midi_list[0] = msg;

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
        return update_midi_list[0];
    }

    // 미디 파일 이메일 전송
    void Send_Email(String Seperate, String User_id, final String file_name) {
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
                    dos = new DataOutputStream(socket.getOutputStream());
                    dis = new DataInputStream(socket.getInputStream());

                    // input에 받을꺼 넣어짐
                    String checkpoint = "+";
                    String Emailsend = "sendto_email-" + UserInfo.GetUser_id() + "-" + file_name + checkpoint;
                    dos.writeBytes(Emailsend);
                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼", "버퍼생성 잘못됨");
                }
                Log.w("버퍼", "버퍼생성 잘됨");
            }
        };
        checkUpdate.start();
        Log.w("버퍼", "check");
        try {
            checkUpdate.join();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}