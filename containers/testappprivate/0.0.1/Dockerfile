FROM python:3.9-slim

# Labels
LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS"
LABEL org.opencontainers.image.authors="Anne Marie Noronha (noronhaa@mskcc.org)"
LABEL org.opencontainers.image.created="2020-12-16T15:55:35Z"
LABEL org.opencontainers.image.version="0.0.1"
LABEL org.opencontainers.image.licenses="test-license"
LABEL org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/testappprivate/"
LABEL org.opencontainers.image.url="https://github.com/mskcc-omics-workflows/containers/"
LABEL org.opencontainers.image.title="My private test app"
LABEL org.opencontainers.image.description="My private test app description"
LABEL IMAGEPRIVACY="true"



# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
# For this example, we won't have any dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]


