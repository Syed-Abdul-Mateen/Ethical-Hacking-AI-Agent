rule XSS_Reflected {
  strings:
    $xss1 = /echo\s*\(\s*\$_GET/
    $xss2 = /print\s*\(\s*\$_POST/
    $xss3 = /document\.write\s*\(\s*location\.hash/
    $xss4 = /innerHTML\s*=\s*location\.search/
  condition:
    any of them
}