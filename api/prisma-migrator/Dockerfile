FROM node:20-alpine
WORKDIR /app
RUN apk add --no-cache openssl1.1
COPY package*.json ./
RUN npm ci --omit=dev
COPY prisma ./prisma
# Prisma CLI downloads engines on first run if needed
CMD ["npm", "run", "migrate"]