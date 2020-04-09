<!doctype html>
    <html lang="ko">
        <head>
        <meta charset="utf-8">
        <title>Modify(Add)DB Test</title>
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
            #create table & insert new values
            echo "query() to create table test code<br><br>";

            $host="localhost";
            $user="userID";
            $pw="pw";
            $dbName="dbName";
            $mysqli=new mysqli($host,$user,$pw,$dbName); 

            #MYSQL connection suc
            if($mysqli){
                echo "MYSQL 접속 성공<br><br>";
            }else{
                echo "MYSQL 접속 실패<br><br>" .mysqli_connect_error();
            }

            $sql="INSERT into test values";
            $sql=$sql."('me','meme&!')";
            $mysqli->query($sql);

            $sql="INSERT into test values";
            $sql=$sql."('ma','mama012@#')";
            $mysqli->query($sql);

            $sql="INSERT into test values";
            $sql=$sql."('mo','hilmomofiek*34')";
            $mysqli->query($sql);

            $sql='SELECT * FROM test';
            $res=$mysqli->query($sql);

            #record count
            echo 'record  count number: '.$res->num_rows;
            echo '<br>';

            #field count
            echo 'field count number: '.$res->field_count;
            echo '<br>';

            #show test login table
            $query="select *from test LIMIT 100;"; #"select * from table_name
            $res=mysqli_query($mysqli,$query);
            
            #show data
            while($row=mysqli_fetch_array($res)){
                echo '<tr><td>' . $row['id'] . '</td><td>'. $row['password'] . '</td></tr>';
            }

            mysqli_close($mysqli);
            ?>
        </tbody>
    </table>
  </body>
</html>