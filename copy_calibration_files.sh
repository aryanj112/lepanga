#!/bin/bash
set -euo pipefail

DEST=~/Downloads/calibration_files
mkdir -p "$DEST"

cp ~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader/leader_arm.json "$DEST/"
cp ~/.cache/huggingface/lerobot/calibration/robots/so_follower/panga.json "$DEST/"

echo "Copied to $DEST:"
ls -la "$DEST"
