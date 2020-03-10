<?
header("Content-Type: text/html; charset=UTF-8");
#php.net -> setcookie

setcookie("Test","what",time()+(3600*24*30),"/");

#cookie data in php
echo $_COOKIE["Testcookie"];

#delete cookie in C:\APM_Setup\htdocs\COOKIE.php
#setcookie("Test","",time()-3600);

#현재 실행중인 file's path
print_r($_SERVER);
?>
