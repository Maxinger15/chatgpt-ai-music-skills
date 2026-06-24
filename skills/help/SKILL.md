---
name: help
description: "Shows available skills, common workflows, and quick reference for the plugin. Use when the user asks for help, what skills are available, or how to do something."
---

## maxinger15-music Plugin Help

Display this help information to the user in a clear, organized format.

---

### Getting Started

**New to the plugin?**
- `$maxinger15-music:tutorial` - Interactive guided album creation
- `$maxinger15-music:configure` - Set up configuration file
- `$maxinger15-music:about` - About maxinger15 and this plugin

**Resume existing work:**
- `$maxinger15-music:resume <album-name>` - Find an album and see status/next steps

---

### Skills by Category

**Album & Track Creation**
- `$maxinger15-music:album-ideas` - Track and manage album ideas
- `$maxinger15-music:promote-idea` - Convert a Pending idea into a full album (one-shot)
- `$maxinger15-music:new-album` - Create new album with directory structure
- `$maxinger15-music:album-conceptualizer` - Album concepts and tracklist architecture
- `$maxinger15-music:genre-creator` - Create and document a new genre reference
- `$maxinger15-music:lyric-writer` - Write/review lyrics, fix prosody
- `$maxinger15-music:lyric-refiner` - Multi-pass lyric refinement and refactoring
- `$maxinger15-music:suno-engineer` - Technical Suno prompting and genre selection

**Research & Sources**
- `$maxinger15-music:researcher` - Main research coordinator, fact-checking
- `$maxinger15-music:verify-sources` - Human source-verification gate before generation
- `$maxinger15-music:document-hunter` - Automated document search/download
- `$maxinger15-music:researchers-legal` - Court documents, indictments
- `$maxinger15-music:researchers-gov` - DOJ/FBI/SEC releases
- `$maxinger15-music:researchers-tech` - Project histories, changelogs
- `$maxinger15-music:researchers-journalism` - Investigative articles
- `$maxinger15-music:researchers-security` - Malware analysis, CVEs
- `$maxinger15-music:researchers-financial` - SEC filings, market data
- `$maxinger15-music:researchers-historical` - Archives, timelines
- `$maxinger15-music:researchers-biographical` - Personal backgrounds
- `$maxinger15-music:researchers-primary-source` - Tweets, blogs, forums
- `$maxinger15-music:researchers-verifier` - Quality control, citation validation

**Quality Control**
- `$maxinger15-music:lyric-reviewer` - Pre-generation QC gate (14-point checklist)
- `$maxinger15-music:pronunciation-specialist` - Scan for pronunciation risks
- `$maxinger15-music:explicit-checker` - Verify explicit content flags
- `$maxinger15-music:plagiarism-checker` - Check lyrics for phrases matching existing songs
- `$maxinger15-music:voice-checker` - Detect AI-written patterns in lyrics and prose
- `$maxinger15-music:pre-generation-check` - Final pre-generation checkpoint (6 gates)
- `$maxinger15-music:validate-album` - Validate album structure and paths

**Production & Release**
- `$maxinger15-music:album-art-director` - Visual concepts and AI art prompts
- `$maxinger15-music:mix-engineer` - Per-stem audio polish (cleanup, EQ, compression)
- `$maxinger15-music:mastering-engineer` - Audio mastering guidance
- `$maxinger15-music:promo-writer` - Write platform-specific social promo copy
- `$maxinger15-music:promo-reviewer` - Review and revise social media promo copy
- `$maxinger15-music:promo-director` - Generate promo videos for social media
- `$maxinger15-music:cloud-uploader` - Upload promo videos to Cloudflare R2 or AWS S3
- `$maxinger15-music:sheet-music-publisher` - Convert audio to sheet music
- `$maxinger15-music:release-director` - Release coordination and distribution

**File Management**
- `$maxinger15-music:import-track` - Move track .md files to album location
- `$maxinger15-music:import-audio` - Move audio files to album location
- `$maxinger15-music:import-art` - Place album art in correct locations
- `$maxinger15-music:rename` - Rename album/track with path updates
- `$maxinger15-music:clipboard` - Copy track lyrics/prompts to clipboard

**Workflow & Status**
- `$maxinger15-music:session-start` - Run session startup procedure
- `$maxinger15-music:next-step` - Get recommended next action
- `$maxinger15-music:album-dashboard` - Visual album progress dashboard

**System & Maintenance**
- `$maxinger15-music:setup` - Dependency/venv environment check and setup
- `$maxinger15-music:health-check` - Verify venv + skill registration health
- `$maxinger15-music:configure` - Edit plugin configuration
- `$maxinger15-music:test` - Run automated tests
- `$maxinger15-music:help` - Show this help (you are here!)
- `$maxinger15-music:about` - About maxinger15 and the plugin

---

### Common Workflows

**Creating a New Album:**
1. `$maxinger15-music:new-album <name> <genre>` - Create structure (or `$maxinger15-music:promote-idea "<idea title>"` if the idea lives in `IDEAS.md`)
2. Answer the 7 planning phases (concept, sonic direction, etc.)
3. Write lyrics for each track
4. Run `$maxinger15-music:lyric-reviewer` before generation
5. Generate in Suno, log results
6. Master audio with `$maxinger15-music:mastering-engineer`
7. [Optional] Generate promo videos with `$maxinger15-music:promo-director`
8. [Optional] Upload to cloud with `$maxinger15-music:cloud-uploader`
9. Release with `$maxinger15-music:release-director`

**True-Story Albums (with research):**
1. Use researcher skills to gather sources
2. All sources must be verified by human before production
3. Update track status from `❌ Pending` to `✅ Verified (DATE)`
4. Then proceed with lyric writing and generation

**Resume Existing Work:**
1. `$maxinger15-music:resume <album-name>` - Get detailed status
2. Follow the recommended next steps

---

### Quick Tips

- **Config file:** `~/.maxinger15-music/config.yaml` (always read this for paths)
- **Pronunciation:** Use phonetic spelling for tricky words (see pronunciation guide)
- **Explicit content:** Use flag for: fuck, shit, bitch, cunt, cock, dick, pussy, etc.
- **Mastering target:** -14 LUFS, -1.0 dBTP for streaming platforms
- **Promo videos:** Generate after mastering, 15s vertical (9:16) for social media
- **Track status flow:** Not Started → In Progress → Generated → Final
- **Album status flow:** Concept → In Progress → Complete → Released

---

### Key Documentation

- **AGENTS.md** - Main workflow instructions
- **README.md** - Project overview
- `{plugin_root}/reference/suno/` - Suno V5 guides, pronunciation, tips
- `{plugin_root}/reference/workflows/` - Detailed workflow procedures
- `{plugin_root}/reference/mastering/` - Audio mastering documentation
- `{plugin_root}/templates/` - Templates for new content
- `{plugin_root}/skills/[skill-name]/SKILL.md` - Individual skill documentation

---

### Getting Help

- Use this skill anytime: `$maxinger15-music:help`
- For tutorial: `$maxinger15-music:tutorial`
- For status: `$maxinger15-music:resume <album-name>`
- Ask Codex: "What should I do next?" for guidance
