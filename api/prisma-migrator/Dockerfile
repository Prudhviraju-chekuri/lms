FROM node:20-bullseye-slim
WORKDIR /app

# Install tini (optional, for better signal handling in containers)
RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*

COPY package*.json ./
RUN npm ci --omit=dev

COPY prisma ./prisma

CMD ["npm", "run", "migrate"]