# Developer Documentation

Internal notes for maintaining this repo, its CI pipeline, and release flow.

---

## CI Pipeline

Three workflows coordinate to keep the add-on current upstream MCPO releases:

| Workflow | File | Trigger | Purpose |
|---|---|---|---|
| **Lint** | `.github/workflows/lint.yaml` | Push/PR to `main` | Validates add-on config schema |
| **Sync MCPO Version** | `.github/workflows/mcpo-sync.yaml` | Daily at 06:00 or manual dispatch | Checks for new upstream MCPO release; patches version bump + tags |
| **Build & Publish App** | `.github/workflows/builder.yaml` | `mcpo-*` tag push or manual dispatch | Builds multi-arch Docker image, pushes to GHCR |

### Flow

```
mcpo-sync (daily) → detects new MCPO version → patches config + Dockerfile → creates mcpo-{ver} tag → pushes to main
    ↓
builder (on mcpo-* tag) → builds aarch64 + amd64 images → signs with cosign → publishes to GHCR
```

---

## Tagging Scheme

We use `mcpo-*` tags (e.g. `mcpo-0.0.20`) to mark each MCPO wrapper release. The builder workflow listens for these tags and triggers a new image build automatically.

### Why not rely on main branch pushes?
Almost all commits to `main` are docs, lint fixes, or housekeeping — none of which need a new Docker image. Tag-only builds ensures we only publish images when MCPO actually moves.

### What if a tag push doesn't trigger the build?
GitHub occasionally misses a tag trigger when workflow configs have been recently changed (cache race). In that case, use `workflow_dispatch` on the builder to rebuild manually:

```bash
gh workflow run builder.yaml --ref main
```

The dispatch always works regardless of tag state. This is why both triggers are kept.

---

## Rebuilding / Retagging

If a build fails or you need to rebuild an existing version:

1. **Don't delete and recreate the tag** — it loses commit provenance and can confuse GHCR
2. **Use workflow dispatch instead** — the builder accepts manual runs independent of tags:
   ```bash
   gh workflow run builder.yaml --ref main
   ```
3. If you *must* retag (e.g., the wrong tag landed), delete + recreate, then force-push:
   ```bash
   git tag -d mcpo-X.Y.Z && git push origin :refs/tags/mcpo-X.Y.Z
   git tag mcpo-X.Y.Z <commit> && git push origin --tags
   ```

---

## GHCR Package Management

Images are published to `ghcr.io/thespacegod/mcpo-hass-app`. Version bumps create new image tags in the registry. Old orphaned images (from earlier tagging schemes or failed builds) accumulate over time.

### Cleaning orphaned images

1. Go to GitHub → repository Settings → Packages
2. Find **mcpo-hass-app** under Container Registry packages
3. Remove any versions with stale tags (`v*`, `*-dev`, etc.)
4. Keep only current `mcpo-*` versioned tags + `latest`

### Setting retention policy

On the same page under the package details, set a **Retention Policy** to auto-expire old versions:
- Keep 20 most recent versions
- Delete all other versions after 90 days

This prevents unbounded growth in the registry.

---

## Local Development

Tests run with `uv`:

```bash
uv run pytest tests/
```

### Building locally

```bash
docker build --tag mcpo-local ./mcpo
docker run --rm --publish 80:8000 -e MCP_SERVERS='{"example": {"type": "streamable-http", "url": "http://..."}}' mcpo-local
```

### Modifying the Dockerfile base image

Change `ARG BUILD_FROM` in `mcpo/Dockerfile`. Pin to a specific Home Assistant base version rather than letting builder override it.

---

## Troubleshooting CI

| Symptom | Likely cause | Fix |
|---|---|---|
| Tag push doesn't trigger build | Workflow engine cached old config | Manually dispatch builder via `gh workflow run builder.yaml --ref main` or re-push tag |
| `persist-credentials: true` deprecation warning in mcpo-sync | Git checkout action deprecated this option | Replace with explicit PAT token via `token:` in the future (low priority — works today) |
| Image pushes to GHCR fail | Token lacks `packages: write` scope — ensure GitHub Actions permissions are enabled in repo settings → Actions → Read/Write access |
