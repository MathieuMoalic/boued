FROM node:14-alpine

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./
RUN npm install
COPY . .
RUN npm run build
RUN npm prune --production

EXPOSE 5000
ENV HOST=0.0.0.0

CMD [ "npm", "start", "--","--port","5000" ]