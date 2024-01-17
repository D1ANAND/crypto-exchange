# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /NABEELBHAI

ENV HOST 0.0.0.0

# Copy the current directory contents into the container at /usr/src/app
COPY requirements.txt .  

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

COPY . .
# Make port 80 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["python","-m" ,"uvicorn", "nabeelbhai:app", "--host", "0.0.0.0", "--port", "80"]
