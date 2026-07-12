#!/usr/bin/env python3
"""Fail closed when the Kin release correlation or formula authority drifts."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / ".github" / "workflows" / "update-formula.yml"


def require(content: str, policy: str) -> None:
    if policy not in content:
        raise AssertionError(f"update-formula.yml is missing policy: {policy}")


def main() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    for policy in (
        "repository_dispatch:",
        "types: [kin-release]",
        "schedule:",
        "workflow_dispatch:",
        "Update formula {0} from Kin run {1}",
        "Legacy Kin release reconciliation",
        "Scheduled formula reconciliation",
        "Break-glass formula reconciliation",
        "actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0",
        "DISPATCH_SCHEMA_VERSION: ${{ github.event.client_payload.schema_version || '' }}",
        "DISPATCH_KIN_TAG: ${{ github.event.client_payload.kin_tag || '' }}",
        "DISPATCH_KIN_SHA: ${{ github.event.client_payload.kin_sha || '' }}",
        "DISPATCH_RUN_ID: ${{ github.event.client_payload.release_workflow_run_id || '' }}",
        'tag=$(gh release view --repo firelock-ai/kin --json tagName -q .tagName)',
        '[ "$DISPATCH_SCHEMA_VERSION" = 1 ]',
        '[[ "$DISPATCH_KIN_SHA" =~ ^[0-9a-f]{40}$ ]]',
        '[[ "$DISPATCH_RUN_ID" =~ ^[0-9]+$ ]]',
        '[ "$DISPATCH_KIN_TAG" = "$tag" ]',
        'repos/firelock-ai/kin/actions/runs/${DISPATCH_RUN_ID}',
        '[ "$(jq -r .status <<< "$release_run")" = completed ]',
        '[ "$(jq -r .conclusion <<< "$release_run")" = success ]',
        '[ "$(jq -r .path <<< "$release_run")" = .github/workflows/release.yml ]',
        '[ "$(jq -r .head_branch <<< "$release_run")" = "$DISPATCH_KIN_TAG" ]',
        '[ "$(jq -r .head_sha <<< "$release_run")" = "$DISPATCH_KIN_SHA" ]',
        'repos/firelock-ai/kin/git/ref/tags/${DISPATCH_KIN_TAG}',
        '[ "$object_type" = commit ]',
        '[ "$peeled" = "$DISPATCH_KIN_SHA" ]',
        'repos/firelock-ai/kin/releases/tags/${DISPATCH_KIN_TAG}',
        '[ "$(jq -r .draft <<< "$release")" = false ]',
        '[ "$(jq -r .prerelease <<< "$release")" = false ]',
        'repos/firelock-ai/kin/releases/latest',
        '[ "$release_id" = "$latest_id" ]',
        "legacy kin-release dispatch without correlation payload",
        "ruby -c Formula/kin.rb",
        "git push",
    ):
        require(workflow, policy)

    if 'tag="$DISPATCH_KIN_TAG"' in workflow:
        raise AssertionError(
            "the formula must rederive GitHub Latest instead of trusting dispatch data"
        )
    secret_names = set(re.findall(r"secrets\.([A-Za-z0-9_]+)", workflow))
    if secret_names != {"GITHUB_TOKEN"}:
        raise AssertionError(
            "update-formula.yml must use only the ephemeral repository token; "
            f"found {sorted(secret_names)}"
        )

    print(
        "Homebrew formula workflow correlates exact Kin callbacks while retaining "
        "scheduled, manual, and legacy reconciliation"
    )


if __name__ == "__main__":
    main()
