FROM node:23.5.0-alpine3.21 as frontend
WORKDIR /app
COPY frontend/package.json ./
COPY frontend/package-lock.json ./
RUN npm install
COPY frontend .
RUN npm run build

FROM python:3.13-slim
WORKDIR /app
COPY backend/pyproject.toml backend/pyproject.toml
RUN pip install --no-cache-dir ./backend
COPY --from=frontend /app/build ./static
COPY backend backend
EXPOSE 6001
ENV DATABASE_URL=sqlite:////data/db1.sqlite

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
