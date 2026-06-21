FROM node:24-alpine
WORKDIR /app
COPY src/package*.json ./
RUN npm install
COPY src/ .
CMD ["node", "index.js"]
