# Procédure de mise à jour

> Si vous avez déjà installé Hugo, passez directement à la section *Procédure mise à jour blog*

## Installation de Hugo sur votre machine

Il suffit de suivre les [instructions détaillées de GoHugo](https://gohugo.io/getting-started/quick-start/) concernant votre OS et comment vous souhaitez l'installer.

## Procédure mise à jour blog

> ***Vous devez avoir installé Hugo localement avant de procéder à une mise à jour***

* Faire tout d'abord un ```git pull``` du dépôt
* Mettre votre nouveau post au format MarkDown ```[nomdupost].md``` dans la section ```./hugo_base/content/blog```
* Ajouter une en-tête à votre post pour renseigner les catégories, la date, l'auteur, les images éventuelles. Utilisez l'exemple ci-dessous comme base (*vous pouvez créer n'importe quelle catégorie, elle sera référencée automatiquement mais il serait bien d'essayer d'être raccord avec les autres posts*). Rendez-vous après le bloc ci-dessous pour des explications détaillées:

```markdown
+++
author = "GeoDataScience crew"
categories = ["misc", "presentation"]
date = "2019-05-20"
description = "This is a description"
featured = "MonImageTitre.jpg"
featuredalt = "Titre de mon image titre"
featuredpath = "date"
linktitle = ""
title = "Welcome"
type = "post"

+++
```
* Détails de l'en-tête (***tout est à mettre entre ```"``` sauf procédure particulière pour les catégories***):
  * ```author```: *Votre nom d'auteur pour le blog*
  * ```categories```: *liste de catégories entre ```[]```, avec des noms entre deux ```"```*
  * ```date```: *date au format ```YYYY-MM-DD```*
  * ```description```: *description de votre post*
  * ```featured```: *nom de votre image titre, si aucune mettre ```""```*
  * ```featuredalt```: *titre de votre image titre, si aucun mettre ```""```*
  * ```featuredpath```: *méthode de référence pour trouver votre image (cf. point détaillé ci après concernant les images)*
  * ```linktitle```: *laisser ```""``` pour le moment*
  * ```title```: titre de votre post
  * ```type```: type de post. Normalement toujours ```"post"```
* Détails concernant les images:
  * ```featuredpath```: votre image titre doit se trouver dans le dossier annuel puis mensuel correspondant. Par exemple, pour mai 2019, votre image doit se trouver dans ```./hugo_base/static/img/2019/05```. Bien entendu il faudra créer des dossiers pour les années et mois suivants, sauf à changer de méthode (*renseignements à prendre*)
  * images dans votre post: les placer dans le même dossier que votre post et y faire référence dans votre fichier MarkDown avec une chemin relatif et au format MarkDown ou balise HTML (*à vérifier si cela fonctionne bien*)
* Une fois cela fait, suivez la procédure suivante en étant à la racine de votre répertoire local GitHub:
```bash
cd hugo_base
hugo server -D
```
* Vérifier la bonne marche de votre mise à jour en local en allant sur http://localhost:1313/
* Ensuite vous pouvez générer le véritable site web à jour dans le répertoire ```./docs``` en vous mettant à la racine du repertoire ```hugo_base``` du dépôt (*là où les éléments Hugo se trouvent*)
```bash
hugo -d ../docs
```
* Si tout se passe correctement vous devriez obtenir quelque chose de similaire à ceci dans votre shell:
```bash
Building sites .
                   | EN | FR
+------------------+----+----+
  Pages            | 20 | 11
  Paginator pages  |  0 |  0
  Non-page files   |  0 |  0
  Static files     | 12 | 12
  Processed images |  0 |  0
  Aliases          |  5 |  1
  Sitemaps         |  2 |  1
  Cleaned          |  0 |  0

Total in 59 ms
```
* Vous pouvez ensuite faire un ```git commit``` puis un ```git push``` et normalement GitHub Pages prend le relais et quelques secondes/minutes après, le site à jour est en ligne sur
