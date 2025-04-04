FROM python:3-alpine

WORKDIR /app

# Copy the entire directory to the container
COPY . .

# Install required Python packages
RUN pip install --no-warn-script-location flet mysql-connector-python

# Command to run the application
CMD ["python", "./main.py"]