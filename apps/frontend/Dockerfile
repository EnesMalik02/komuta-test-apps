FROM node:22-alpine AS builder
WORKDIR /app
ARG NEXT_PUBLIC_GO_API_URL
ARG NEXT_PUBLIC_PY_API_URL
ENV NEXT_PUBLIC_GO_API_URL=$NEXT_PUBLIC_GO_API_URL
ENV NEXT_PUBLIC_PY_API_URL=$NEXT_PUBLIC_PY_API_URL
COPY package.json package-lock.json ./
RUN npm ci --legacy-peer-deps
COPY . .
RUN npm run build

FROM node:22-alpine
ENV NODE_ENV=production
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
EXPOSE 3000
USER 1001
CMD ["node_modules/.bin/next", "start", "-p", "3000"]
