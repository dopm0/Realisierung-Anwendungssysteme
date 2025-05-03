#!/bin/bash
URL="https://${CODESPACE_NAME}.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}:8080/"
echo "structurizr.url=$URL" >>structurizr.properties
docker restart $(docker ps -f name=structurizr-lite -q)
echo "Restarting container for ${URL}workspace/explore"