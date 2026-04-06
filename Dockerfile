# Base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 7860

# Run app using gunicorn
<<<<<<< HEAD
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:7860"]
=======
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:7860"]
>>>>>>> a78b4d1 (how are you)
