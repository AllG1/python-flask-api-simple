# Base image
ARG VARIANT="3.12-bookworm"
FROM python:${VARIANT}

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

# Set working directory
WORKDIR /workspace

# Copy necessary files
COPY ./pyproject.toml /workspace/
COPY ./build/uwsgi.ini /workspace/
COPY ./build/entrypoint.sh /workspace/

# Install Poetry
ARG POETRY_VERSION="1.8.5"
RUN pip install poetry==${POETRY_VERSION}
RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root

# Copy application code
COPY ./src /workspace/

# Run application
CMD ["bash", "/workspace/entrypoint.sh"]