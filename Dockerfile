# Use official Python image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy project files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask default port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
