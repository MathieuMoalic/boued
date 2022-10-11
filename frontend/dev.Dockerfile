FROM node:18-alpine3.14
WORKDIR /app
COPY package.json ./
COPY package-lock.json ./
RUN npm install
ENV HOST=0.0.0.0
ENV PORT=6000
EXPOSE 6000
CMD [ "npm", "run", "dev"]
