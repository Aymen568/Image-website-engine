# Use an official Python runtime as the base image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit script and other necessary files to the working directory
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Set the default command to run when the container starts
CMD ["streamlit", "run", "--server.enableCORS", "false", "final_project.py"]