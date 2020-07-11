package com.example.ourchord_app;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.Toast;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.Charset;
import java.util.ArrayList;

import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;

import static com.example.ourchord_app.R.layout;

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

    private final int MY_PERMISSION_REQUEST_FILE = ;
    private final int FILE_SELECT_CODE = ;

    Uri file_path;


    public static upload_folder newInstance() {
        return new upload_folder();
    }

    public upload_folder() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {

        // 쓰기 권한 설정
        int permissionCheck_1 = ContextCompat.checkSelfPermission(getContext(), Manifest.permission.WRITE_EXTERNAL_STORAGE);
        if (permissionCheck_1 != PackageManager.PERMISSION_GRANTED) {
            Toast.makeText(getContext(), "권한 승인 필요", Toast.LENGTH_LONG).show();
            if (ActivityCompat.shouldShowRequestPermissionRationale(getActivity(), Manifest.permission.WRITE_EXTERNAL_STORAGE)) {
                Toast.makeText(getContext(), "파일 업로드를 위해 파일 권한이 필요합니다!", Toast.LENGTH_LONG).show();
            } else {
                ActivityCompat.requestPermissions(getActivity(), new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, MY_PERMISSION_REQUEST_FILE);
                Toast.makeText(getContext(), "파일 업로드 위해 파일 권한이 필요합니다.", Toast.LENGTH_LONG).show();
            }
        }
        // 읽기 권한 설정
        int permissionCheck_2 = ContextCompat.checkSelfPermission(getContext(), Manifest.permission.READ_EXTERNAL_STORAGE);
        if (permissionCheck_2 != PackageManager.PERMISSION_GRANTED) {
            Toast.makeText(getContext(), "권한 승인 필요", Toast.LENGTH_LONG).show();
            if (ActivityCompat.shouldShowRequestPermissionRationale(getActivity(), Manifest.permission.READ_EXTERNAL_STORAGE)) {
                Toast.makeText(getContext(), "파일 업로드를 위해 파일 권한이 필요합니다!", Toast.LENGTH_LONG).show();
            } else {
                ActivityCompat.requestPermissions(getActivity(), new String[]{Manifest.permission.READ_EXTERNAL_STORAGE}, MY_PERMISSION_REQUEST_FILE);
                Toast.makeText(getContext(), "파일 업로드 위해 파일 권한이 필요합니다.", Toast.LENGTH_LONG).show();
            }
        }

        final View fv = inflater.inflate(layout.fragment_upload_folder, container, false);

        // 액티비티 구분용
        final String Activity = "upload_folder";

        String nList =connect_pdf(Activity);
        System.out.println("리스트 모음 " + nList);

        String[] arrayLi = nList.split("-");

        int arrayLilen = arrayLi.length;

        // 파일 이름 추가 될 리스트
        ArrayList<String> arrayList = new ArrayList<String>();
        for(int i = 0 ; i < arrayLilen ; i++){
            arrayList.add(arrayLi[i]);
        }

        ArrayAdapter<String> Adapter;
        Adapter = new ArrayAdapter<String>(getContext(), android.R.layout.simple_list_item_1, arrayList);

        ListView listView = (ListView) fv.findViewById(R.id.file_list);
        listView.setAdapter(Adapter);
        // 다운로드 폴더에 있는거 보여주는 리스트
/*
        ListView lv = (ListView)fv.findViewById(R.id.file_list);
        File[] listfile = (new File("/sdCard/Download/pdf").listFiles());

        List<String> list = new ArrayList<String>();
        for(File file : listfile)
            list.add(file.getName());

        ArrayAdapter<String> Adapter;
        Adapter = new ArrayAdapter<String>(getContext(), android.R.layout.simple_list_item_1, list);
        lv.setAdapter(Adapter); */

        // 파일 추가 버튼
        ImageButton upload = (ImageButton) fv.findViewById(R.id.upload_btn);

        upload.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent intent = new Intent();
                intent.setType("application/pdf");
                intent.setAction(Intent.ACTION_GET_CONTENT);

                startActivityForResult(Intent.createChooser(intent, "Select a File to Upload"), FILE_SELECT_CODE);
                System.out.println("파일 선택 고고링링링롱");
                // 안드로이드 경로 저장
                String path = Environment.getExternalStorageDirectory().getAbsolutePath() + file_path;
                System.out.println("path : " + path);
            }
        });
        return fv;
    }
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (resultCode == -1 && requestCode == 1) {
            System.out.println("모야!!짜증나게하지마!!");
            file_path = data.getData();
            System.out.println("uri : " + file_path);
            System.out.println("uri : " + file_path.toString());
            String testPath = file_path.toString();
            String patharry [] = testPath.split("%2F");
            int bb = patharry.length;
            System.out.println("uri name: " + patharry[bb-1]);
            write_pdf(patharry[bb-1]);
        }
    }
    // 파일 승인 확인 용 요기에 있어야 됨
    @Override
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        String str = null;

        if (requestCode == 100) {
            // If request is cancelled, the result arrays are empty.
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(getContext(), "승인이 허가되어 있습니다.", Toast.LENGTH_LONG).show();

            } else {
                Toast.makeText(getContext(), "아직 승인받지 않았습니다.", Toast.LENGTH_LONG).show();
            }
        }
    }
    void write_pdf(final String file_path){
        mHandler = new Handler();
        Log.w("connect", "연결 하는중");

        Thread writeThread = new Thread() {
            public void run() {
                try {
                    socket = new Socket(ip, port);
                    Log.w("서버 접속됨", "서버 접속됨");
                } catch (IOException e1) {
                    Log.w("서버접속못함", "서버접속못함");
                    e1.printStackTrace();
                }
                try {
                    //File file = new File(file_path);
                    String pName = "pNmae+";
                    dos.writeBytes(pName);
                    Log.w("이름보내",file_path);
                    String chpath = file_path + "+";
                    dos.writeBytes(chpath);
                    File file = new File("/sdcard/Download/" + file_path);
                    long fileSize = file.length();
                    //String sSize = Long.toString(fileSize) + "bytes";
                    //dos.writeBytes(sSize);
                    FileInputStream fis = new FileInputStream(file);

                    BufferedInputStream br = new BufferedInputStream(fis);
                    Log.w("파일내", "시");
                    int len;
                    int size = 4096;
                    byte[] data = new byte[size];
                    //String testtxt = "test";

                    while((len = br.read(data))!=-1){
                        //char test = (char)len;
                        //System.out.println("읽" + test);
                        dos.write(data,0,len);
                        //dos.writeBytes(testtxt);
                    }
                    String checkpoint = "+";
                    dos.writeBytes(checkpoint);
                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼", "버퍼생성 잘못됨");
                }
                Log.w("버퍼", "버퍼생성 잘됨");
            }
        };
        writeThread.start();
        Log.w("버퍼", "check");
        try{
            writeThread.join();
        }catch (Exception e){
            e.printStackTrace();
        }
    }
    // 서버 전송
    String connect_pdf(final String Activity) {
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
                    ByteBuffer dd = ByteBuffer.wrap(data);
                    Charset charset = Charset.forName("UTF-8");
                    //String ttt = charset.decode(b).toString();
                    //System.out.println("test 확인용 : " + ttt);
                    dd.order(ByteOrder.LITTLE_ENDIAN);
                    int len1 = dd.getInt();
                    len1 = 30;
                    //System.out.println("test 확인  : " + len1);
                    byte[] data2 = new byte[len1];
                    dis.read(data2, 0, len1);

                    String msg = new String(data2, "UTF-8");
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