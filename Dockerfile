# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required by PyMuPDF, OpenCV, and pdf2docx
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libfreetype6-dev \
    libjpeg-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create temp upload directory
RUN mkdir -p temp_uploads

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app.py"]
