package com.example.ourchord_app;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;

public class loading extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_loading);

        Handler load_handler = new Handler();
        load_handler.postDelayed(new loadinghandler(), 3000);
    }
    private class loadinghandler implements Runnable
    {
        public void run()
        {
            startActivity(new Intent(getApplication(), login.class));
            loading.this.finish();
        }
    }
}
