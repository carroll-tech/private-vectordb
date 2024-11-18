# Base image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS build

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt .
RUN uv venv /opt/venv && \
    uv pip install --no-cache -r requirements.txt

# App image
FROM python:3.12-slim-bookworm AS app
COPY --from=build /opt/venv /opt/venv
ADD src/main.py .

# Activate the virtualenv in the container
# See here for more information:
# https://pythonspeed.com/articles/multi-stage-docker-python/
ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["/opt/venv/bin/python", "./main.py"]