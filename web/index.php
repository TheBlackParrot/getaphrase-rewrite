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
		if(!$data['phrase']) {
			$root = dirname(dirname(__FILE__));
			$out = str_replace('\'', '\\\'', shell_exec('cd ' . $root . '; ./main.py 2>&1'));

			$data = json_decode($out, true);
			$data_j = $out;
		}
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

	$effects = [];
	switch(mt_rand(0, 5)) {
		case 1: // dark shadow
			$effects[] = "text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.75);";
			break;

		case 2: // light shadow
			$effects[] = "text-shadow: 0px 1px 0px rgba(255, 255, 255, 0.75);";
			break;

		case 3: // outline
			$amount = mt_rand(1, 3);
			$effects[] = "text-shadow: -{$amount}px -{$amount}px 0 #000, {$amount}px -{$amount}px 0 #000, -{$amount}px {$amount}px 0 #000, {$amount}px {$amount}px 0 #000;";
			break;

		case 4: // emboss
			$effects[] = "text-shadow: -1px -1px 0px rgba(255,255,255,0.4), 1px 1px 0px rgba(0,0,0,0.8);";
			break;

		case 5: // retro
			$spacing = mt_rand(2, 4);
			$direction = mt_rand(-1, 1);
			$offset = $spacing*$direction;
			$offset_double = $offset*2;
			$spacing_double = $spacing*2;
			$css[] = "text-shadow: {$offset}px {$spacing}px 0px #{$bg}, {$offset_double}px {$spacing_double}px 0px rgba(0,0,0,0.5);";
			break;
	}

	$weight = mt_rand(4, 7)*100;
?>

<html>

<head>
	<title>get a phrase: <?php echo $data['phrase'] . ' (ID ' . $data['id'] . ')'; ?></title>
	<link rel="stylesheet" type="text/css" href="css/reset.css">
	<link rel="stylesheet" type="text/css" href="css/main.css">

	<script type="text/javascript" src="js/jquery.js"></script>
	<script>
		var raw_data = '<?php echo trim($data_j); ?>';
		var data = JSON.parse(raw_data);
	</script>
	<style>
		@import 'https://fonts.googleapis.com/css?family=<?php echo $font_safe; ?>';
		.wrapper {
			background-color: #<?php echo $bg; ?>;
			color: #<?php echo $fg; ?>;
		}
		#phrase {
			font-family: "<?php echo $font; ?>", sans-serif;
			font-weight: <?php echo $weight; ?>;
			<?php foreach($effects as $effect) {
				echo($effect);
			}
			?>
		}
	</style>
</head>

<body>
	<div class="wrapper">
		<div id="phrase"><?php echo $data['phrase']; ?></div>
		<?php
			if(!$data['phrase']) {
				echo '<script>console.log("$data[\"phrase\"] was empty, fell back to JS to render text");$("#phrase").text(data.phrase);</script>';
			}
		?>
	</div>
	<div class="bottom">
		<div class="left">
			<a href="https://twitter.com/getaphrase" class="twitter-follow-button" data-show-count="true">Follow @getaphrase</a><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
			<iframe style="margin-left: 24px;" src="https://ghbtns.com/github-btn.html?user=theblackparrot&repo=getaphrase-2&type=star&count=true" frameborder="0" scrolling="0" width="170px" height="20px"></iframe>
		</div>
		<div class="right">
			<a href="index.php?id=<?php echo $data['id']; ?>">permalink</a>
		</div>
	</div>
</body>

</html>