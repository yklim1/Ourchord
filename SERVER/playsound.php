<?php
header("Content-Type: text/html; charset=UTF-8");

phpinfo();
//안스 튜닝음 받아오기
$tuning=$_POST['tuning'];

//exc(cf. radio button)
if(empty($tuning)){
    //$errMSG="듣고 싶은 튜닝음을 선택해주세요.";
    echo "듣고 싶은 튜닝음을 선택해주세요.<br><br>";
}

//suc
//if(!isset($errMSG)){
else{
      //1.DB접근
      $host ="localhost";
      $user = "userID";
      $password ="password";
      $dbname ="dbname";
      
      $con=mysqli_connect($host, $user, $password, $dbname);
      
      if($con){
          echo "MYSQL Connection success<br><br>";
          }else{
          echo "MYSQL Connection fail <br><br>" .mysqli_connect_error();
          }

      //2.SQL에서 튜닝음 경로 추출
     
      $sql= "SELECT *FROM Sound where tuning='$tuning'";
      $result=mysqli_query($con, $sql);
      while($row=mysqli_fetch_array($result)){
        //tuning음을 통한 음의 경로 얻어오기
        echo $row['tuning']."/".$row['path'];
        echo "<br>";
        //py코드에 넘길 db에 저장된 path
        $path=$row['path'];
      }
      mysqli_close($conn);

      //3.py
      $python= shell_exec($path);
      echo $python;
}
?>
