# Configure Skill - Settings Reference

Quick lookup for all configuration options. Full documentation: [{plugin_root}/config/README.md]({plugin_root}/config/README.md).

---

## Config File Location

```
~/.maxinger15-music/config.yaml
```

---

## Required Settings

| Setting | Description | Example |
|---------|-------------|---------|
| `artist.name` | Your artist/project name | `"maxinger15"` |
| `paths.content_root` | Albums, artists, research | `"~/music-projects"` |
| `paths.audio_root` | Mastered audio output | `"~/music-projects/audio"` |
| `paths.documents_root` | PDFs, primary sources | `"~/music-projects/documents"` |

---

## Optional Settings

### Artist Info

| Setting | Description | Example |
|---------|-------------|---------|
| `artist.genres` | Primary genres (array) | `["electronic", "hip-hop"]` |
| `artist.style` | Brief style description | `"dark industrial electronic"` |

**Tip**: `artist.style` helps Codex understand your overall vibe for consistent suggestions.

### Paths

| Setting | Description | Default |
|---------|-------------|---------|
| `paths.overrides` | Custom workflow overrides | `{content_root}/overrides` |
| `paths.ideas_file` | Album ideas tracking | `{content_root}/IDEAS.md` |

**Tip**: Override files let you customize skills without plugin update conflicts.

### Platform URLs

| Setting | Description |
|---------|-------------|
| `urls.soundcloud` | SoundCloud profile |
| `urls.spotify` | Spotify artist page |
| `urls.bandcamp` | Bandcamp page |
| `urls.youtube` | YouTube channel |
| `urls.twitter` | Twitter/X profile |

**Tip**: Used by release-director for post-release workflows.

### Generation Service

| Setting | Description | Default |
|---------|-------------|---------|
| `generation.service` | Music generation service | `suno` |

Currently only Suno is supported.

---

## Feature-Specific Settings

### Promo Videos (`promotion:`)

For `$maxinger15-music:promo-director`:

| Setting | Description | Default |
|---------|-------------|---------|
| `promotion.default_style` | Visualization style | `pulse` |
| `promotion.duration` | Video duration (seconds) | `15` |
| `promotion.include_sampler` | Generate album sampler | `true` |
| `promotion.sampler_clip_duration` | Seconds per track in sampler | `12` |

**Styles**: pulse, bars, line, mirror, mountains, colorwave, neon, dual, circular

### Sheet Music (`sheet_music:`)

For `$maxinger15-music:sheet-music-publisher`:

| Setting | Description | Default |
|---------|-------------|---------|
| `sheet_music.page_size` | Page size | `letter` |
| `sheet_music.section_headers` | Include [Verse] labels | `false` |

**Page sizes**: letter, 9x12, 6x9

### Cloud Storage (`cloud:`)

For `$maxinger15-music:cloud-uploader`:

| Setting | Description |
|---------|-------------|
| `cloud.enabled` | Enable cloud uploads |
| `cloud.provider` | `r2` or `s3` |
| `cloud.public_read` | Make uploads public |

Provider-specific keys documented in [{plugin_root}/reference/cloud/setup-guide.md]({plugin_root}/reference/cloud/setup-guide.md).

---

## Quick Commands

```bash
# Show current config
$maxinger15-music:configure show

# Edit a specific setting
$maxinger15-music:configure edit

# Validate config for issues
$maxinger15-music:configure validate

# Start fresh
$maxinger15-music:configure reset
```

---

## Common Patterns

### Minimal Config

```yaml
artist:
  name: "my-artist"

paths:
  content_root: "~/music-projects"
  audio_root: "~/music-projects/audio"
  documents_root: "~/music-projects/documents"
```

### Full Config

See [{plugin_root}/config/config.example.yaml]({plugin_root}/config/config.example.yaml) for complete example with all options.

---

## See Also

- [SKILL.md](SKILL.md) - Full skill documentation
- [{plugin_root}/config/README.md]({plugin_root}/config/README.md) - Complete config reference with examples
- [{plugin_root}/config/config.example.yaml]({plugin_root}/config/config.example.yaml) - Example config file
