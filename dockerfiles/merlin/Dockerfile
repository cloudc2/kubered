# git clone https://github.com/Ne0nd0g/merlin into the docker build directory
# Run docker build -t merlin .

FROM golang:latest

LABEL maintainer="@larrysuto"

ARG GO111MODULE=auto

WORKDIR /merlin
COPY merlin/go.mod merlin/go.sum ./
RUN go mod download

COPY merlin/cmd/merlinserver /merlin/cmd/merlinserver
COPY merlin/pkg  /merlin/pkg

WORKDIR /merlin/cmd/merlinserver

RUN go build -o merlinserver .

RUN mkdir -p /merlin/cmd/merlinserver/data


EXPOSE 443

ENTRYPOINT ["./merlinserver"]
#CMD ["./merlinserver", "-i", "0.0.0.0"]
