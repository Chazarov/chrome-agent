FROM golang:1.25-alpine AS builder

# Устанавливаем git и openssh для работы с приватными репозиториями
RUN apk add --no-cache git openssh ca-certificates

WORKDIR /app

ARG GIT_PERSONAL_ACCESS_TOKEN
ARG GIT_USERNAME
ENV GIT_PERSONAL_ACCESS_TOKEN=${GIT_PERSONAL_ACCESS_TOKEN}
ENV GIT_USERNAME=${GIT_USERNAME}

RUN git config --global url."https://${GIT_USERNAME}:${GIT_PERSONAL_ACCESS_TOKEN}@github.com/".insteadOf "https://github.com/"
ENV GOPRIVATE=github.com/Chazarov/simple-shop

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o main ./cmd/

 