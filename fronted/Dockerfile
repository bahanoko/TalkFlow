FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN \
   if [ -f package-lock.json ]; then npm ci; \
   elif [ -f pnpm-lock.yaml ]; then npm install -g pnpm && pnpm install; \
   elif [ -f yarn.lock ]; then yarn install; \
   else npm install; fi

COPY . .

RUN npm run build

# 2. 実行用イメージ
FROM node:20-alpine

WORKDIR /app

COPY --from=builder /app ./

ENV NODE_ENV=production
EXPOSE 3000

CMD ["npm", "start"]