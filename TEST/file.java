//client: 보내기
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;
import java.net.UnknownHostException;
 
public class file {
    public static final int DEFAULT_BUFFER_SIZE = 10000;
    //public static void main(String[] args) {
    public static void main() {
        //String serverIP = args[0];              //String serverIP = "127.0.0.1";
        String serverIP = "13.125.160.38";
        //int port = Integer.parseInt(args[1]);   //int port = 9999;
        int port = 9300;
        //String FileName = args[2];              //String FileName = "test.mp4";
        String FileName = "/Users/zjisuoo/Documents/학교/OurChord/CODE/TEST/PDF/test.pdf";
        
         
        File file = new File(FileName);
        if (!file.exists()) {
            System.out.println("File not Exist.");
            System.exit(0);
        }
         
        long fileSize = file.length();
        long totalReadBytes = 0;
        byte[] buffer = new byte[DEFAULT_BUFFER_SIZE];
        int readBytes;
        double startTime = 0;
         
        try {
            FileInputStream fis = new FileInputStream(file);
            Socket socket = new Socket(serverIP, port);
            if(!socket.isConnected()){
                System.out.println("Socket Connect Error.");
                System.exit(0);
            }
             
            startTime = System.currentTimeMillis();
            OutputStream os = socket.getOutputStream();
            while ((readBytes = fis.read(buffer)) > 0) {
                os.write(buffer, 0, readBytes);
                totalReadBytes += readBytes;
                System.out.println("In progress: " + totalReadBytes + "/"
                        + fileSize + " Byte(s) ("
                        + (totalReadBytes * 100 / fileSize) + " %)");
            }
             
            System.out.println("File transfer completed.");
            fis.close();
            os.close();
            socket.close();
        } catch (UnknownHostException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
         
        double endTime = System.currentTimeMillis();
        double diffTime = (endTime - startTime)/ 1000;;
        double transferSpeed = (fileSize / 1000)/ diffTime;
         
       // System.out.println("time: " + diffTime+ " second(s)");
       // System.out.println("Average transfer speed: " + transferSpeed + " KB/s");
    }
}