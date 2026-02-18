FROM node:18-alpine AS builder

WORKDIR /app

# Build arguments for environment variables
ARG VITE_WS_URL=ws://localhost:8000/ws

# Set environment variables from build args
ENV VITE_WS_URL=$VITE_WS_URL

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files to nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
