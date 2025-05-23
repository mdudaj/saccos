FROM python:3.10

# Set the working directory in the container
WORKDIR /app/src

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/src

# Install python dependencies
COPY requirements.txt /app/src/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app/src
COPY . /app/src

# Expose the port the app runs on
EXPOSE 8000

# Run the application using Gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]