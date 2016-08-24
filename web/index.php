<?php
	include dirname(__FILE__) . "/config.php";

	$fonts = json_decode(file_get_contents("lists/fonts.json"));
	$font = $fonts[mt_rand(0, count($fonts)-1)];
	$font_safe = str_replace(" ", "+", $font);

	if(isset($_GET['id'])) {
		if(ctype_alnum($_GET['id'])) {
			if($stmt = $mysqli->prepare("SELECT * FROM cache WHERE id = ?")) {
				$stmt->bind_param("s", $_GET['id']);
				$stmt->execute();
				$result = $stmt->get_result();

				while($row = $result->fetch_assoc()) {
					$data = $row;
				}
			}
		}
	}

	if(!isset($data)) {
		$root = dirname(dirname(__FILE__));
		$out = str_replace('\'', '\\\'', shell_exec('cd ' . $root . '; ./main.py 2>&1'));

		$data = json_decode($out, true);
		$data_j = $out;
	} else {
		$data_j = str_replace('\'', '\\\'', json_encode($data));
	}

	$colors = json_decode(file_get_contents("lists/colors.json"), true);
	if(mt_rand(0, 1)) {
		$fg = $colors["light"][mt_rand(0, count($colors["light"])-1)];
		$bg = $colors["dark"][mt_rand(0, count($colors["dark"])-1)];
	} else {
		$bg = $colors["light"][mt_rand(0, count($colors["light"])-1)];
		$fg = $colors["dark"][mt_rand(0, count($colors["dark"])-1)];
	}
?>

<html>

<head>
	<title>get a phrase: <?php echo $data['phrase'] . ' (ID ' . $data['id'] . ')'; ?></title>
	<link rel="stylesheet" type="text/css" href="css/reset.css">
	<link rel="stylesheet" type="text/css" href="css/main.css">

	<script type="text/javascript" src="js/jquery.js"></script>
	<script>
		var data = JSON.parse('<?php echo trim($data_j); ?>');
	</script>
	<style>
		@import 'https://fonts.googleapis.com/css?family=<?php echo $font_safe; ?>';
		.wrapper {
			background-color: #<?php echo $bg; ?>;
			color: #<?php echo $fg; ?>;
		}
		#phrase {
			font-family: "<?php echo $font; ?>", sans-serif;
			font-size: 10vw;
		}
	</style>
</head>

<body>
	<div class="wrapper">
		<div id="phrase"><?php echo $data['phrase']; ?></div>
		<?php
			if(!$data['phrase']) {
				echo "<span>something has gone wrong here, just refresh.</span>";
			}
		?>
	</div>
	<div class="bottom">
		<div class="left">
			<a href="https://twitter.com/getaphrase" class="twitter-follow-button" data-show-count="true">Follow @getaphrase</a><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
		</div>
		<div class="right">
			<a href="index.php?id=<?php echo $data['id']; ?>">permalink</a>
		</div>
	</div>
</body>

</html>