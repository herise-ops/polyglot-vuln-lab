# Intentionally old/EOL runtime for container-scanner findings.
FROM node:16-bullseye AS build

WORKDIR /app

COPY package*.json tsconfig.json ./
RUN npm ci

COPY src ./src
RUN npm run build

FROM node:16-bullseye-slim

WORKDIR /app
ENV NODE_ENV=production

COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force

COPY --from=build /app/dist ./dist
COPY public ./public

USER node
EXPOSE 3000

CMD ["node", "dist/server.js"]