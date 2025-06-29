# Dockerfile for frontend (React + Vite)

# ------------ Base Stage ------------
FROM node:20-alpine AS base
WORKDIR /app

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

COPY package.json pnpm-lock.yaml ./
RUN pnpm install
COPY . .

# ------------ Development Stage ------------
FROM base AS development
EXPOSE 5173
CMD ["pnpm", "run", "dev", "--host"]

# ------------ Production Stage ------------
FROM base AS builder
RUN pnpm run build

FROM nginx:alpine AS production
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

