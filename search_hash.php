<?php  
//字符编码设置  
header("Content-type:text/html;charset=utf-8");
// 数据库参数
$servername = "localhost";
$phashtablename = "image_search";
$password = "kyzdmbrK8hfyATry";
$dbname = "image_search";
$data = array();
class phashtable{
	public $id;
	public $name;
	public $phash;
}
// 连接数据库
$conn = new mysqli($servername, $phashtablename, $password, $dbname);
 
// 检测连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
} 
// echo "连接成功";

$sql = "SELECT * FROM `imgtable`;";
$result = $conn->query($sql);
if($result) {
    //echo "查询成功";
    while ($row = mysqli_fetch_array($result,MYSQL_ASSOC)) {
        $phashtable = new phashtable();
        // 主键序号
        $phashtable->id = $row["id"];
        // 文件名
        $phashtable->name = $row["name"];
        // 哈希值
        $phashtable->phash = $row["phash"];
        // 数据列表
        $data[]=$phashtable;
    }	
}
$image_name=$_COOKIE["imgcookie"];
$image_file='/www/wwwroot/tjlzt98.cn/imagesearch/image/'.$image_name;
// print_r($image_file);
// 搜索开始时间
$t1=microtime(true);
// 执行python脚本
$output=exec("python /www/wwwroot/tjlzt98.cn/imagesearch/PHashSim.py {$image_file}");
// 分割返回数据
$result=explode(',',$output);
// 最佳匹配相似度
$mindist=$result[0];
$similarity=(1-$mindist*1.0/64);
// 最佳匹配图像序号
$minindex=$result[1];
// 搜索结束时间
$t2=microtime(true);
// 计算搜索时间
$time1=$t2-$t1;
sleep(4);
// 输出结果
echo "<h1 align='center'>PHash算法图片搜索结果: </h1>";
echo "<div align='center' style='font-size:40px'>";
echo "<br />";
echo "<img src='http://tjlzt98.cn/imagesearch/coco/".$data[$minindex]->name."' />";
echo "<br />";
echo "<br />";
print_r('最佳匹配图像：'.$data[$minindex]->name);
echo "<br>";
print_r('汉明距离：'.$mindist);
echo "<br>";
print_r('相似度：'.$similarity);
echo "<br>";
print_r('程序执行时间:'.$time1);
echo "</div>";

?> 