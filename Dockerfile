# Python image to use.
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# copy the requirements file used for dependencies
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY dogidentificationapp/ /app/dogidentificationapp/
COPY manage.py /app/

EXPOSE 8080

# Copy static files for production server
RUN ["python", "manage.py", "collectstatic"]

RUN ["python", "manage.py", "migrate"]

# Run app.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]