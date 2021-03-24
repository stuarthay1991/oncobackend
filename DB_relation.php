<<?php  
$json = exec ('python generate_php_dic.py', $output);
$cancer_dic = json_decode($json, true);
?>