<!doctype html>
    <html lang="ko">
        <head>
        <meta charset="utf-8">
        <title>Login Test</title>
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
            $localhostName='localhost';
            $userId='ID';
            $pw='PASSWORD';
            $dbName='DATABASENAME';
                
            $mysqli=mysqli_connect($localhostName,$userId,$pw,$dbName);

            #MYSQL connection suc
            if($mysqli){
                echo "MYSQL 접속 성공<br><br>";
            }else{
                echo "MYSQL 접속 실패<br><br>" .mysqli_connect_error();
            }

            #show test login table
            $query="select *from TABLE_NAME LIMIT 2;"; #"select * from table_name
            $res=mysqli_query($mysqli,$query);

            #show data
            while($row=mysqli_fetch_array($res)){
                echo '<tr><td>' . $row['FIRSTROW'] . '</td><td>'. $row['SECONDROW'] . '</td></tr>';
            }

            mysqli_close($mysqli);

            ?>
        </tbody>
    </table>
  </body>
</html>
