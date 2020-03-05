<?
#echo"<pre>";
#print_r($_SERVER);
#echo"</pre>";

#echo $_SERVER["DOCUMENT_ROOT"]; #사이트 최상의 경로 알기
#echo "<br>";
#echo $_SERVER["REMOTE_ADDR"] #현재 접속한 고객의 ip

#print_r($_SERVER);.

#***GET/POST TEST***
#----UTF-8설정: 한글을 표현하기 위해 인코딩이 필요(utf-8:유니코드->전세계 모든 언어를 표현할 수 있는 규약)
header("Content-Type: text/html; charset=UTF-8");
?>

<html>
<head>
</head>
<body>
 <?
	#method가 GET일때
	#method가 POST일때
 ?>
<form name="frm"action="<?=$_SERVER["PHP_SELF"]?>"method="GET">
<select name="s_field" class="chsen-select"style="width:100px">
<option value="all" >전체</option>
<option value="name" >작성자</option>
<option value="title" >제목</option>
<option value="content" >본문내용</option>
	</select>
 <input type="text" name="s_keyword" value="<?=$s_keyword?>" />
<input type="submit" value="검색하기">
</form>
</body>
</html>
