<?
header("Content-Type: text/html; charset=UTF-8");
#php.net -> setcookie
/*setcookie(string $name [, string $value=""[, int $expires=0 [, string $path=""[,
string $domain ="" [, bool $secure =FALSE [, bool $httponly =FALSE]]]]]]]):bool
setcookie(쿠키이름, 데이터, 종료시간, 경로, 도메인, 보안, $httponly);*/
# $secure =FALSE : httponly(javascript의 cookie 보호)/secure: javascript이외의 cookie접근 보호 / secure설정시, https가 아닌곳에 쿠키 제공x /true로 설정
# $httponly =FALSE : CSS(Cross Site Scripting)공격(쿠키에 접근할 수 없도록) 제한 / 기본값 false(true로 설정)
#time()+(3600:60*60==1hour==3600sec *24hour *30days

setcookie("Test","what",time()+(3600*24*30),"/");

#cookie data in php
echo $_COOKIE["Test"];

#delete cookie in C:\APM_Setup\htdocs\COOKIE.php
#setcookie("Test","",time()-3600);

#현재 실행중인 file's path
print_r($_SERVER);
?>
