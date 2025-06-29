<?php
$dataFile = __DIR__ . '/data/products.json';
$imageDir = __DIR__ . '/static/images';

function load_products($file) {
    if (file_exists($file)) {
        $json = file_get_contents($file);
        $data = json_decode($json, true);
        return is_array($data) ? $data : [];
    }
    return [];
}

function save_products($file, $products) {
    if (!is_dir(dirname($file))) {
        mkdir(dirname($file), 0777, true);
    }
    file_put_contents($file, json_encode($products, JSON_UNESCAPED_UNICODE));
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $title = $_POST['title'] ?? '';
    $description = $_POST['description'] ?? '';
    $imagePath = '';
    if (isset($_FILES['image']) && $_FILES['image']['error'] === UPLOAD_ERR_OK) {
        if (!is_dir($imageDir)) {
            mkdir($imageDir, 0777, true);
        }
        $filename = basename($_FILES['image']['name']);
        $target = $imageDir . '/' . $filename;
        move_uploaded_file($_FILES['image']['tmp_name'], $target);
        $imagePath = 'images/' . $filename;
    }
    $products = load_products($dataFile);
    $products[] = [
        'title' => $title,
        'description' => $description,
        'image' => $imagePath
    ];
    save_products($dataFile, $products);
    header('Location: admin.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>Admin Bereich</title>
<link rel="stylesheet" href="static/style.css">
</head>
<body>
<h1>Produkt hinzufügen</h1>
<form action="admin.php" method="post" enctype="multipart/form-data">
  <label>Titel: <input type="text" name="title"></label><br>
  <label>Beschreibung:<br><textarea name="description" rows="4" cols="50"></textarea></label><br>
  <label>Bild: <input type="file" name="image"></label><br>
  <input type="submit" value="Hinzufügen">
</form>
<a href="index.php">Zurück</a>
</body>
</html>
