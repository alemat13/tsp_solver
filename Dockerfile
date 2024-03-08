# Stage 1: Build the React frontend
FROM node:20 as builder

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

COPY frontend/public ./public
COPY frontend/src ./src

RUN npm run build

# Stage 2: Setup Flask server to serve frontend and API
FROM python:3.12

WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY backend/requirements.txt /app/backend

# Installer les dépendances Python
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy built frontend from the previous stage
COPY --from=builder /app/build /app/frontend

# Copy backend code
COPY backend /app/backend

# Expose port for Flask server
EXPOSE 5000

# Define the command to run the Flask server
CMD ["python", "backend/app.py"]