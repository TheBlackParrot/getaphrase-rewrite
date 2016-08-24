<?php
	header("Content-type: text/plain");

	$root = dirname(dirname(__FILE__));
	
	$out = shell_exec('cd ' . $root . '; ./main.py 2>&1');

	echo $out;
?>