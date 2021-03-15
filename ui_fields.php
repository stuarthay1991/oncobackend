<?php
//Code for building UI
$pok = scandir("Columns");
$file_arr = $pok;
$output_arr = array();
for($i = 2; $i < count($file_arr); $i++)
{
	$cur_file = "Columns/" . $file_arr[$i];
	$cur_file_open = fopen($cur_file, "r");
	$line = fgets($cur_file_open);
	$line = explode("#", $line);
	$refname = substr($cur_file, 0, -4);
	$output_arr[$refname] = $line;
	fclose($cur_file_open);
}
echo json_encode($output_arr);
?>