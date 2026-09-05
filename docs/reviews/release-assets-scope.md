# Release assets review scope

This document defines the review boundary for the release automation in pull request #45. The change establishes reproducible, checksummed macOS and Linux archives for the existing `ubt`, `ubtctl`, and `ubtd` programs. It does not publish a release by itself.

## Included

- A GoReleaser v2 configuration that builds the three existing programs for:
  - macOS on AMD64 and ARM64
  - Linux on AMD64 and ARM64
- Four stable archive names of the form `universal-bluetooth-sdk_<os>_<arch>.tar.gz`.
- The `ubt`, `ubtctl`, and `ubtd` binaries, plus `README.md` and `LICENSE.txt`, in every archive.
- A SHA-256 checksum manifest named `checksums.txt`.
- A tag-triggered GitHub Actions workflow that:
  - accepts semantic version tags with optional `alpha`, `beta`, or `rc` suffixes;
  - requires the tagged commit to be reachable from `origin/master`;
  - grants release write permission only to the publishing job; and
  - runs the pinned GoReleaser action and GoReleaser version.
- A non-publishing CI snapshot job that verifies all expected archives, archive members, and checksums before release automation can be merged.

## Excluded

- Creating or pushing a release tag.
- Publishing or approving a GitHub Release.
- The curl installer tracked by issue #41.
- The mise integration tracked by issue #42.
- The Homebrew tap tracked by issue #43.
- The stable installer URL tracked by issue #44.
- Bun or npm distribution.
- Windows or PowerShell installation.
- macOS code signing or notarization, Linux package signing, provenance attestations, or SBOM publication.
- Runtime Bluetooth and hardware qualification.

## Reviewer roadmap

Review the change in this order:

1. [`.goreleaser.yml`](../../.goreleaser.yml) defines the public artifact contract: binaries, platforms, names, version injection, archive contents, and checksums.
2. [`.github/workflows/release.yml`](../../.github/workflows/release.yml) defines the publication boundary: accepted tags, master ancestry, permissions, and pinned tooling.
3. [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) proves the same configuration can build without publishing and verifies the resulting artifact shape.
4. [`.gitignore`](../../.gitignore) keeps local snapshot output out of source control.
5. Review the rendered [sequence](release-assets/sequence.svg), [architecture](release-assets/architecture.svg), and [reviewer roadmap](release-assets/reviewer-roadmap.svg) diagrams against those files.

## Invariants

- All binaries in a release are built from the tagged commit and report the tag-derived version.
- `ubt` and `ubtctl` remain two executable names built from the same `./cli/ubtctl` source package.
- Every supported archive contains exactly the three expected executables and the two repository documents.
- A branch push or pull request cannot publish a release.
- An invalid tag or a tag outside `master` history cannot publish a release.
- The snapshot job does not receive repository write permission.
- The checksum manifest verifies the archive bytes published with the release.
- The four archive names remain independent of the GoReleaser version and build host.

## Failure behavior

- Invalid tags stop before GoReleaser runs.
- A tag whose commit is not reachable from `origin/master` stops before GoReleaser runs.
- A compile, archive, or checksum failure fails the workflow and prevents a successful release job.
- A missing archive, unexpected archive member, or checksum mismatch fails pull-request CI.
- No fallback path publishes unverified locally built files.

GitHub can still contain a draft or partial release if the hosting service fails during upload. A maintainer must inspect the release page and its assets before announcing it.

## Rollout gates

1. Merge pull request #45 only after Linux and macOS tests and the release snapshot job pass for its exact head commit.
2. Create the next version tag only with explicit maintainer approval.
3. Confirm the GitHub Release contains four archives plus `checksums.txt` and verify at least one downloaded archive independently.
4. Implement the installer and package-manager issues against the verified asset contract.
5. Add signing, attestations, or platform packaging as separate reviewed changes if the project requires those guarantees.

## Evidence limits

Snapshot builds prove compilation, archive layout, and checksum consistency in GitHub Actions. They do not prove installation on every supported operating-system version, Bluetooth hardware behavior, macOS trust prompts, package-manager integration, or successful publication by GitHub Releases.
