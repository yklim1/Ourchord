package com.example.ourchord_app;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.Toast;

import java.io.File;

import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;

import static com.example.ourchord_app.R.layout;

public class upload_folder extends Fragment  {
   
    private final int MY_PERMISSION_REQUEST_FILE = 1001;

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

        View fv = inflater.inflate(layout.fragment_upload_folder, container, false);

        ImageButton upload = (ImageButton)fv.findViewById(R.id.upload_btn);

        upload.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent();
                intent.setAction(android.content.Intent.ACTION_VIEW);

                String _strPath = "";
                String _strFileName = "";

                File file = new  File(_strPath +  "/" + _strFileName);

                if(_strFileName.endsWith("pdf")){
                    intent.setDataAndType(Uri.fromFile(file), "applicaion/pdf");
                }
                startActivity(intent);
            }
        });
        return fv;
    }
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        switch (requestCode) {
            case MY_PERMISSION_REQUEST_FILE: {
                // If request is cancelled, the result arrays are empty.
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    Toast.makeText(getContext(), "승인이 허가되어 있습니다.", Toast.LENGTH_LONG).show();

                } else {
                    Toast.makeText(getContext(), "아직 승인받지 않았습니다.", Toast.LENGTH_LONG).show();
                }
            }
        }
    }
}