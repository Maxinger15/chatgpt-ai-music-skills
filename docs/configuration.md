# Configuration

Config file: `~/.maxinger15-music/config.yaml`

Create from template:
```bash
cp config/config.example.yaml ~/.maxinger15-music/config.yaml
```

Or use the interactive setup: `$maxinger15-music:configure`

## Settings

| Setting | Purpose | Default |
|---------|---------|---------|
| `artist.name` | Your artist/project name | (required) |
| `artist.genres` | Primary genres | `[]` |
| `paths.content_root` | Where albums/artists are stored | (required) |
| `paths.audio_root` | Where mastered audio goes | (required) |
| `paths.documents_root` | Where PDFs/primary sources go | (required) |
| `urls.soundcloud` | SoundCloud profile URL | (optional) |
| `generation.service` | Music generation service | `suno` |

## Path Structure

Content, audio, and documents use a mirrored directory structure:

```
{content_root}/artists/{artist}/albums/{genre}/{album}/    # Album files (git-tracked)
{audio_root}/artists/{artist}/albums/{genre}/{album}/      # Mastered audio
{documents_root}/artists/{artist}/albums/{genre}/{album}/  # Research PDFs
```

The `~/.maxinger15-music/` directory also contains the shared Python venv, cache files, and state.

See `config/README.md` for the full reference and `config/config.example.yaml` for all available options.
