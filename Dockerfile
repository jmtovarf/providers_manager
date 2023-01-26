# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose the port for the application
EXPOSE 8000

# Run the command to start the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]