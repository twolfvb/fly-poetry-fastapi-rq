# Pull the official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install curl and pip, then Poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && pip install --upgrade pip \
    && curl -sSL https://install.python-poetry.org | python -

# Set the working directory
WORKDIR /app

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml /app/

ENV PATH="${PATH}:/root/.local/bin"


# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy all files
COPY . /app

# Command to run on container start
CMD ["./run.sh"]
