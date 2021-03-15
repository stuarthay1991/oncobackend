<?php

//Connect to postgres db
$conn = pg_pconnect("dbname=oncocasen");
if (!$conn) {
    echo "An error occurred1.\n";
    exit;
}

//First query for sample ids. Will need to be changed to be contructed in depth.
$metaresult = pg_query($conn, ("SELECT * FROM meta WHERE batch_number='" . $_POST["Batch"] . "' AND primary_therapy_outcome_success='" .$_POST["DS"] . "'"));
if (!$metaresult) {
    echo "An error occurred2.\n";
    exit;
}

//Set up metaresult
$m_arr = array();
$m_arr_count = 0;

while ($mrow = pg_fetch_assoc($metaresult)) {
  $m_arr[$m_arr_count] = $mrow["submitter_id_samples"];
  $m_arr_count = $m_arr_count + 1;
}

//Hardcoded query for annotations for signatures
$makequery = "SELECT symbol, description, examined_Junction, background_major_junction, altexons, proteinpredictions, dpsi, clusterid, uid, coordinates, eventannotation, ";

//Only sample ids matched by the metadata query are retrieved
for($i = 0; $i < count($m_arr); $i++)
{
	//Strings have to be edited in order to be matched
	$str_edit = str_replace(".", "_", $m_arr[$i]);
	$str_edit = str_replace("-", "_", $str_edit);
	$str_edit = $str_edit . "_bed";
	$str_edit = strtolower($str_edit);
	//Add to query string
	$makequery = $makequery . $str_edit;
	if($i != (count($m_arr) - 1))
	{
		$makequery = $makequery . ", ";
	}
	else
	{
		$makequery = $makequery . " FROM gasm";
	}
}

//Remove newline characters (if any) from result
$makequery = str_replace("\n", "", $makequery);
$makequery = str_replace("\r", "", $makequery);

//Connect and send the query
$result = pg_query($conn, $makequery);
if (!$result) {
    echo "An error occurred3.\n";
    exit;
}

//Set up result
$rr = "";
$enum = 50;
$returned_result = array();
$col_beds = array();
$col_beds_i = 0;
//This line takes the number of columns
$total_cols = pg_num_fields($result);

//This portion separates the sample ids from the annotation columns
for($i = 0; $i < $total_cols; $i++)
{
	$cur_name = pg_field_name($result, $i);
	$last_4_chars = substr($cur_name, -4);
	if($last_4_chars == "_bed")
	{
		$col_beds[$col_beds_i] = $cur_name;
		$col_beds_i = $col_beds_i + 1;
	}
}

//Because this we are in a testing phase, we limit the rows to 80
for($i = 0; $i < 80; $i++)
{
  $row = pg_fetch_assoc($result);
  $returned_result[$i] = $row;
}

//Set up output
$pull_array = array();
$pull_array["rr"] = $returned_result;
$pull_array["col_beds"] = $col_beds;
$pull_array = json_encode($pull_array);
echo $pull_array;

?>