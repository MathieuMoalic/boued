FROM node:20.3.0-alpine3.18 as frontend
WORKDIR /app
COPY frontend/package.json ./
COPY frontend/package-lock.json ./
RUN npm install
COPY frontend .
RUN npm run build
RUN npm prune --production

FROM python:3.11.3-slim-buster
WORKDIR /app
COPY --from=frontend /app/dist ./static
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 6001
COPY backend/main.py ./
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "6001"]