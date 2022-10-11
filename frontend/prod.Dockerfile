FROM node:18-alpine3.14
WORKDIR /app
COPY package.json ./
COPY package-lock.json ./
RUN npm install
COPY . .
RUN npm run build
RUN npm prune --production
ENV HOST=0.0.0.0
ENV PORT=5000
EXPOSE 5000
CMD [ "npm", "start"]