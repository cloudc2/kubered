FROM debian:jessie
MAINTAINER Matteo Guglielmetti <matteo.guglielmetti@hotmail.it>
#Updated by @larrysuto 

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    unzip \
    ca-certificates \
    wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /opt/gophish-v0.8.0-linux-64bit
RUN wget -nv https://github.com/gophish/gophish/releases/download/v0.8.0/gophish-v0.8.0-linux-64bit.zip && \
    unzip gophish-v0.8.0-linux-64bit.zip && \
    rm -f gophish-v0.8.0-linux-64bit.zip

RUN sed -i "s|127.0.0.1|0.0.0.0|g" config.json && \
    chmod +x gophish

EXPOSE 3333 80
ENTRYPOINT ["./gophish"]
