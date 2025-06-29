<?php
$dataFile = __DIR__ . '/data/products.json';
$products = [];
if (file_exists($dataFile)) {
    $json = file_get_contents($dataFile);
    $products = json_decode($json, true) ?: [];
}
?>
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>Produkte</title>
<link rel="stylesheet" href="static/style.css">
</head>
<body>
<h1>Produkte</h1>
<div class="products">
<?php foreach ($products as $p): ?>
  <div class="product">
    <?php if (!empty($p['image'])): ?>
      <img src="static/<?php echo htmlspecialchars($p['image']); ?>" alt="<?php echo htmlspecialchars($p['title']); ?>">
    <?php endif; ?>
    <h2><?php echo htmlspecialchars($p['title']); ?></h2>
    <p><?php echo nl2br(htmlspecialchars($p['description'])); ?></p>
  </div>
<?php endforeach; ?>
</div>
<a href="admin.php">Admin Bereich</a>
</body>
</html>
