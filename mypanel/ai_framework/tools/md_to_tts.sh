#!/bin/bash
# MD to TTS converter using Qwen3-TTS models
# Supports VoiceDesign (natural language descriptions) and Base (voice cloning)
#
# Usage:
#   md_to_tts.sh file.md                      # Convert file to audio
#   md_to_tts.sh "Hello world"                # Speak inline text aloud
#   md_to_tts.sh -v ceo "Production ready"    # Speak with CEO voice preset
#   md_to_tts.sh --speak readme.md            # Speak file aloud (no save)
#   md_to_tts.sh --list-voices                # Show available voice presets

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GENERATOR_SCRIPT="$SCRIPT_DIR/tts_generator.py"

# Check for uv
if ! command -v uv &> /dev/null; then
    echo "Error: uv is required but not installed."
    echo "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check for ffmpeg (only required for file output, not speak mode)
# Let Python handle this check based on the mode

# Run the TTS generator with uv for isolated execution
# Using mlx-audio (v0.3.1+) for Apple Silicon optimization with full Qwen3-TTS support
# Installing from git to ensure latest version with generate_voice_design support
uv run --python 3.10 --with "mlx-audio @ git+https://github.com/Blaizzy/mlx-audio.git" --with soundfile --with numpy \
    python "$GENERATOR_SCRIPT" "$@"
