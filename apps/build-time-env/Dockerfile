FROM node:24-alpine AS builder
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
ARG NEXT_PUBLIC_TEST_ONE
ARG NEXT_PUBLIC_TEST_TWO
ENV NEXT_PUBLIC_TEST_ONE=$NEXT_PUBLIC_TEST_ONE \
    NEXT_PUBLIC_TEST_TWO=$NEXT_PUBLIC_TEST_TWO
RUN npm run build

FROM node:24-alpine AS runner
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PORT=3000 \
    HOSTNAME=0.0.0.0
WORKDIR /app
COPY --from=builder --chown=1001:1001 /app/package.json ./package.json
COPY --from=builder --chown=1001:1001 /app/node_modules ./node_modules
COPY --from=builder --chown=1001:1001 /app/.next ./.next
USER 1001
EXPOSE 3000
CMD ["node_modules/.bin/next", "start", "-p", "3000"]
