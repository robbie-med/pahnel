# Hegemon Framework Tool Dependencies

## Required Global Dependencies

### uv (Required)
**Purpose**: Package and tool management for isolated Python tool execution  
**Installation**: 
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# After installation, restart terminal or run:
source ~/.bashrc  # or ~/.zshrc on macOS

# Verify installation
uv --version
```

**Why Required**: 
- Enables isolated execution of spec-kit without global Python pollution
- Manages Python dependencies automatically
- Ensures consistent tool behavior across projects

**Used By**:
- spec-kit integration (`uvx --from ./ai_framework/tools/spec-kit`)
- TTS generation (`uv run --with "mlx-audio @ git+https://github.com/Blaizzy/mlx-audio.git"`)

### ffmpeg (Required for TTS)
**Purpose**: Audio format conversion for TTS output (MP4, MP3, WAV)
**Installation**:
```bash
# macOS (Homebrew)
brew install ffmpeg

# Linux (apt)
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

**Why Required**:
- Converts raw WAV audio to MP4/MP3 formats
- Validates reference audio duration for voice cloning
- Concatenates audio segments for multi-file processing

**Used By**:
- TTS generator (`/ai_framework/tools/md_to_tts.sh`)

## Optional Dependencies

### git (Expected)
- Required for submodule management
- Usually pre-installed on development systems

### Python 3.8+ (Managed by uv)
- Not required globally if uv is installed
- uv handles Python version management

## Checking Dependencies

Run this command to verify all dependencies:
```bash
.claude/hooks/check_dependencies.sh
```

Or manually check:
```bash
command -v uv >/dev/null 2>&1 && echo "✅ uv installed" || echo "❌ uv not found"
command -v git >/dev/null 2>&1 && echo "✅ git installed" || echo "❌ git not found"
command -v ffmpeg >/dev/null 2>&1 && echo "✅ ffmpeg installed" || echo "❌ ffmpeg not found (needed for /tts)"
```

## Framework Initialization

The `/init` command will:
1. Check for required dependencies
2. Prompt for installation if missing
3. Verify spec-kit submodule is accessible
4. Test isolated execution with uvx

---

*Last Updated: 2026-01*
*Dependencies Version: 1.1*