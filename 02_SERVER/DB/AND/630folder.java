package com.example.ourchord_app;

import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;

import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentTransaction;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;


public class folder extends Fragment {

    public static final int DEFAULT_BUFFER_SIZE = 1048576;

    private Handler mHandler;
    private Socket socket;

    private BufferedReader networkReader;
    private PrintWriter networkWriter;

    private DataOutputStream dos = null;
    private DataInputStream dis;

    private String ip = "";            // IP 번호
    private int port = ;

    final String activity ="folder";

    public static folder newInstance() {
        return new folder();
    }

    @Override
    public void onCreate(Bundle savedInstanceState){

        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View fv = inflater.inflate(R.layout.fragment_folder, container, false);

        // 첫화면 업로드 폴더 지정
        FragmentTransaction fragmenetTransaction = getChildFragmentManager().beginTransaction();
        fragmenetTransaction.add(R.id.file_layout, new upload_folder()).commit();

        ImageButton renew = (ImageButton) fv.findViewById(R.id.renew_btn);

        Button upload_tab, midiupload_tab;

        upload_tab = (Button) fv.findViewById(R.id.upload_tab);
        upload_tab.setOnClickListener(new View.OnClickListener() {
            public void onClick(View fv){
                connect_folder(activity, 'B');
            }
        });

        midiupload_tab = (Button) fv.findViewById(R.id.midiupload_tab);
        midiupload_tab.setOnClickListener(new View.OnClickListener() {
            public void onClick(View fv){
                connect_folder(activity, 'C');
            }
        });

        return fv;
    }

    // 데이터베이스(서버) 전송
    void connect_folder(final String Activity, final char show) {
        mHandler = new Handler();
        Log.w("connect", "연결 하는중");

        //final int[] a = new int[1];
        //final char[] aa = new char[1];
        Thread FOLDER_CONFIRM = new Thread() {
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

                    //--------------------------------------
                    // input에 받을꺼 넣어짐
                    Log.w("실행 화면 확인 ", Activity);
                    System.out.println("MIDI 확인: " + show);

                    String FolderInfo = Activity + "-" + show;
                    dos.writeBytes(FolderInfo);
                    //--------------------------------------

                    //바이트 단위로 데이터를 읽는다, 외부로 부터 읽어들이는 역할을 담당
                    InputStream is = socket.getInputStream();
                    Log.d("바이트 단위로 읽었어", "읽음");
                    System.out.println(is);

                    //파일 읽기
                    BufferedInputStream bis = new BufferedInputStream(is);
                    DataInputStream dis = new DataInputStream(bis);

                    Log.d("파일 읽었어", "읽음");
                    System.out.println(bis);

                    // == client.py의 line25
                    Integer file_size = dis.read(); //버퍼 사이즈 읽기
                    System.out.println(file_size);

/*                  BufferedInputStream bis = new BufferedInputStream(socket.getInputStream());
                    DataInputStream dis = new DataInputStream(bis);

                    int filesCount = dis.readInt();  //파일 갯수 읽음  +++++++++++++++++++++++++++++++++++++++++

                    File[] files = new File[filesCount]; // 파일을 read한 것 받아 놓습니다.

                    for (int i = 0; i < filesCount; i++) {   //파일 갯수 만큼 for문 돕니다.
                        long fileLength = dis.readLong();    //파일 길이 받습니다. +++++++++++++++++++++++++++++++++++++++++
                        String fileName = dis.readUTF();     //파일 이름 받습니다. +++++++++++++++++++++++++++++++++++++++++


                        System.out.println("수신 파일 이름 : " + fileName);

                        files[i] = new File("/data/data/com.example.ourchord_app/", fileName);
                        FileOutputStream fos = new FileOutputStream(files[i]); // 지정한 폴더로 내보냄
                        BufferedOutputStream bos = new BufferedOutputStream(fos);

                        InputStream in = socket.getInputStream();

                        /*for (int j = 0; j < fileLength; j++) //파일 길이 만큼 읽습니다.
                            bos.write(bis.read());
                        bos.flush();*/

                    BufferedReader br = new BufferedReader(new InputStreamReader(is));
                    //B와 C 구분하여 디렉토리 생성
                    //result.mid는 업로드한 pdf 이름을 folder.java로 변수를 통해 받아와서 지정하기
                    //FileOutputStream output = new FileOutputStream("/data/data/com.example.ourchord_app/"+ show + "result.mid");
                    FileOutputStream output = new FileOutputStream("/data/data/com.example.ourchord_app/629.mid");
                    //System.out.println("파일 경로: " +output);
                    InputStream in = socket.getInputStream();
                    System.out.println(in);
//여기부터
                    //String str = null;
                    while((br.readLine())!=null){ //데이터 읽어와서 output 경로에 write
                        //str = br.readLine(); // for 0~ eof
                        byte[] buf = new byte[1048576];
                        //str = in.read(buf, 0, buf.length);
                        System.out.println("수신중인 파일내용: " + buf);

                        output.write(buf);
                        Log.d("line 저장완료","저장됨");
//여기까지 건너뛰네
                    }
                    br.close();
                    output.close();
                    //output.close();
                    System.out.println("수신완료");

                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼", "버퍼생성 잘못됨");
                }
                Log.w("버퍼", "버퍼생성 잘됨");
            }
        };
        FOLDER_CONFIRM.start();
        Log.w("버퍼", "check");
        try{
            FOLDER_CONFIRM.join();
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
