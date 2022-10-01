FROM linuxserver/code-server:latest

USER root
RUN apt-get update && \
    apt-get install -y sqlite3 && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.8 python3-pip s3fs && \
    rm -rf /var/lib/apt/lists

COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN ln -s /usr/bin/python3 /usr/bin/python && \
    mkdir -p /config/workspace/evelyn/ /config/workspace/omolara/ /config/workspace/lekan/
ENV PATH="${PATH}:/config/.local/bin"

## Set the directory where you want to mount your s3 bucket
ARG S3_MOUNT_DIRECTORY=/config/workspace
ENV S3_MOUNT_DIRECTORY=$S3_MOUNT_DIRECTORY

EXPOSE 8443

## Entry Point
ADD s3-docker-mount-script.sh /s3-docker-mount-script.sh
RUN chmod 755 /s3-docker-mount-script.sh
CMD ["/s3-docker-mount-script.sh"]
