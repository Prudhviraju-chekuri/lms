FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY prisma ./prisma
# Prisma CLI downloads engines on first run if needed
CMD ["npm", "run", "migrate"]