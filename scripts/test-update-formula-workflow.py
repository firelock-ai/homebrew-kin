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
        "Update formula {0} from Kin run {1}",
        "Legacy Kin release reconciliation",
        "Scheduled formula reconciliation",
        "actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0",
        "ref: main",
        "persist-credentials: false",
        "Require exact current main",
        '[ "$GITHUB_REF" = refs/heads/main ]',
        "repos/firelock-ai/homebrew-kin/git/ref/heads/main",
        '[ "$(git rev-parse HEAD)" = "$current" ]',
        "DISPATCH_SCHEMA_VERSION: ${{ github.event.client_payload.schema_version || '' }}",
        "DISPATCH_KIN_TAG: ${{ github.event.client_payload.kin_tag || '' }}",
        "DISPATCH_KIN_SHA: ${{ github.event.client_payload.kin_sha || '' }}",
        "DISPATCH_RUN_ID: ${{ github.event.client_payload.release_workflow_run_id || '' }}",
        'tag=$(gh release view --repo firelock-ai/kin --json tagName -q .tagName)',
        '[ "$DISPATCH_SCHEMA_VERSION" = 1 ]',
        '[[ "$DISPATCH_KIN_SHA" =~ ^[0-9a-f]{40}$ ]]',
        '[[ "$DISPATCH_RUN_ID" =~ ^[0-9]+$ ]]',
        '[ "$DISPATCH_KIN_TAG" = "$tag" ]',
        'ghcr.io/firelock-ai/kin:${DISPATCH_KIN_SHA}',
        '[[ "$digest" =~ ^sha256:[0-9a-f]{64}$ ]]',
        'gh attestation verify "oci://ghcr.io/firelock-ai/kin@${digest}"',
        "--repo firelock-ai/kin",
        "--bundle-from-oci",
        "--predicate-type https://slsa.dev/provenance/v1",
        "--signer-workflow firelock-ai/kin/.github/workflows/release.yml",
        '--signer-digest "$DISPATCH_KIN_SHA"',
        '--source-digest "$DISPATCH_KIN_SHA"',
        '--source-ref "refs/tags/${DISPATCH_KIN_TAG}"',
        "--deny-self-hosted-runners",
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
        "gh auth setup-git",
        "git push origin HEAD:main",
    ):
        require(workflow, policy)

    # An Actions run record is not durable evidence: it ages out of retention,
    # it can be deleted outright, and it never proved which artifact a run
    # produced. Both the single-run form and the workflow-scoped runs-list form
    # are refused so neither can come back as a correlation input.
    for banned in ("actions/runs/", "/runs?"):
        if banned in workflow:
            raise AssertionError(
                "the formula must correlate a release from its signed "
                f"attestation, not from a workflow run record: {banned}"
            )

    # The attestation is only meaningful once the tag is proven to peel to the
    # commit whose image is being verified.
    if workflow.index('[ "$peeled" = "$DISPATCH_KIN_SHA" ]') > workflow.index(
        "gh attestation verify"
    ):
        raise AssertionError(
            "the release tag must peel to the dispatched commit before that "
            "commit's image attestation is verified"
        )

    if 'tag="$DISPATCH_KIN_TAG"' in workflow:
        raise AssertionError(
            "the formula must rederive GitHub Latest instead of trusting dispatch data"
        )
    if "workflow_dispatch:" in workflow:
        raise AssertionError(
            "the mutating Homebrew workflow must not expose branch-selectable "
            "manual dispatch"
        )
    secret_names = set(re.findall(r"secrets\.([A-Za-z0-9_]+)", workflow))
    if secret_names != {"GITHUB_TOKEN"}:
        raise AssertionError(
            "update-formula.yml must use only the ephemeral repository token; "
            f"found {sorted(secret_names)}"
        )

    print(
        "Homebrew formula workflow correlates exact Kin callbacks while retaining "
        "scheduled and legacy reconciliation"
    )


if __name__ == "__main__":
    main()
