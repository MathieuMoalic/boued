FROM python:3
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5001
COPY main.py ./
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "5001"]
