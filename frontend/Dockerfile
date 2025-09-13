# Use Node.js LTS
FROM node:lts-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

# Use PORT from Render, fallback to 3000 locally
CMD ["sh", "-c", "next start -p ${PORT:-3000}"]