# Base image
FROM python:latest

# Set work directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy project code
COPY . .

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "corbado-auth.py"]