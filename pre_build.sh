#!/bin/bash
set -e

echo "Starting pre-build script..."

# Download SAM checkpoint if missing or invalid
SAM_MODEL="sam_vit_b_01ec64.pth"
if [ ! -f "$SAM_MODEL" ] || [ ! -s "$SAM_MODEL" ]; then
    echo "SAM checkpoint not found or invalid. Downloading from official source..."
    curl -L -o "$SAM_MODEL" "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth"
    
    # Verify download
    if [ ! -f "$SAM_MODEL" ] || [ ! -s "$SAM_MODEL" ]; then
        echo "ERROR: Failed to download SAM checkpoint"
        exit 1
    fi
    
    echo "SAM checkpoint downloaded successfully."
    ls -lh "$SAM_MODEL"
else
    echo "SAM checkpoint already exists."
    ls -lh "$SAM_MODEL"
fi
