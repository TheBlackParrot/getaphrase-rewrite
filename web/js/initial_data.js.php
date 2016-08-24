<?php
	$root = dirname(dirname(dirname(__FILE__)));
	$out = shell_exec('cd ' . $root . '; ./main.py 2>&1');
?>
var data = JSON.parse('<?php echo trim($out); ?>');