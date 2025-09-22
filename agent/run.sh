#!/bin/bash
# Agent runner script
cd "$(dirname "$0")"
PYTHONPATH=/Users/ongasatoshi/Documents/development/onc-limb/knowledge-hub uv run python main.py "$@"