<?php
header("Content-Type: text/html; charset=UTF-8");

phpinfo();

$host="localhost";
$user="userID";
$pw="pw";
$dbName="dbName";

$con=mysqli_connect($host, $user, $password, $dbname, $port);

 if($con){
    echo "MYSQL 접속 성공<br><br>";
    }else{
    echo "MYSQL 접속 실패<br><br>" .mysqli_connect_error();
     }
 
 $res = mysqli_query($con,"select * from testdb");  
    
 $result = array();  

 echo json_encode(array("result"=>$result));  
    
 mysqli_close($con);
    
 #print_r($_SERVER);
 ?>