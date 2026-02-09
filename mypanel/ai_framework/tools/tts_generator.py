#!/usr/bin/env python3
"""
Hegemon Framework TTS Generator

Converts markdown files to audio using Qwen3-TTS models via mlx-audio.
Supports two modes:
- VoiceDesign: Natural language voice descriptions
- Base (Cloning): Clone any voice from 3-second reference audio

Usage:
    python tts_generator.py input.md [options]
    python tts_generator.py *.md --mode concat [options]

Requirements:
    - mlx-audio package (optimized for Apple Silicon)
    - soundfile
    - ffmpeg (for format conversion)
"""

import argparse
import os
import re
import sys
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple
import warnings

# Suppress transformers warnings during import
warnings.filterwarnings("ignore", category=UserWarning)


# Voice presets mapped to Hegemon agents
VOICE_PRESETS = {
    # Strategic/Executive - Confident, authoritative
    "ceo": "Confident American male executive, authoritative, measured pace, inspiring tone",
    "cfo": "Analytical American male, precise, data-focused, calm and methodical",
    "pitch": "Direct persuasive American male, high energy, assertive, compelling",

    # Technical - Precise, focused
    "dev": "Technical American male, pragmatic, clear, moderate pace",
    "architect": "Thoughtful American male, strategic, deliberate, authoritative on technical matters",
    "qa": "Detail-oriented American female, rigorous, precise, quality-focused",

    # Analytical/Research - Evidence-based
    "analyst": "Methodical American female, evidence-based, collaborative, thorough",
    "researcher": "Academic British male, methodical, citation-aware, transparent",

    # Process/Management - Organized
    "pm": "Organized American female, clear, coordinating, focused on outcomes",
    "legal": "Cautious American male, precise, risk-aware, formal",

    # Creative/Content - Engaging
    "writer": "Engaging American female, narrative-focused, adaptable, clear",
    "editor": "Refined British female, quality-focused, clear, maintains flow",
    "marketing": "Energetic American female, growth-focused, compelling, data-informed",

    # User-Focused - Empathetic
    "ux": "Empathetic American female, user-centered, iterative, research-driven",
    "ui": "Visual-minded American male, clarity-focused, accessibility-aware",
    "support": "Warm American female, helpful, enabling, solution-oriented",
}


def resolve_voice(voice_arg: Optional[str], default: str) -> str:
    """Resolve voice argument to description.

    Args:
        voice_arg: Voice preset name or literal description
        default: Default voice description if voice_arg is None

    Returns:
        Voice description string
    """
    if voice_arg is None:
        return default

    # Check if it's a preset name
    if voice_arg.lower() in VOICE_PRESETS:
        return VOICE_PRESETS[voice_arg.lower()]

    # Otherwise use as literal description
    return voice_arg


@dataclass
class TTSConfig:
    """Configuration for TTS generation."""
    # MLX-optimized models from mlx-community (requires mlx-audio v0.3.1+)
    voicedesign_model: str = "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16"
    clone_model: str = "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16"
    small_clone_model: str = "mlx-community/Qwen3-TTS-12Hz-0.6B-Base-bf16"
    default_voice: str = "Natural American professional male, clear articulation, moderate pace"
    default_language: str = "en"
    chunk_size: int = 2000  # Characters per chunk
    sample_rate: int = 24000  # Qwen3-TTS outputs 24kHz audio (12Hz = token rate, not sample rate)
    cache_dir: str = field(default_factory=lambda: os.path.expanduser("~/.cache/huggingface/hub"))


class ModelManager:
    """Manages lazy loading and caching of TTS models."""

    def __init__(self, config: TTSConfig):
        self.config = config
        self._voicedesign_model = None
        self._clone_model = None
        self._using_small_model = False

    def _check_model_cached(self, model_name: str) -> bool:
        """Check if a model is already cached."""
        cache_path = Path(self.config.cache_dir)
        model_dir_name = f"models--{model_name.replace('/', '--')}"
        model_path = cache_path / model_dir_name

        # Check if the model directory exists and has content
        if model_path.exists():
            snapshots_dir = model_path / "snapshots"
            if snapshots_dir.exists() and any(snapshots_dir.iterdir()):
                return True
        return False

    def _get_model_size(self, model_name: str) -> str:
        """Return approximate model size for user info."""
        if "0.6B" in model_name:
            if "8bit" in model_name or "4bit" in model_name:
                return "~400MB"
            return "~1.5GB"
        elif "1.7B" in model_name:
            if "8bit" in model_name:
                return "~2GB"
            elif "4bit" in model_name:
                return "~1GB"
            return "~4.5GB"
        return "unknown size"

    def _load_model(self, model_name: str):
        """Load a model using mlx-audio utilities (v0.3.1+)."""
        try:
            from mlx_audio.tts.utils import load_model
            model = load_model(model_name)
            return model
        except ImportError:
            print("Error: mlx-audio package not installed or outdated.", file=sys.stderr)
            print("Install latest: pip install git+https://github.com/Blaizzy/mlx-audio.git", file=sys.stderr)
            sys.exit(1)

    def get_voicedesign_model(self, confirm_download: bool = False):
        """Get the VoiceDesign model, downloading if needed."""
        if self._voicedesign_model is not None:
            return self._voicedesign_model

        model_name = self.config.voicedesign_model

        if not self._check_model_cached(model_name):
            if not confirm_download:
                print(f"""
⚠️  First-time setup: VoiceDesign model
   Model: {model_name}
   Size: {self._get_model_size(model_name)} download

   Cached in: {self.config.cache_dir}
   To proceed: Run with --confirm-download
""", file=sys.stderr)
                sys.exit(1)
            print(f"Downloading VoiceDesign model ({self._get_model_size(model_name)})...", file=sys.stderr)

        self._voicedesign_model = self._load_model(model_name)
        return self._voicedesign_model

    def get_clone_model(self, confirm_download: bool = False, use_small: bool = False):
        """Get the Base model for voice cloning, downloading if needed."""
        if self._clone_model is not None and self._using_small_model == use_small:
            return self._clone_model

        model_name = self.config.small_clone_model if use_small else self.config.clone_model

        if not self._check_model_cached(model_name):
            if not confirm_download:
                size_info = self._get_model_size(model_name)
                small_note = ""
                if not use_small:
                    small_note = f"\n   Alternative: Use --small-model for 0.6B version (~1.5GB)"
                print(f"""
⚠️  First-time setup: Base model (for voice cloning)
   Model: {model_name}
   Size: {size_info} download

   Cached in: {self.config.cache_dir}{small_note}
   To proceed: Run with --confirm-download
""", file=sys.stderr)
                sys.exit(1)
            print(f"Downloading Base model ({self._get_model_size(model_name)})...", file=sys.stderr)

        self._clone_model = self._load_model(model_name)
        self._using_small_model = use_small
        return self._clone_model


class MarkdownProcessor:
    """Process markdown files for TTS conversion."""

    def __init__(self, chunk_size: int = 2000):
        self.chunk_size = chunk_size

    def extract_title(self, content: str) -> Optional[str]:
        """Extract title from H1 header or frontmatter."""
        # Check for YAML frontmatter title
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE)
            if title_match:
                return title_match.group(1).strip()

        # Check for H1 header
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()

        return None

    def strip_formatting(self, content: str) -> str:
        """Strip markdown formatting for clean TTS text."""
        # Remove YAML frontmatter
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

        # Remove code blocks (keep description if it's a comment)
        content = re.sub(r'```[\s\S]*?```', '[code block omitted]', content)
        content = re.sub(r'`[^`]+`', '', content)

        # Convert headers to spoken form
        content = re.sub(r'^#{1,6}\s+(.+)$', r'\1.', content, flags=re.MULTILINE)

        # Remove links but keep text
        content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)

        # Remove images
        content = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'Image: \1', content)

        # Remove bold/italic markers
        content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
        content = re.sub(r'\*([^*]+)\*', r'\1', content)
        content = re.sub(r'__([^_]+)__', r'\1', content)
        content = re.sub(r'_([^_]+)_', r'\1', content)

        # Convert bullet points
        content = re.sub(r'^\s*[-*+]\s+', '• ', content, flags=re.MULTILINE)

        # Convert numbered lists
        content = re.sub(r'^\s*\d+\.\s+', '', content, flags=re.MULTILINE)

        # Remove HTML tags
        content = re.sub(r'<[^>]+>', '', content)

        # Remove horizontal rules
        content = re.sub(r'^[-*_]{3,}\s*$', '', content, flags=re.MULTILINE)

        # Clean up multiple newlines
        content = re.sub(r'\n{3,}', '\n\n', content)

        # Clean up multiple spaces
        content = re.sub(r' {2,}', ' ', content)

        return content.strip()

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks for processing."""
        if len(text) <= self.chunk_size:
            return [text]

        chunks = []
        sentences = re.split(r'(?<=[.!?])\s+', text)
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= self.chunk_size:
                current_chunk += (" " if current_chunk else "") + sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                # If a single sentence is too long, split it
                if len(sentence) > self.chunk_size:
                    words = sentence.split()
                    word_chunk = ""
                    for word in words:
                        if len(word_chunk) + len(word) + 1 <= self.chunk_size:
                            word_chunk += (" " if word_chunk else "") + word
                        else:
                            if word_chunk:
                                chunks.append(word_chunk)
                            word_chunk = word
                    current_chunk = word_chunk
                else:
                    current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def process_file(self, file_path: Path) -> Tuple[str, List[str]]:
        """Process a markdown file, returning title and text chunks."""
        content = file_path.read_text(encoding='utf-8')
        title = self.extract_title(content)
        clean_text = self.strip_formatting(content)
        chunks = self.chunk_text(clean_text)

        return title, chunks


class SmartNamer:
    """Generate intelligent filenames with version sequencing."""

    @staticmethod
    def slugify(text: str) -> str:
        """Convert text to a filename-safe slug."""
        # Convert to lowercase
        text = text.lower()
        # Replace spaces and special chars with hyphens
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_]+', '-', text)
        # Remove leading/trailing hyphens
        text = text.strip('-')
        # Limit length
        return text[:50]

    @staticmethod
    def get_next_version(output_dir: Path, base_name: str, extension: str) -> int:
        """Find the next version number for a file."""
        pattern = re.compile(rf'^{re.escape(base_name)}-v(\d+)\.{re.escape(extension)}$')
        max_version = 0

        if output_dir.exists():
            for f in output_dir.iterdir():
                match = pattern.match(f.name)
                if match:
                    version = int(match.group(1))
                    max_version = max(max_version, version)

        return max_version + 1

    @classmethod
    def generate_filename(cls, title: Optional[str], source_file: Path,
                         output_dir: Path, extension: str = "mp4") -> Path:
        """Generate a versioned filename from title or source file."""
        if title:
            base_name = cls.slugify(title)
        else:
            base_name = source_file.stem.lower()

        # Ensure we have a valid base name
        if not base_name:
            base_name = "audio"

        version = cls.get_next_version(output_dir, base_name, extension)
        filename = f"{base_name}-v{version}.{extension}"

        return output_dir / filename


def play_audio(wav_data: bytes) -> bool:
    """Play audio through system speakers using afplay (macOS).

    Args:
        wav_data: WAV audio data as bytes

    Returns:
        True if playback succeeded, False otherwise
    """
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        tmp.write(wav_data)
        tmp_path = tmp.name

    try:
        subprocess.run(['afplay', tmp_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error playing audio: {e}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("Error: afplay not found. This feature requires macOS.", file=sys.stderr)
        return False
    finally:
        os.unlink(tmp_path)


def play_audio_file(file_path: str) -> bool:
    """Play an audio file through system speakers.

    Args:
        file_path: Path to audio file (wav, mp3, mp4, etc.)

    Returns:
        True if playback succeeded, False otherwise
    """
    try:
        subprocess.run(['afplay', file_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error playing audio: {e}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("Error: afplay not found. This feature requires macOS.", file=sys.stderr)
        return False


def speak_notification(text: str, voice: str = "dev") -> bool:
    """Generate and play a short TTS notification.

    Args:
        text: Short text to speak (keep under 10 words for speed)
        voice: Voice preset name

    Returns:
        True if notification played successfully
    """
    config = TTSConfig()
    generator = AudioGenerator(config)
    voice_desc = resolve_voice(voice, config.default_voice)

    try:
        wav_data = generator.generate_wav(
            text,
            voice_description=voice_desc,
            confirm_download=True  # Don't block on notifications
        )
        return play_audio(wav_data)
    except Exception as e:
        print(f"Notification error: {e}", file=sys.stderr)
        return False


def is_inline_text(arg: str) -> bool:
    """Detect if argument is inline text vs file reference.

    Args:
        arg: The input argument to check

    Returns:
        True if this looks like inline text to speak, False if it's a file reference
    """
    # Inline if: starts with quote
    if arg.startswith('"') or arg.startswith("'"):
        return True
    # Inline if: contains spaces and doesn't end with .md
    if ' ' in arg and not arg.endswith('.md'):
        return True
    return False


def list_voice_presets() -> None:
    """Print available voice presets and exit."""
    print("\nAvailable Voice Presets:\n")
    print("Strategic/Executive:")
    for name in ["ceo", "cfo", "pitch"]:
        print(f"  {name:12} - {VOICE_PRESETS[name]}")

    print("\nTechnical:")
    for name in ["dev", "architect", "qa"]:
        print(f"  {name:12} - {VOICE_PRESETS[name]}")

    print("\nAnalytical/Research:")
    for name in ["analyst", "researcher"]:
        print(f"  {name:12} - {VOICE_PRESETS[name]}")

    print("\nProcess/Management:")
    for name in ["pm", "legal"]:
        print(f"  {name:12} - {VOICE_PRESETS[name]}")

    print("\nCreative/Content:")
    for name in ["writer", "editor", "marketing"]:
        print(f"  {name:12} - {VOICE_PRESETS[name]}")

    print("\nUser-Focused:")
    for name in ["ux", "ui", "support"]:
        print(f"  {name:12} - {VOICE_PRESETS[name]}")

    print("\nUsage: /tts -v <preset> \"Text to speak\"")
    print("       /tts --voice <preset> file.md")


class AudioGenerator:
    """Generate audio from text using Qwen3-TTS models."""

    def __init__(self, config: TTSConfig):
        self.config = config
        self.model_manager = ModelManager(config)

    def _check_ffmpeg(self) -> bool:
        """Check if ffmpeg is available."""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _validate_reference_audio(self, audio_path: Path) -> bool:
        """Validate reference audio file for voice cloning."""
        if not audio_path.exists():
            print(f"Error: Reference audio file not found: {audio_path}", file=sys.stderr)
            return False

        # Check duration using ffprobe
        try:
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                 '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)],
                capture_output=True, text=True, check=True
            )
            duration = float(result.stdout.strip())
            if duration < 3.0:
                print(f"Error: Reference audio must be at least 3 seconds (got {duration:.1f}s)",
                      file=sys.stderr)
                return False
            return True
        except (subprocess.CalledProcessError, ValueError, FileNotFoundError):
            # If ffprobe fails, let the model try to handle it
            print("Warning: Could not validate reference audio duration", file=sys.stderr)
            return True

    def generate_wav(self, text: str, voice_description: Optional[str] = None,
                     reference_audio: Optional[Path] = None,
                     confirm_download: bool = False,
                     use_small_model: bool = False) -> bytes:
        """Generate WAV audio from text using Qwen3-TTS via mlx-audio."""
        import soundfile as sf
        import numpy as np
        import io

        voice = voice_description or self.config.default_voice

        if reference_audio:
            # Voice cloning mode using Base model
            if not self._validate_reference_audio(reference_audio):
                sys.exit(1)

            model = self.model_manager.get_clone_model(confirm_download, use_small_model)

            # Generate with reference audio (model.generate for cloning)
            # ref_text is optional but helps quality
            results = list(model.generate(
                text=text,
                ref_audio=str(reference_audio),
                ref_text=None  # Could add transcript support later
            ))
        else:
            # VoiceDesign mode - use generate_voice_design
            model = self.model_manager.get_voicedesign_model(confirm_download)
            results = list(model.generate_voice_design(
                text=text,
                language=self.config.default_language,
                instruct=voice
            ))

        # Collect audio from all result segments
        all_audio = []
        for result in results:
            audio_segment = result.audio if hasattr(result, 'audio') else result

            # Convert MLX array to numpy
            if hasattr(audio_segment, 'tolist'):
                audio_np = np.array(audio_segment.tolist(), dtype=np.float32)
            else:
                audio_np = np.array(audio_segment, dtype=np.float32)

            all_audio.append(audio_np)

        # Concatenate all segments
        if all_audio:
            audio_data = np.concatenate(all_audio)
        else:
            audio_data = np.array([], dtype=np.float32)

        # Convert to WAV bytes (Qwen3-TTS outputs 12kHz)
        wav_buffer = io.BytesIO()
        sf.write(wav_buffer, audio_data, self.config.sample_rate, format='WAV')
        wav_buffer.seek(0)
        return wav_buffer.read()

    def convert_format(self, wav_data: bytes, output_path: Path, format: str) -> bool:
        """Convert WAV data to specified format using ffmpeg."""
        if not self._check_ffmpeg():
            print("Error: ffmpeg required. Install: brew install ffmpeg", file=sys.stderr)
            return False

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_wav:
            tmp_wav.write(wav_data)
            tmp_wav_path = tmp_wav.name

        try:
            cmd = ['ffmpeg', '-y', '-i', tmp_wav_path]

            if format == 'mp4':
                # MP4 with AAC audio
                cmd.extend(['-c:a', 'aac', '-b:a', '192k'])
            elif format == 'mp3':
                # MP3 with high quality
                cmd.extend(['-c:a', 'libmp3lame', '-q:a', '2'])
            elif format == 'wav':
                # Just copy for WAV
                cmd.extend(['-c:a', 'copy'])

            cmd.append(str(output_path))

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error converting audio: {result.stderr}", file=sys.stderr)
                return False

            return True
        finally:
            os.unlink(tmp_wav_path)

    def concatenate_wav(self, wav_files: List[bytes]) -> bytes:
        """Concatenate multiple WAV files."""
        import soundfile as sf
        import numpy as np
        import io

        all_audio = []
        for wav_data in wav_files:
            wav_buffer = io.BytesIO(wav_data)
            audio, sr = sf.read(wav_buffer)
            all_audio.append(audio)
            # Add a small pause between segments
            pause = np.zeros(int(sr * 0.5))  # 0.5 second pause
            all_audio.append(pause)

        # Remove the last pause
        if all_audio:
            all_audio = all_audio[:-1]

        combined = np.concatenate(all_audio)

        output_buffer = io.BytesIO()
        sf.write(output_buffer, combined, self.config.sample_rate, format='WAV')
        output_buffer.seek(0)
        return output_buffer.read()


def find_markdown_files(patterns: List[str], base_dir: Path) -> List[Path]:
    """Find markdown files matching the given patterns."""
    import glob

    files = []
    for pattern in patterns:
        # Handle wildcards
        if '*' in pattern:
            matches = glob.glob(str(base_dir / pattern))
            files.extend([Path(m) for m in matches if m.endswith('.md')])
        else:
            # Direct file reference
            path = Path(pattern)
            if not path.is_absolute():
                path = base_dir / pattern

            # Add .md extension if not present
            if not path.suffix:
                path = path.with_suffix('.md')

            if path.exists():
                files.append(path)
            else:
                # Try common locations
                for search_dir in [base_dir, base_dir / 'ai_project', base_dir / 'ai_framework']:
                    candidate = search_dir / path.name
                    if candidate.exists():
                        files.append(candidate)
                        break

    return sorted(set(files))


def main():
    parser = argparse.ArgumentParser(
        description='Convert markdown files to audio using Qwen3-TTS',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s README.md                          # VoiceDesign mode with default voice
  %(prog)s prd.md --voice "British female"    # Custom voice description
  %(prog)s prd.md --clone ~/sample.wav        # Clone voice from reference
  %(prog)s *.md --mode concat                 # Concatenate all files
  %(prog)s spec.md --format mp3               # Output as MP3

Speak Aloud Mode:
  %(prog)s "Hello, this is a test"            # Speak inline text directly
  %(prog)s -v ceo "Production approved"       # Speak as CEO agent voice
  %(prog)s --speak readme.md                  # Speak file aloud (no save)
  %(prog)s --list-voices                      # Show available voice presets
        """
    )

    parser.add_argument('input', nargs='*', help='Markdown file(s) or inline text to convert')

    # Voice options
    voice_group = parser.add_argument_group('Voice Options')
    voice_group.add_argument('-v', '--voice',
                            help='Voice preset name (e.g., ceo, dev) or description')
    voice_group.add_argument('--clone', metavar='FILE',
                            help='Reference audio for voice cloning (3+ seconds)')
    voice_group.add_argument('--list-voices', action='store_true',
                            help='List available voice presets and exit')

    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument('-o', '--output-dir',
                             help='Output directory (default: same as source)')
    output_group.add_argument('-f', '--format', choices=['mp4', 'mp3', 'wav'],
                             default='mp4', help='Output format (default: mp4)')
    output_group.add_argument('--speak', action='store_true',
                             help='Play audio aloud instead of saving to file')

    # Multi-file options
    multi_group = parser.add_argument_group('Multi-file Options')
    multi_group.add_argument('-m', '--mode', choices=['concat', 'split', 'single'],
                            default='concat',
                            help='concat: single output, split: separate files (default: concat)')

    # Model options
    model_group = parser.add_argument_group('Model Options')
    model_group.add_argument('--confirm-download', action='store_true',
                            help='Confirm model download on first use')
    model_group.add_argument('--small-model', action='store_true',
                            help='Use 0.6B Base model for cloning (smaller, faster)')

    # Notification options
    notify_group = parser.add_argument_group('Notification Options')
    notify_group.add_argument('--notify', action='store_true',
                             help='Play audio notification when conversion completes')
    notify_group.add_argument('--progress', action='store_true',
                             help='Show detailed progress updates during conversion')
    notify_group.add_argument('--quiet', action='store_true',
                             help='Suppress all output except errors (for background use)')

    args = parser.parse_args()

    # Handle --list-voices
    if args.list_voices:
        list_voice_presets()
        sys.exit(0)

    # Check for input
    if not args.input:
        parser.print_help()
        sys.exit(1)

    # Logging helper that respects --quiet flag
    def log(msg: str, level: str = "info"):
        """Print message unless --quiet is set. Level: info, progress, error"""
        if args.quiet and level != "error":
            return
        if level == "progress" and not args.progress:
            return
        print(msg, file=sys.stderr)

    # Track output for notification
    generated_files = []

    # Setup
    config = TTSConfig()
    generator = AudioGenerator(config)

    # Resolve voice (check presets first)
    voice_description = resolve_voice(args.voice, config.default_voice)

    # Determine mode: inline text speak vs file processing
    # Join all input args to check for inline text
    input_text = ' '.join(args.input)

    # Detect speak mode: inline text or --speak flag
    is_speak_mode = args.speak or is_inline_text(input_text)

    if is_speak_mode and not args.speak:
        # Inline text detected - strip quotes if present
        text_to_speak = input_text.strip('"\'')

        log(f"Speaking: \"{text_to_speak[:50]}{'...' if len(text_to_speak) > 50 else ''}\"")

        # Generate audio
        wav_data = generator.generate_wav(
            text_to_speak,
            voice_description=voice_description,
            reference_audio=Path(args.clone) if args.clone else None,
            confirm_download=args.confirm_download,
            use_small_model=args.small_model
        )

        # Play directly
        if play_audio(wav_data):
            log("✓ Done")
        else:
            sys.exit(1)
        return

    # File mode - find markdown files
    base_dir = Path.cwd()
    files = find_markdown_files(args.input, base_dir)

    if not files:
        print(f"Error: No markdown files found matching: {args.input}", file=sys.stderr)
        sys.exit(1)

    processor = MarkdownProcessor(config.chunk_size)

    # If --speak flag with files, play aloud instead of saving
    if args.speak:
        log(f"Speaking {len(files)} file(s)...")

        all_wav_chunks = []
        for file_path in files:
            log(f"  Processing: {file_path.name}")
            title, chunks = processor.process_file(file_path)

            for i, chunk in enumerate(chunks):
                log(f"    Chunk {i+1}/{len(chunks)}...", "progress")
                wav_data = generator.generate_wav(
                    chunk,
                    voice_description=voice_description,
                    reference_audio=Path(args.clone) if args.clone else None,
                    confirm_download=args.confirm_download,
                    use_small_model=args.small_model
                )
                all_wav_chunks.append(wav_data)

        # Concatenate if multiple chunks
        if len(all_wav_chunks) > 1:
            final_wav = generator.concatenate_wav(all_wav_chunks)
        else:
            final_wav = all_wav_chunks[0]

        # Play directly
        if play_audio(final_wav):
            log("✓ Done")
        else:
            sys.exit(1)
        return

    # File save mode (original behavior)
    log(f"Processing {len(files)} file(s)...")

    # Determine output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = files[0].parent

    # Process based on mode
    if args.mode == 'concat' and len(files) > 1:
        # Concatenate all files into one audio
        all_wav_chunks = []
        combined_title = None
        total_chunks = sum(len(processor.chunk_text(processor.strip_formatting(f.read_text()))) for f in files)
        current_chunk = 0

        for file_path in files:
            log(f"  Processing: {file_path.name}")
            title, chunks = processor.process_file(file_path)
            if combined_title is None and title:
                combined_title = title

            for i, chunk in enumerate(chunks):
                current_chunk += 1
                log(f"    Chunk {current_chunk}/{total_chunks} ({file_path.name})", "progress")
                wav_data = generator.generate_wav(
                    chunk,
                    voice_description=voice_description,
                    reference_audio=Path(args.clone) if args.clone else None,
                    confirm_download=args.confirm_download,
                    use_small_model=args.small_model
                )
                all_wav_chunks.append(wav_data)

        # Concatenate and convert
        combined_wav = generator.concatenate_wav(all_wav_chunks)
        output_path = SmartNamer.generate_filename(
            combined_title, files[0], output_dir, args.format
        )

        if generator.convert_format(combined_wav, output_path, args.format):
            log(f"✓ Generated: {output_path}")
            generated_files.append(output_path)
        else:
            sys.exit(1)

    else:
        # Process each file separately
        for file_idx, file_path in enumerate(files):
            log(f"Processing ({file_idx+1}/{len(files)}): {file_path.name}")
            title, chunks = processor.process_file(file_path)

            # Generate audio for each chunk
            wav_chunks = []
            for i, chunk in enumerate(chunks):
                log(f"  Chunk {i+1}/{len(chunks)}...", "progress")
                wav_data = generator.generate_wav(
                    chunk,
                    voice_description=voice_description,
                    reference_audio=Path(args.clone) if args.clone else None,
                    confirm_download=args.confirm_download,
                    use_small_model=args.small_model
                )
                wav_chunks.append(wav_data)

            # Concatenate chunks if multiple
            if len(wav_chunks) > 1:
                final_wav = generator.concatenate_wav(wav_chunks)
            else:
                final_wav = wav_chunks[0]

            # Generate output filename
            output_path = SmartNamer.generate_filename(
                title, file_path, output_dir, args.format
            )

            # Convert to final format
            if generator.convert_format(final_wav, output_path, args.format):
                log(f"✓ Generated: {output_path}")
                generated_files.append(output_path)
            else:
                sys.exit(1)

    # Play completion notification if --notify flag is set
    if args.notify and generated_files:
        if len(generated_files) == 1:
            notify_text = f"Conversion complete. {generated_files[0].name}"
        else:
            notify_text = f"Conversion complete. {len(generated_files)} files generated."
        speak_notification(notify_text, voice="dev")


if __name__ == '__main__':
    main()
