<?php
   include("config.php");
   session_start();
   
   if($_SERVER["REQUEST_METHOD"] == "POST") {
      // username and password sent from form 
      
      $myusername = mysqli_real_escape_string($db,$_POST['username']);
      $mypassword = mysqli_real_escape_string($db,$_POST['password']); 
      
      $sql = "SELECT * FROM usuarios WHERE user = '$myusername' and password = '$mypassword'";
      $result = mysqli_query($db,$sql);
      $row = mysqli_fetch_array($result,MYSQLI_ASSOC);
      $active = $row['active'];
      
      $count = mysqli_num_rows($result);
      
      // If result matched $myusername and $mypassword, table row must be 1 row
		
      if($count == 1) {
         
         $_SESSION['login_user'] = $myusername;
         
         header("location: configuracion.php");
      }else {
         $error = "Usuario o Password invalida";
      }
   }
?>
<html>
   
 <head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Configuración</title>
<link href="estilos.css" rel="stylesheet" type="text/css">
</head>
   
   <body>
	
      <div class="group">        
               
               <form action = "" method = "post">
                  <label>Usuario  :</label><input type = "text" name = "username" class = "box"/><br /><br/>
                  <label>Password  :</label><input type = "password" name = "password" class = "box" /><br/><br />
                  <center><input class="form-btn"type = "submit" value = " Aceptar "/><br /></center>
               </form> 			   
			<div style = "font-size:11px; color:#cc0000; margin-top:10px"><?php echo $error; ?></div>			   
               			
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