FROM gliderlabs/alpine:latest
MAINTAINER Andre
COPY . /app
WORKDIR /app
RUN apk add --no-cache \
    python \
    python-dev \
    py-pip \
    build-base \
    libffi-dev \
    musl-dev \
    linux-headers
RUN pip install -r requirements.txt
RUN mkdir -p /var/app
ENTRYPOINT ["python"]
CMD ["manage.py", "server", "-h", "0.0.0.0"]
EXPOSE 5000
VOLUME /var/app

