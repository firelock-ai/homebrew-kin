# Security Policy

## Reporting a Vulnerability

Please report security vulnerabilities privately. **Do not open a public
issue for a suspected vulnerability.**

Use GitHub's private vulnerability reporting on this repository:

1. Go to the **Security** tab of
   [firelock-ai/homebrew-kin](https://github.com/firelock-ai/homebrew-kin/security).
2. Click **Report a vulnerability** to open a private security advisory.
3. Include a description, the affected formula or workflow, reproduction
   steps, the impact you observed, and the relevant Kin release and platform.

We will keep you informed as we investigate. Please give us a reasonable
opportunity to release a fix before any public disclosure.

There is no paid bug-bounty program at this time.

## Supported Versions

This tap tracks the latest supported Kin release. Only the formula and update
automation on the current `main` branch are supported; older formula revisions
are not patched. Security fixes to this tap ship on `main`.

| Version | Supported |
| ------- | --------- |
| Current `main` and formula | :white_check_mark: |
| Older formula revisions | :x: |

The Kin binaries installed by the formula follow the
[Kin security policy](https://github.com/firelock-ai/kin/security/policy).

## Scope

This policy covers the `homebrew-kin` repository: `Formula/kin.rb`, the formula
renderer, and the automation that validates and updates the tap from published
Kin releases.

For vulnerabilities in the installed Kin binaries, including the CLI, daemon,
MCP server, or VFS runtime, report them privately to
[firelock-ai/kin](https://github.com/firelock-ai/kin/security). If you are not
sure which repository owns the issue, report it here and the maintainers will
route it privately.
