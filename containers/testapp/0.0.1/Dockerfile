FROM python:3.9-slim

# Labels
LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS"
LABEL org.opencontainers.image.authors="Anne Marie Noronha (noronhaa@mskcc.org)" 

LABEL org.opencontainers.image.created="2020-12-16T15:55:35Z" \ 
	org.opencontainers.image.version="0.0.1" \
	org.opencontainers.image.licenses="test-license" \
	org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/testapp/" \
    org.opencontainers.image.url="https://github.com/mskcc-omics-workflows/containers/" \
    org.opencontainers.image.title="My test app" \
    org.opencontainers.image.description="My test app description"



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