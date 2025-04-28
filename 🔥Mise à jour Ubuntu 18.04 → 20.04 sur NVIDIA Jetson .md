# 🔥 Mise à jour Ubuntu 18.04 → 20.04 sur NVIDIA Jetson (JetPack)
# Introduction

La mise à jour (**upgrade**) du système d'exploitation est une étape essentielle pour garantir la stabilité, la sécurité et la performance d'un ordinateur, en particulier dans les projets utilisant des plateformes embarquées comme le **Jetson Nano** ou d'autres modules **NVIDIA Jetson**.
Dans le domaine de la **vision par ordinateur** (Computer Vision), où les traitements d'images et les modèles d'intelligence artificielle nécessitent des ressources matérielles puissantes et des outils logiciels récents, disposer d'un système d'exploitation à jour est encore plus crucial.

Cette démarche permet d'accéder aux dernières versions de bibliothèques comme **CUDA**, **TensorRT**, **OpenCV** ou **PyTorch**, optimisées pour offrir de meilleures performances d'inférence et de traitement. De plus, une version récente d'Ubuntu assure une meilleure compatibilité avec les nouveaux pilotes GPU, les frameworks modernes et les dispositifs de capture d'images (caméras haute définition, caméras stéréo, etc.).

Dans ce guide, nous allons expliquer étape par étape comment réaliser la mise à jour de l'OS d'une plateforme Jetson, en passant d'Ubuntu 18.04 vers Ubuntu 20.04 , tout en détaillant l'importance de chaque commande utilisée.

# Pourquoi mettre à jour (upgrader) l'OS ?

**1\. Accéder à des nouvelles fonctionnalités**
🔵 Un nouvel OS apporte souvent des améliorations dans le noyau Linux, dans les bibliothèques système, dans les pilotes matériels (drivers), etc.

**2\. Bénéficier de meilleures performances**
🔵 Optimisations du système pour mieux utiliser le CPU, la RAM, et surtout pour Jetson : une meilleure gestion du GPU NVIDIA.

**3\. Sécurité**
🔵 Corriger des failles de sécurité critiques.
Un OS ancien est vulnérable aux attaques modernes.

**4\. Meilleure compatibilité logicielle**
🔵 Beaucoup d'outils récents (TensorFlow, PyTorch, OpenCV, ROS2, CUDA, TensorRT, etc.) nécessitent Ubuntu 20.04 ou supérieur pour fonctionner correctement.

# Et pour la **Computer Vision** alors ?

Dans le domaine de la **Computer Vision** (Vision par Ordinateur), **mettre à jour l'OS** est important car :

**🔵 Meilleure compatibilité avec CUDA, TensorRT et les GPU NVIDIA**

* Les frameworks comme OpenCV ou PyTorch utilisent directement CUDA/TensorRT pour accélérer les traitements (ex. traitement d'image, détection d'objet, segmentation...).
* Ubuntu 20.04 est souvent requis pour installer facilement les dernières versions de ces librairies.

**🔵 Accéder aux nouvelles fonctionnalités de Computer Vision**

* Certaines opérations (comme DNN, Deep Learning inference, YOLO, Faster-RCNN) utilisent des accélérations matérielles disponibles uniquement dans les versions récentes.

**🔵 Support des nouveaux matériels**

* Si tu branches une caméra moderne (ex : caméra stéréo, ZED, RealSense...), souvent le SDK ou les pilotes demandent une version récente d'Ubuntu.

**🔵 Optimisation pour le temps réel**

* Les optimisations dans Ubuntu 20.04 permettent un meilleur traitement en temps réel, ce qui est crucial pour des applications embarquées sur Jetson (ex: surveillance vidéo, drones, robots).

# Implémentation :

**Attention :**

* Ce processus est délicat car JetPack est très lié à la version de l'OS.
* Sauvegardez votre travail avant de commencer !

---

## 1\. Vérifier les versions actuelles

```bash
gcc --version 
python3 --version
```

**Pourquoi ?**
✅ Pour vérifier quelle version de GCC (compilateur C++) et Python sont installées.
✅ Certaines mises à jour peuvent casser des dépendances si les versions sont trop anciennes.

---

## 2\. Nettoyer les paquets inutiles (important)

```bash
sudo apt-get remove --purge chromium-browser
```

**Pourquoi ?**
✅ Chromium dans Ubuntu 18.04 est en paquet DEB, mais dans 20.04 il passe en Snap. Ça peut bloquer la mise à jour.
✅ Le retirer évite des conflits plus tard.

---

## 3\. Mise à jour du système actuel

```bash
sudo apt-get update 
sudo apt-get upgrade 
sudo apt-get autoremove
```

**Pourquoi ?**
✅ `update` : Met à jour la liste des paquets.
✅ `upgrade` : Installe les dernières versions des paquets existants.
✅ `autoremove` : Supprime les anciens paquets devenus inutiles.

---

## 4\. Autoriser la mise à jour de distribution

```bash
sudo nano /etc/update-manager/release-upgrades
```

👉 Modifier la ligne :

```bash
- Prompt=never 
+ Prompt=normal
```

**Pourquoi ?**
✅ `Prompt=normal` permet d'autoriser le passage vers une version supérieure d'Ubuntu.

---

## 5\. Mise à jour avancée des paquets

```bash
sudo apt-get update 
sudo apt-get dist-upgrade
```

**Pourquoi ?**
✅ `dist-upgrade` est plus puissant que `upgrade`, il gère les changements de dépendances (nouveaux/remplacés).

---

## 6\. Lancer la montée de version officielle

```bash
sudo do-release-upgrade
```

**Que faire pendant ?**
🔵Lorsque le système vous demande si vous souhaitez continuer, répondez **"y"** (oui).
🔵Lorsqu'une question apparaît concernant un fichier de configuration modifié, choisissez **"n"** pour conserver votre version actuelle.

---

⚠️ NE PAS REDÉMARRER IMMÉDIATEMENT ! Avant cela, il faut régler des paramètres liés au serveur graphique NVIDIA.

---

## 7\. Corriger l'affichage graphique NVIDIA

```bash
sudo nano /etc/gdm3/custom.conf
```

👉 Décommenter la ligne suivante (enlever le `#`) :

```bash
WaylandEnable=false
```

**Pourquoi ?**
✅ Wayland est activé par défaut dans Ubuntu 20.04, mais Jetson utilise X11 et NVIDIA Driver qui fonctionnent mieux sans Wayland.

---

```bash
sudo nano /etc/X11/xorg.conf
```

👉 Décommenter ou ajouter :

```bash
Driver "nvidia"
```

**Pourquoi ?**
✅ Force le système à utiliser le driver NVIDIA au démarrage (important pour l'accélération GPU).

---

## 8\. Verrouiller à nouveau les mises à jour automatiques de version

```bash
sudo nano /etc/update-manager/release-upgrades
```

👉 Remettre :

```bash
- Prompt=normal 
+ Prompt=never
```

**Pourquoi ?**
✅ Empêche Ubuntu de vous proposer accidentellement de passer à Ubuntu 22.04 (non compatible avec JetPack actuel).

---

## 9\. Redémarrer proprement

```bash
sudo reboot
```

✅ Après le redémarrage, votre Jetson doit tourner sous **Ubuntu 20.04** avec les réglages NVIDIA fonctionnels !