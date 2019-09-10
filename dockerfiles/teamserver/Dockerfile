# BUILD INSTRUCTIONS & README
# Modified from:  https://blog.obscuritylabs.com/docker-command-controll-c2/
# docker build --build-arg cskey="xxxx-xxxx-xxxx-xxxx" -t teamserver/ub18 .
FROM ubuntu:18.04 as base 

MAINTAINER kubered 
LABEL version="1.0"
LABEL description="Dockerfile for CobaltStrike."

# setup local env
ARG cskey
ENV cs_key ${cskey}

# docker hardcoded sh...
SHELL ["/bin/bash", "-c"]

RUN apt-get update && \
    apt-get install -y wget curl net-tools sudo software-properties-common apt-utils --no-install-recommends && \
    apt install -y openjdk-11-jdk && \
    update-java-alternatives -s java-1.11.0-openjdk-amd64 && \
    rm -rf /var/lib/apt/lists/*


# install CobaltStrike with license key and update
RUN var=$(curl 'https://www.cobaltstrike.com/download' -XPOST -H 'Referer: https://www.cobaltstrike.com/download' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: https://www.cobaltstrike.com' -H 'Host: www.cobaltstrike.com' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Connection: keep-alive' -H 'Accept-Language: en-us' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5' --data "dlkey=$cs_key" | sed -n 's/.*href="\([^"]*\).*/\1/p' | grep /downloads/ | cut -d '.' -f 1) && \
    cd /opt && \
    wget https://www.cobaltstrike.com$var.tgz && \
    tar xvf cobaltstrike-trial.tgz && \
    cd cobaltstrike && \
    echo $cs_key > ~/.cobaltstrike.license && \
    ./update

# cleanup image
RUN apt-get -y clean && \
    apt-get -y autoremove

# set entry point
WORKDIR "/opt/cobaltstrike"
ENTRYPOINT ["./teamserver"]
