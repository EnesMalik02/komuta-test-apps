FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
ARG NEXT_PUBLIC_GO_API_URL
ARG NEXT_PUBLIC_PY_API_URL
ENV NEXT_PUBLIC_GO_API_URL=$NEXT_PUBLIC_GO_API_URL \
    NEXT_PUBLIC_PY_API_URL=$NEXT_PUBLIC_PY_API_URL
RUN npm run build

FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production PORT=3000
COPY --from=build --chown=node:node /app ./
USER node
EXPOSE 3000
CMD ["npm", "start"]
