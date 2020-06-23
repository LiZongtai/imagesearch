<?php
header("Content-type:text/html; charset=utf-8");
echo "<link rel='stylesheet' href='upfile.css' type='text/css' />";
$file=$_FILES["file"]["tmp_name"];
$filename=$_FILES["file"]["name"];

$path="./image/";
$res=move_uploaded_file($file,$path.$filename);
if($res){
    setcookie('imgcookie',$filename);
    echo "<h1 align='center'>图片上传成功: ".$path.$filename."</h1>";
    echo "<br />";
    echo "<h3 align='center'>服务器网速慢，图片显示需要一定时间，请稍等</h3>";
    echo "<div align='center' style='font-size:30px'>";
    echo "<script type='text/javascript' src='upfile.js'></script>";
    echo "<br />";
    echo "<div class='div1'><img class='bg1' src='http://tjlzt98.cn/imagesearch/image/".$filename."' /></div>";
    echo "<br />";
    echo "<form action='search_hash.php' method='POST' enctype='multipart/form-data'>";
    echo "<input type='hidden' name='.$filename.' value='.$filename.' />";
    echo "<input type='submit' value='Hash搜索'onclick='my_hash()' class='btn'/>";
    echo "<div id='light_hash' class='white_content'>正在搜索请稍等<br />大约需要5s</div><div id='fade_hash' class='black_overlay'></div></form> ";
    echo "<br />";
    // echo "<form action='search_sift.php' method='POST' enctype='multipart/form-data'>";
    // echo "<input type='hidden' name='.$filename.' value='.$filename.' />";
    // echo "<input type='submit' value='SIFT搜索'onclick='my_sift()' class='btn'/>";
    // echo "<div id='light_sift' class='white_content'>正在搜索请稍等<br />大约需要120s</div><div id='fade_sift' class='black_overlay'></div></form> ";
    // echo "<br />";
    echo "<form action='search_hist.php' method='POST' enctype='multipart/form-data'>";
    echo "<input type='hidden' name='.$filename.' value='.$filename.' />";
    echo "<input type='submit' value='Hist搜索'onclick='my_hist()' class='btn'/>";
    echo "<div id='light_hist' class='white_content'>正在搜索请稍等<br />大约需要60s</div><div id='fade_hist' class='black_overlay'></div></form></div>";
}else{
    echo "图片上传失败";
}
?>