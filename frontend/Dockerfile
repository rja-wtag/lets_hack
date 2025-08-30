FROM node:24-alpine

WORKDIR /workspace

COPY ./frontend/package*.json ./
RUN npm install
COPY . .

EXPOSE 5173
