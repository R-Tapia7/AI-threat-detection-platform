# Build
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json .
RUN npm ci

COPY . .

# ARG receives the value from docker-compose at build time.
# ENV makes it available to the Vite build process.
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# Serve with nginx
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]