FROM golang:1.25-alpine AS builder

RUN apk add --no-cache git openssh ca-certificates

WORKDIR /app

ARG GIT_PERSONAL_ACCESS_TOKEN
ARG GIT_USERNAME

RUN if [ -n "$GIT_PERSONAL_ACCESS_TOKEN" ] && [ -n "$GIT_USERNAME" ]; then \
      git config --global url."https://${GIT_USERNAME}:${GIT_PERSONAL_ACCESS_TOKEN}@github.com/".insteadOf "https://github.com/"; \
    fi

ENV GOPRIVATE=github.com/Chazarov/simple-shop

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 go build -o main ./cmd/

FROM alpine:3.21

RUN apk add --no-cache ca-certificates

WORKDIR /app

COPY --from=builder /app/main .
COPY --from=builder /app/migrations ./migrations

EXPOSE 8080

CMD ["./main"]
