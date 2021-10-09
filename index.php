<?php

//ouverture de la connexion à la bbd où on a récupérer les informations de la bourse

$objetPdo = new PDO('mysql:host=localhost;dbname=bourse','root','root');

$pdoStart = $objetPdo->prepare('Select * From nvidia');

//exécution de la requête

$executeIsOk = $pdoStart->execute();

//récupération des résultats

$contacts = $pdoStart->fetchAll();

?>

<!doctype php>
<html lang="fr">
<head>
	<meta charset="utf-8">
	<title>Les valeurs d'une bourse</title>
	<link rel="stylesheet" href="./style.css">

</head>
<body>
	<header>
			<div id="image1"><img src="./media/logo1.png" alt="menu"/></div>
			<div id="titre1"><h1>Recupération des informations de la bourse</h1></div>
			<div id="image2"><img src="./media/logo.png" alt="logo"></div>
	</header>

	<main>
			
		<div id="firstBlock">
			<h1> Valeur récupéré</h1>
			<div class="border"></div>

			<div id="tableau">
				<table>
					<tr>
						<th>Valeur en bourse</th>
						<th>Pourcentage</th>
						<th>Ouverture</th>
						<th>Valeur indicative</th>
						<th>clôture de veille</th>
						<th>Volume</th>
						<th>Date</th>
					</tr>
				
				<?php foreach ($contacts as $contacts): ?>
					<tr>
						<td><?= $contacts['valeur_boursiere'] ?></td>
						<td><?= $contacts['pourcentage'] ?></td>
						<td><?= $contacts['valeur_indicative'] ?></td>
						<td><?= $contacts['ouverture'] ?></td>
						<td><?= $contacts['cloture_veille'] ?></td>
						<td><?= $contacts['volume'] ?></td>
						<td><?= $contacts['date']?></td>
					</tr>
				<?php endforeach; ?>

				</table>
			</div>
		</div>
	</main>
</body>
</html>