# Use the official Python 3.12.4 slim image
FROM python:3.12.4-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file if it exists
COPY requirements.txt ./

# Install any required packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Expose port 5001 to the outside world (assuming you're using Flask)
EXPOSE 5001

# Define environment variable for Python to not buffer outputs
ENV PYTHONUNBUFFERED=1

# Run app.py when the container launches
CMD ["python", "app.py"]
