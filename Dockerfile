# Use a base image with Python and Node.js pre-installed
FROM python:3.9-slim

# Install Node.js and npm
RUN apt-get update && apt-get install -y nodejs npm

# Install youtube-po-token-generator globally
RUN npm install -g youtube-po-token-generator

# Set the working directory
WORKDIR /app

# Copy your project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 5000

# Command to run your Flask app
CMD ["python", "app.py", "--host=0.0.0.0"]
