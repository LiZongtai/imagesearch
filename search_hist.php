<?php  
//字符编码设置  
header("Content-type:text/html;charset=utf-8");
// 数据库参数
$servername = "localhost";
$histtablename = "image_search";
$password = "kyzdmbrK8hfyATry";
$dbname = "image_search";
$data = array();
class histtable{
	public $id;
	public $name;
	public $hist;
}
// 连接数据库
$conn = new mysqli($servername, $histtablename, $password, $dbname);
 
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
        $histtable = new histtable();
        // 主键序号
        $histtable->id = $row["id"];
        // 文件名
        $histtable->name = $row["name"];
        // 直方图数据
        $histtable->hist = $row["hist"];
        // 数据列表
        $data[]=$histtable;
    }	
}
$image_name=$_COOKIE["imgcookie"];
$image_file='/www/wwwroot/tjlzt98.cn/imagesearch/image/'.$image_name;
// print_r($image_file);
// 搜索开始时间
$t1=microtime(true);
// 执行python脚本
$output=exec("python /www/wwwroot/tjlzt98.cn/imagesearch/HistSim.py {$image_file}");
// 分割返回数据
$result=explode(',',$output);
// 最佳匹配相似度
$maxdiff=$result[0];
// $maxdiff1=(int)((int)$maxdiff*256);
// 最佳匹配图像序号
$maxindex=$result[1];
// 搜索结束时间
$t2=microtime(true);
// 计算搜索时间
$time1=$t2-$t1;
sleep(30);
// 输出结果
echo "<h1 align='center'>Hist算法图片搜索结果: </h1>";
echo "<div align='center' style='font-size:40px'>";
echo "<br />";
echo "<img src='http://tjlzt98.cn/imagesearch/coco/".$data[$maxindex]->name."' />";
echo "<br />";
echo "<br />";
print_r('最佳匹配图像：'.$data[$maxindex]->name);
echo "<br>";
// print_r('直方图差异：'.$maxdiff1);
// echo "<br>";
print_r('相似度：'.$maxdiff);
echo "<br>";
print_r('程序执行时间:'.$time1);
echo "</div>";

?> 