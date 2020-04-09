<!doctype html>
    <html lang="ko">
        <head>
        <meta charset="utf-8">
        <title>LoginDB Test</title>
        <style>
            body {
                font-family: Consolas, monospace;
                font-family: 12px;
            }
            table {
                width: 100%;
            }
            th, td {
                padding: 10px;
                border-bottom: 1px solid #dadada;
            }
        </style>
    </head>
    <body>
        <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>PASSWORD</th>
            </tr>
        </thead>
        <tbody>
            <?php
            #php-db connection test code
            #localhost/study/database_con_test.php
            #header("Content-Type: text/html; charset=UTF-8");
            $host="localhost";
            $user="userID";
            $pw="pw";
            $dbName="dbName";
                
            $mysqli=mysqli_connect($localhostName,$userId,$pw,$dbName);

            #MYSQL connection suc
            if($mysqli){
                echo "MYSQL 접속 성공<br><br>";
            }else{
                echo "MYSQL 접속 실패<br><br>" .mysqli_connect_error();
            }

            #show test login table
            $query="select *from test LIMIT 100;"; #"select * from table_name
            $res=mysqli_query($mysqli,$query);
            #$row=mysqli_fetch_array($res); - line53 while($res){ :error(첫번째 행만 무한반복 출력)

            #show data
            while($row=mysqli_fetch_array($res)){
                echo '<tr><td>' . $row['id'] . '</td><td>'. $row['password'] . '</td></tr>';
            }

            mysqli_close($mysqli);
            #print_r($_SERVER);
            ?>
        </tbody>
    </table>
  </body>
</html>