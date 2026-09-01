> **Umbrella guidance:** the workspace-root `AGENTS.md` is the source of truth for cross-repo thesis, boundaries, and rules. This file is the repo-specific authority for `homebrew-kin`.

# homebrew-kin

The Homebrew distribution tap for kin (manifest layer `infrastructure`, role
`homebrew-distribution-tap`). It carries one formula and the script that generates it. Nothing about
kin's behaviour belongs here; this repo only decides what `brew install` fetches.

## The formula is generated, never hand-edited

`Formula/kin.rb` is output. `scripts/render-formula.sh <version> <sha_macos_arm> <sha_macos_intel>
<sha_linux_intel> <sha_linux_arm>` writes it, interpolating the release-asset URLs from that one
version. Hand-editing it is how the sha256s drift from the published assets, the failure the
generator exists to prevent. Change the template inside the script, then regenerate.

`.github/workflows/update-formula.yml` runs the generator for real. It fires on a
`repository_dispatch` of type `kin-release`, sent by kin's completed-release callback, and on a
`17 */6 * * *` schedule as a self-heal in case a dispatch is ever missed.

## Gates

One graded job, `policy`, which is the required context on main:

```bash
python3 scripts/test-update-formula-workflow.py   # release correlation policy
bash -n scripts/render-formula.sh                 # renderer parses
ruby -c Formula/kin.rb                            # current formula parses
```

A second job, `run-lookup-guard`, comes from kin-actions pinned to a commit. It fails when a
verification input resolves a specific past Actions run, because run history is deletable. This repo
claims no exemption and passes no allowlist.

## Two traps when you check what a user actually gets

Both are in the umbrella's `docs/traps.md`, and both make a stale read look exactly like a publish
leg that never fired.

**A `raw.githubusercontent.com/<owner>/<repo>/main/<path>` read is CDN-cached for up to five
minutes,** so it can serve the previous commit's bytes with a 200. On 2026-08-26 this formula was
bumped to 0.6.0 at 21:53:55Z and a raw/main read minutes later still returned the old version. Pin
the ref to a sha, or read through the API, before concluding the tap is behind.

**The tap has a phantom `master` branch.** `repos/firelock-ai/homebrew-kin/branches/master` does not
404; it answers with `main`'s branch object. A check that reads `master` therefore succeeds while
telling you nothing about the branch that exists.

## Landing

Hosted merge queue, ruleset `Merge queue on main`, active, alongside `Protect Homebrew main` and
`Freeze Homebrew main history`. The one required status context is `policy`, from the ruleset rather
than classic protection, which returns no contexts here. The queue mints the squash commit verbatim
from the PR title and body, so get both right before arming. From the umbrella root,
`bin/kin-lane merge enqueue homebrew-kin <lane> <pr>` then
`bin/kin-lane merge land homebrew-kin <lane> <pr>`. Commit with `git commit -s`.
