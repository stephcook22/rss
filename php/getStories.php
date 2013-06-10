<?php
    $con = mysql_connect('localhost','project','aPmezfFCepKJLhbW');
    if (!$con)
  {
  die('Could not connect: ' . mysql_error());
  }
  mysql_select_db("stories", $con);
  $query = "Select * from stories";
  $result = mysql_query($sql,$con);
while($row = mysql_fetch_array($result))
  {
  echo $row['Title'];
  echo "<br />";
  }
mysql_close($con);
