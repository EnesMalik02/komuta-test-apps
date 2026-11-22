FROM node:24-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
ARG NEXT_PUBLIC_TEST_ONE
ARG NEXT_PUBLIC_TEST_TWO
ENV NEXT_PUBLIC_TEST_ONE=$NEXT_PUBLIC_TEST_ONE \
    NEXT_PUBLIC_TEST_TWO=$NEXT_PUBLIC_TEST_TWO \
    NEXT_TELEMETRY_DISABLED=1
RUN npm run build && npm prune --omit=dev

FROM node:24-alpine
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1
WORKDIR /app
COPY --from=builder --chown=1001:1001 /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
EXPOSE 3000
USER 1001
CMD ["node_modules/.bin/next", "start", "-p", "3000"]
