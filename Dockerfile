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
CMD ["uvicorn", "backend.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "6001"]