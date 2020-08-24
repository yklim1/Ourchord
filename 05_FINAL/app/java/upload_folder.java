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
import java.util.ArrayList;

import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;

import static com.example.ourchord_app.R.layout;

public class upload_folder extends Fragment {

    common UserInfo = new common();
    common FileList = new common();

    private Handler mHandler;
    private String html = "";
    private Socket socket;

    private BufferedReader networkReader;
    private PrintWriter networkWriter;

    private DataOutputStream dos;
    private DataInputStream dis;

    private String ip = "IP주소";            // IP 번호
    private int port = 9300;

    private final int MY_PERMISSION_REQUEST_FILE = 1001;
    private final int FILE_SELECT_CODE = 1;

    private String update_pdf_list_name;
    public String getUpdate_pdf_list_name(){
        return update_pdf_list_name;
    }
    public void setUpdate_pdf_list_name(){
        this.update_pdf_list_name = update_pdf_list_name;
    }

    ArrayAdapter<String> Adapter;

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
            //Toast.makeText(getContext(), "권한 승인 필요", Toast.LENGTH_LONG).show();
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
            //Toast.makeText(getContext(), "권한 승인 필요", Toast.LENGTH_LONG).show();
            if (ActivityCompat.shouldShowRequestPermissionRationale(getActivity(), Manifest.permission.READ_EXTERNAL_STORAGE)) {
                //Toast.makeText(getContext(), "파일 업로드를 위해 파일 권한이 필요합니다!", Toast.LENGTH_LONG).show();
            } else {
                ActivityCompat.requestPermissions(getActivity(), new String[]{Manifest.permission.READ_EXTERNAL_STORAGE}, MY_PERMISSION_REQUEST_FILE);
                //Toast.makeText(getContext(), "파일 업로드 위해 파일 권한이 필요합니다.", Toast.LENGTH_LONG).show();
            }
        }
        // 프래그먼트라 보여줄 액티비티 설정
        final View up_folder = inflater.inflate(layout.fragment_upload_folder, container, false);

        // 서버 전송용 정보
        final String Activity = "upload_folder";
        String User_Id = UserInfo.GetUser_id();

        // 파일 추가 버튼
        ImageButton upload = (ImageButton) up_folder.findViewById(R.id.upload_btn);
        upload.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent();
                intent.setType("application/pdf");
                intent.setAction(Intent.ACTION_GET_CONTENT);

                startActivityForResult(Intent.createChooser(intent, "Select a File to Upload"), FILE_SELECT_CODE);
                // 안드로이드 경로 저장
                String path = Environment.getExternalStorageDirectory().getAbsolutePath() + file_path;
                System.out.println("경로"+path);
            }
        });

        // - 으로 파일 구분, 사용자가 입력할 PDF 파일
        String pdf_list = connect_pdf(Activity, User_Id);
        String[] user_input_pdf = pdf_list.split("-");
        FileList.Set_file_list(user_input_pdf);
        int pdf_list_len = user_input_pdf.length;

        // 파일 이름 추가 될 리스트
        ArrayList<String> arrayList = new ArrayList<String>();
        for(int i = 0 ; i < pdf_list_len ; i++){
            arrayList.add(user_input_pdf[i]);
        }

        // 파일 이름 추가 된 리스트
        ArrayAdapter<String> Adapter;
        Adapter = new ArrayAdapter<String>(getContext(), android.R.layout.simple_list_item_1, arrayList);

        ListView pdf_file_name_list = (ListView) up_folder.findViewById(R.id.file_list);
        pdf_file_name_list.setAdapter(Adapter);

        return up_folder;
    }

    // 파일 선택해서 경로 받는 부분
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (resultCode == -1 && requestCode == 1) {
            file_path = data.getData();

            // 파일 - 으로 구분 용
            String user_input_file_path = file_path.toString();
            String user_input_file_path_arr[] = user_input_file_path.split("%2F");

            // - 으로 구분 된 파일 경로 길이
            int cut = user_input_file_path_arr.length;
            write_pdf(user_input_file_path_arr[cut-1]);
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

    // 서버에 저장 된 파일 앱에 배열로 전송용
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
                    dos = new DataOutputStream(socket.getOutputStream());   // output에 보낼꺼 넣음
                    dis = new DataInputStream(socket.getInputStream());

                    String file_list_name = "pName-";
                    dos.writeBytes(file_list_name);

                    String user_id = UserInfo.GetUser_id()+"-";
                    dos.writeBytes(user_id);

                    // 사용자가 추가한 파일 추가됨
                    String update_file_list_name =  file_path + "+";
                    System.out.println("file : "+ update_file_list_name);
                    dos.writeBytes(update_file_list_name);
                    File file = new File("/저장선택경로/" + file_path);

                    FileInputStream fis = new FileInputStream(file);
                    BufferedInputStream br = new BufferedInputStream(fis);

                    // 파일 길이 확인, 최대 받을 수 있는 크기
                    int file_len;
                    int size = 4096;
                    byte[] p_s_a_data = new byte[size];

                    // 파일 보내주기 확인
                    while((file_len = br.read(p_s_a_data))!=-1){
                        dos.write(p_s_a_data,0, file_len);
                        System.out.println("파일보내기");
                    }
                    String checkpoint = "+";
                    System.out.println("체크포인트보내기");
                    dos.writeBytes(checkpoint);
                    System.out.println("체크포인트보내기완료");
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
            //e.printStackTrace();
        }
    }

    // 앱에서 서버로 전송한 파일
    String connect_pdf(final String Activity, final String User_id) {
        mHandler = new Handler();
        Log.w("connect", "연결 하는중");
        final String[] update_pdf_list = new String[1];
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
                    String checkpoint = "+";
                    String PDFInfo = Activity;
                    String input_id = User_id;
                    String uploadInfo = Activity +  "-" + User_id;
                    dos.writeBytes(uploadInfo);
                    dos.writeBytes(checkpoint);

                    // 파일 이름 최대 길이 설정
                    int pdf_len = 70;
                    byte[] p_a_s_data = new byte[pdf_len];
                    dis.read(p_a_s_data, 0, pdf_len);

                    update_pdf_list_name = new String(p_a_s_data, "UTF-8");
                    System.out.println("pdf-list : " + update_pdf_list_name);
                    update_pdf_list[0] = update_pdf_list_name;

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
        return update_pdf_list[0];
    }
}
