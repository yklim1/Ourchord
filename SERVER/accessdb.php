<?php 
#php-db connection test php code
header("Content-Type: text/html; charset=UTF-8");

$con=mysqli_connect("localhost_name","ID","PASSWORD","TABLE_NAME"); 
  
if (mysqli_connect_errno($con))  
{  
   echo "Failed to connect to MySQL: " . mysqli_connect_error();  
}

$res = mysqli_query($con,"select * from grade");  
   
$result = array();  

#mysqli_fetch_array: 한글깨짐
while($row = mysqli_fetch_array($res)){  
  array_push($result,
    array('Sno'=>$row[0],'Sname'=>$row[1],'Year'=>$row[2],'Dept'=>$row[3]  
    ));  
}  
   
echo json_encode(array("result"=>$result));  
   
mysqli_close($con);
   
#print_r($_SERVER);
?>
