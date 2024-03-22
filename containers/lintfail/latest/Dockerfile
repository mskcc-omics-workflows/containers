FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get update && apt-get install -y curl
RUN echo "hello world" | grep "world" | wc -l
CMD ["echo", "Hello, world!"]
