# Utiliser l'image Python officielle comme image de base
FROM python:3.9

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers dans le conteneur
COPY . .

EXPOSE 5000

# Commande par défaut à exécuter lors du démarrage du conteneur
CMD [ "python", "./app.py" ]
