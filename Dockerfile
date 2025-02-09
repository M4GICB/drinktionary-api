# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Accept build arguments for environment variables
ARG MONGODB_URL
ARG DB_NAME

# Set environment variables for the build process
ENV MONGODB_URL=$MONGODB_URL
ENV DB_NAME=$DB_NAME


# Copy the current directory contents into the container at /app
COPY . /app

# Install the necessary dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port that FastAPI will run on
EXPOSE 8000

# Run the application using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
