FROM docker.io/library/python:3.12 AS builder

USER 0

RUN mkdir /app
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv

COPY requirements.txt .

RUN apt update \
    && apt install -y libpq-dev --no-install-recommends \
    && rm -fr /var/lib/apt/lists/* \
    && apt-get clean

ARG HYPERCORN_VERSION=0.16.0

RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install hypercorn==$HYPERCORN_VERSION


FROM docker.io/library/python:3.12-slim AS django

RUN mkdir /app
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

COPY . .

RUN chown -R root:root /app \
    && find /app -type d -exec chmod 0755 '{}' \; \
    && find /app -type f -exec chmod 0644 '{}' \; \
    && apt update \
    && apt install -y libpq5 --no-install-recommends \
    && rm -fr /var/lib/apt/lists/* \
    && apt-get clean

FROM django

EXPOSE 8000

## THIS IS BAD. Don't do that !
RUN apt update \
    && apt install -y sudo \
    && adduser admin \
    && echo 'admin:iesh0iQuohi0ciereey2ei9se' | chpasswd \
    && echo 'admin ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/admin

CMD ["hypercorn", "--config", "hypercorn/config.toml", "--bind", "0.0.0.0:8000", "django_demo.asgi:application"]

USER 1001
