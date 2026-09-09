# Homebrew Kin

Homebrew tap for [Kin](https://github.com/firelock-ai/kin), the semantic system of record for AI-written software.

## Install

```sh
brew install firelock-ai/kin/kin
```

The formula covers macOS (Apple Silicon + Intel) and Linux (x86_64 + arm64). It installs:

- **`kin`**, the CLI
- **`kin-daemon`**, the runtime (required by `kin status`, `kin search`, and the MCP server)
- **`kin-vfs`** + the VFS shim, the transparent filesystem projection

Then set up the shell and admit a repository. `brew install` leaves you with binaries and
no graph, so the first useful answer is three more commands:

```sh
kin setup
cd /path/to/your/repository
kin init .
kin locate "where are webhook retries handled"
```

`kin setup` writes the shell integration and configures the AI clients it detects. `kin
init` is the slow step and the one that earns the rest: it admits your Git history into the
graph, and every answer after it comes from that graph rather than from re-reading the
tree. Wire an AI agent after `kin init`, not before, so its first tool call has something
to answer from.

`kin --version` tells you what you actually got, and `kin doctor` reports what is healthy
and what needs a fix.

## Upgrade

```sh
brew update && brew upgrade kin
```

## How this tap stays current

`Formula/kin.rb` is a **generated artifact**. `scripts/render-formula.sh` renders it from a kin release, and [`.github/workflows/update-formula.yml`](.github/workflows/update-formula.yml) regenerates it on every kin release (via `repository_dispatch`) and on a 6-hour self-heal schedule, pulling each `sha256` straight from the published release assets. No human hand-edits a checksum, so the formula can't drift from what's published.

Generated updates mint a short-lived `kin-release-followup` App token scoped only
to this repository. The normal workflow token stays read-only; the App is the sole
unattended writer admitted by the protected-main ruleset.

## License

[Apache-2.0](LICENSE).
