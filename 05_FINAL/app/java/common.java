package com.example.ourchord_app;

public class common {
    private static String user_id = "";
    private static String[] pdf_file_list = {};
    private static String[] midi_file_list =  {};

    public static String GetUser_id(){
        return user_id;
    }
    public static void SetUser_id(String user_input_id){
        user_id = user_input_id;
    }
    public static String[] Get_file_list(){
        return pdf_file_list;
    }
    public static void Set_file_list(String[] user_input_pdf){
        pdf_file_list = user_input_pdf;
    }
    public static String[] Get_midi_list(){
        return  midi_file_list;
    }
    public static void Set_midi_list(String[] create_midi){
        midi_file_list = create_midi;
    }
}

