FROM qdrant/qdrant:latest

RUN apt update && \
    apt install s3fs -y && \
    apt install curl wget unzip -y && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    sudo ./aws/install


COPY ./s3-mount.sh /qdrant


EXPOSE 6333
EXPOSE 6334

RUN chmod 755 /qdrant/s3-mount.sh

CMD ["./s3-mount.sh"]