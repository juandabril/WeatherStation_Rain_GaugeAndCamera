
<!doctype html>
<?php
include('session.php');
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

$sql = "SELECT * FROM config";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        $nameStation = $row["nameStation"];
		$Site = $row["Site"];
		$TimeSend = $row["TimeSend"];
		$ServerFTP = $row["ServerFTP"];
		$UserFTP = $row["UserFTP"];
		$PassFTP = $row["PassFTP"];
		$PathFTP = $row["PathFTP"];
		
		
    }
} else {
    echo "0 results";
}
$conn->close();
?>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Configuración</title>
<link href="estilos.css" rel="stylesheet" type="text/css">
</head>

<body>


<div class="group">
  <form action="registro.php" method="POST">
  <h2><em>Configuración Estación</em></h2>
  
     
      <label for="nameStation">Nombre Estación</label>
      <input type="text" name="nameStation" class="form-input" value="<?php echo $nameStation ?>"/>   
      
      <label for="Site">Ubicación </label>
      <input type="text" name="Site" class="form-input" value="<?php echo $Site ?>"/>             
      
      <label for="TimeSend">Tiempo de Envío en Minutos</label>
      <input type="text" name="TimeSend" class="form-input" value="<?php echo $TimeSend ?>"/>
	  
	  <label for="ServerFTP">Servidor FTP:</label>
      <input type="text" name="ServerFTP" class="form-input" value="<?php echo $ServerFTP ?>"/>
	  
	  <label for="UserFTP">Usuario FTP</label>
      <input type="text" name="UserFTP" class="form-input" value="<?php echo $UserFTP?>"/>
	  
	  <label for="PassFTP">Contraseña FTP</label>
      <input type="password" name="PassFTP" class="form-input" value="<?php echo $PassFTP?>"/>
	  
	   <label for="PathFTP">Path FTP</label>
      <input type="text" name="PathFTP" class="form-input" value="<?php echo $PathFTP?>"/>
	  
     <center> <input class="form-btn" name="submit" type="submit" value="Aceptar" /> <a class="boton" href="logout.php">Cerrar Sesión</a></center>
    
  </form>
</div>
<div class="footer">
	<div class="logo"> 
	<img alt="logo canalclima" src="http://aplicaciones.canalclima.com/plataforma/images/logoblack.png" style="height: 90px;">
	</div>
	<div class="copyright">© 2017 <a href="https://www.canalclima.com">Canal Clima</a> Todos los derechos reservados.</div>
	<div class="correo">E-mail: <a href="mailto:soporte.infraestructura@canalclima.com">soporte.infraestructura@canalclima.com</a>.</div>
	<div class="tel">Tel:(+57-1) 7046444</div>
	<div class="cel">Cel:317 4354213</div>
	<div class="version">Versión: 1.0</div>
</div>

</body>
</html>
