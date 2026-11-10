FROM ubuntu:24.04
WORKDIR /app
COPY greet /app
RUN chmod +x greet
ENV GREETING="Hi"
ENV NAME="You"
CMD ["./greet"]

