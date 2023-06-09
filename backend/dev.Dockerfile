FROM python:3.11
WORKDIR /app
COPY requirements.txt ./
RUN pip install fastapi[complete] uvicorn
EXPOSE 6001
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "6001", "--reload"]
