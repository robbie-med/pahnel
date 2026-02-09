# Tool Versions

## spec-kit
- **Version**: v0.0.90
- **Source**: https://github.com/github/spec-kit.git
- **Installation**: Vendored at `/ai_framework/tools/spec-kit/`
- **Execution**: `uvx --from ./ai_framework/tools/spec-kit specify`
- **Last Updated**: 2025-12-21

### New Features in v0.0.90
- `/clarify` - Interactive spec clarification (up to 5 questions)
- `/analyze` - Cross-artifact consistency analysis
- `/implement` - Checklist-validated implementation
- `speckit.` command prefix for discoverability
- Agent handoffs between commands
- Support for 16+ AI agents
- Quality checklists for validation
- Intelligent branch naming with `--short-name`

### Update Instructions
```bash
# Download fresh copy from GitHub
git clone --depth 1 https://github.com/github/spec-kit.git /tmp/spec-kit-fresh
rm -rf ai_framework/tools/spec-kit
cp -R /tmp/spec-kit-fresh ai_framework/tools/spec-kit
rm -rf ai_framework/tools/spec-kit/.git
# Update this file with new version
```

### Rollback Instructions
Not available for vendored copy. Re-clone specific version if needed.

## md-to-pdf
- **Version**: 5.2.4
- **Source**: npm package
- **Installation**: Global via npm (`npm install -g md-to-pdf`)
- **Location**: `/opt/homebrew/bin/md-to-pdf`
- **Purpose**: Convert markdown documentation to PDF format
- **Scripts**:
  - `/ai_framework/tools/md_to_pdf.sh` - Shell wrapper with custom output support
  - `/ai_framework/tools/pdf_generator.js` - Node.js module for programmatic use

### Usage
```bash
# Direct usage (outputs to same name.pdf)
md-to-pdf document.md

# Using wrapper script (supports custom output)
/ai_framework/tools/md_to_pdf.sh input.md [output.pdf]

# From Node.js
const { generatePDF } = require('./ai_framework/tools/pdf_generator.js');
await generatePDF('input.md', 'custom.pdf');
```

## mlx-audio (TTS Generation)
- **Package**: mlx-audio v0.3.1+ (from GitHub for latest Qwen3-TTS support)
- **Models**: Qwen3-TTS-12Hz series (MLX-optimized from mlx-community)
- **Source**: https://github.com/Blaizzy/mlx-audio
- **Installation**: Auto-installed via uv from git on first use
- **Purpose**: Convert markdown to audio with AI-generated speech on Apple Silicon
- **Output Sample Rate**: 24kHz
- **Scripts**:
  - `/ai_framework/tools/tts_generator.py` - Python module with all TTS logic
  - `/ai_framework/tools/md_to_tts.sh` - Shell wrapper for CLI usage

### Available Models

| Model | Size | Purpose |
|-------|------|---------|
| mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16 | ~4.5GB | Natural language voice descriptions |
| mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16 | ~4.5GB | Voice cloning from reference audio |
| mlx-community/Qwen3-TTS-12Hz-0.6B-Base-bf16 | ~1.5GB | Smaller voice cloning model |

**Note:** "12Hz" refers to the audio token rate, not sample rate. Audio output is 24kHz.

### Model Cache Location
```
~/.cache/huggingface/hub/
├── models--mlx-community--Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16/
└── models--mlx-community--Qwen3-TTS-12Hz-1.7B-Base-bf16/
```

### Voice Presets
Built-in presets for Hegemon agents: `ceo`, `cfo`, `pitch`, `dev`, `architect`, `qa`, `analyst`, `researcher`, `pm`, `legal`, `writer`, `editor`, `marketing`, `ux`, `ui`, `support`

### Usage
```bash
# Speak aloud (inline text)
/ai_framework/tools/md_to_tts.sh "Hello, this is a test"
/ai_framework/tools/md_to_tts.sh -v ceo "Production approved"

# VoiceDesign mode (file conversion)
/ai_framework/tools/md_to_tts.sh document.md
/ai_framework/tools/md_to_tts.sh document.md --voice "British female"

# Voice cloning mode
/ai_framework/tools/md_to_tts.sh document.md --clone ~/reference.wav

# Format options
/ai_framework/tools/md_to_tts.sh document.md --format mp3

# First-time download confirmation
/ai_framework/tools/md_to_tts.sh document.md --confirm-download

# List available voice presets
/ai_framework/tools/md_to_tts.sh --list-voices
```

### First-Run Notes
- Models are downloaded on first use of each mode
- VoiceDesign and Base models are separate (~4.5GB each)
- Use `--confirm-download` to acknowledge large download
- Use `--small-model` for smaller Base model (~1.5GB)
- Optimized for Apple Silicon (M1/M2/M3/M4) via MLX framework

## uv (External Dependency)
- **Required Version**: 0.8.0+
- **Purpose**: Python tool management for isolated execution
- **Installation**: See `/ai_framework/tools/DEPENDENCIES.md`