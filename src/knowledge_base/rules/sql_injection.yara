rule SQL_Injection {
  strings:
    $sql1 = /SELECT.*FROM.*WHERE.*\$_GET/
    $sql2 = /SELECT.*FROM.*WHERE.*\$_POST/
    $sql3 = /SELECT.*FROM.*WHERE.*\$_REQUEST/
    $sql4 = /INSERT\s+INTO.*VALUES\s*\(.*\$_/
    $sql5 = /UPDATE.*SET.*WHERE.*\$_/
  condition:
    any of them
}