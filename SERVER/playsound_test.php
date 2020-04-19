<?php
header("Content-Type: text/html; charset=UTF-8");

//phpinfo();

//$result= escapeshellcmd('python3 C:/APM_Setup/htdocs/Ourchord/androidtest/test.py');
//$output= shell_exec($result);

//$command = escapeshellcmd('python3 /APM_Setup/htdocs/Ourchord/androidtest/test.py');
//$output = shell_exec($command);
echo "실행시작";

//$command = escapeshellcmd('/Ourchord/androidtest/test.py');
//$output=shell_exec($command);
//echo "return value is: $output";

//$message=exec("cd C:\APM_Setup\htdocs\Ourchord\androidtest\test.py");
$message=exec("cd /Users/zjisuoo/Downloads/&& python3 ok.py");
echo $message;
echo "실행종료";
//print_r($message);


//pwd
//C:/testFile/soundtest/A.mp3
?>