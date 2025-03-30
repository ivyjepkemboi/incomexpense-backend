# Use official Python 3.8 image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first and install dependencies
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port for Flask
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]
