# https://developers.home-assistant.io/docs/apps/configuration#app-dockerfile
ARG BUILD_FROM=ghcr.io/home-assistant/base:3.23
FROM ${BUILD_FROM}

RUN \
    apk add --no-cache \
        python3 \
        py3-pip \
        nodejs \
        npm \
        jq \
        curl \
    && curl -LsSf https://get.pip.io/get-pip.py | python3 \
    && pip install uv mcpo --break-system-packages \
    && rm -rf /var/cache/apk/*

COPY rootfs /

LABEL \
    org.opencontainers.image.title="Home Assistant App: mcpo MCP Proxy" \
    org.opencontainers.image.description="Expose MCP tools as OpenAPI HTTP endpoints for Open WebUI." \
    org.opencontainers.image.source="https://github.com/mcpo-community/mcpo-hass-app" \
    org.opencontainers.image.licenses="MIT"
