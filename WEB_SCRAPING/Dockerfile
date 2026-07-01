# Use official Python runtime as base image
FROM python:3.14-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose port 8000 (default for FastAPI/Uvicorn)
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

