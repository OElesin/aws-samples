#!/bin/bash
set -eux
s3fs whiteboardlyapp-assets65004-dev:/demo /qdrant/storage -o nonempty
echo "Lekan"
bash ./entrypoint.sh