# Base image
ARG VARIANT="1-3.12-bookworm"
FROM mcr.microsoft.com/devcontainers/python:${VARIANT}

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

# Install Poetry
ARG POETRY_VERSION="1.8.5"
RUN su vscode -c "umask 0002 && pipx install poetry==${POETRY_VERSION}"
