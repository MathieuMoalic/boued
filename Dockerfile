FROM node:23.5.0-alpine3.21 as frontend
WORKDIR /app
COPY frontend/package.json ./
COPY frontend/package-lock.json ./
RUN npm install
COPY frontend .
RUN npm run build
RUN npm prune --production

FROM python:3.13-slim
WORKDIR /app
COPY --from=frontend /app/static ./static
COPY backend/main.py ./
RUN pip install --no-cache-dir backend
EXPOSE 6001
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "6001"]