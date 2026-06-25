# Homebrew Kin

Homebrew tap for [Kin](https://github.com/firelock-ai/kin) — the semantic system of record for software work.

## Install

```sh
brew install firelock-ai/kin/kin
```

The formula covers macOS (Apple Silicon + Intel) and Linux (x86_64 + arm64). It installs:

- **`kin`** — the CLI
- **`kin-daemon`** — the runtime (required by `kin status`, `kin search`, and the MCP server)
- **`kin-vfs`** + the VFS shim — the transparent filesystem projection

Then run `kin setup` to configure your shell and `kin doctor` to verify the install.

## Upgrade

```sh
brew update && brew upgrade kin
```

## How this tap stays current

`Formula/kin.rb` is a **generated artifact**. `scripts/render-formula.sh` renders it from a kin release, and [`.github/workflows/update-formula.yml`](.github/workflows/update-formula.yml) regenerates it — pulling each `sha256` straight from the published release assets — on every kin release (via `repository_dispatch`) and on a 6-hour self-heal schedule. No human hand-edits a checksum, so the formula can't drift from what's published.

## License

[Apache-2.0](LICENSE).
