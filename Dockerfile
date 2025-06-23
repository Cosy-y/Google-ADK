# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

# Install dependencies listed in requirements.txt
RUN pip install -r requirements.txt

# Ensure google-adk is installed (in case it's not listed in requirements)
RUN pip install google-adk

# Expose the port that adk web uses (default is 10000)
EXPOSE 10000

# Run the ADK web server
CMD ["sh", "-c", "adk web --host 0.0.0.0 --port ${PORT:-8000}"]

