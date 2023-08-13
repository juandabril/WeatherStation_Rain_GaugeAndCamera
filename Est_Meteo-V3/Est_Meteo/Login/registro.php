<?php
$servername = "localhost";
$username = "root";
$password = "A1234567a";
$dbname = "configRPI";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$subs_nameStation = utf8_decode($_POST['nameStation']);
$subs_Site = utf8_decode($_POST['Site']);
$subs_TimeSend = utf8_decode($_POST['TimeSend']);
$subs_ServerFTP = utf8_decode($_POST['ServerFTP']);
$subs_UserFTP = utf8_decode($_POST['UserFTP']);
$subs_PassFTP = utf8_decode($_POST['PassFTP']);
$subs_PathFTP = utf8_decode($_POST['PathFTP']); 

$sql = "UPDATE config SET nameStation='$subs_nameStation', Site ='$subs_Site', TimeSend = '$subs_TimeSend', ServerFTP = '$subs_ServerFTP', UserFTP = '$subs_UserFTP', PassFTP = '$subs_PassFTP', PathFTP = '$subs_PathFTP'  WHERE id=1";

if ($conn->query($sql) === TRUE) {
    header('Location: Success.html');
} else {
    header('Location: Fail.html');
}

$conn->close();
?>