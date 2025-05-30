FROM node:20-alpine AS builder

WORKDIR /frontend

COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN \
   if [ -f package-lock.json ]; then npm ci; \
   elif [ -f pnpm-lock.yaml ]; then npm install -g pnpm && pnpm install; \
   elif [ -f yarn.lock ]; then yarn install; \
   else npm install; fi

COPY . .

RUN npm run build

FROM node:20-alpine

WORKDIR /frontend

COPY --from=builder /frontend ./

ENV NODE_ENV=production
EXPOSE 3000

CMD ["npm", "start"]