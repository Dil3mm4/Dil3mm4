# GitHub profile setup

This package targets the existing public profile repository **[Dil3mm4/Dil3mm4](https://github.com/Dil3mm4/Dil3mm4)**, whose default branch is `main`.

The README displays two matching, repository-local SVG cards. Its Android diagram runs **top to bottom**, from **01 Linux Kernel** to **06 Production**, and the description reads exactly:

> Custom Android platforms, low-level engineering, technical direction and product architecture.

Both cards share their palette in `scripts/render_profile.py`. They use native vector shapes and system font fallbacks: no external fonts, CSS imports, image hosts or third-party widgets.

## Publish (macOS / Linux)

Download `github-profile.zip` and run these commands from the directory where you saved it (for example `~/Downloads`):

```bash
unzip -o github-profile.zip
git clone https://github.com/Dil3mm4/Dil3mm4.git
cp -R github-profile/. Dil3mm4/
cd Dil3mm4
git add README.md SETUP.md assets scripts .github/workflows/update-profile-stats.yml
git commit -m "Update GitHub profile cards"
git push origin main
```

If you already have `Dil3mm4` cloned locally, skip the `git clone` step and copy into your existing clone. Copying the package replaces your current profile README and files with the same paths; other files in the repository stay untouched. You must have GitHub authentication set up for `git push` (for example Git Credential Manager, the GitHub CLI, or SSH).

Open https://github.com/Dil3mm4 after pushing to view the profile.

## Populate the stats card

1. Open https://github.com/Dil3mm4/Dil3mm4/actions.
2. Choose **Update profile stats** and select **Run workflow** on `main`.
3. If the commit step is denied, check **Settings → Actions → General → Workflow permissions** and allow read and write permissions if available. The workflow requests `contents: write`.

The workflow updates `assets/github-stats.svg` daily, using only GitHub Actions, GitHub's REST API, native `git`, and Python's standard library. Public metrics can differ from the old hosted widget because the counting methodology differs. Initial dashes are intentional until the first successful sync; private contributions are not read.

## Local edits

To change the palette, layout or text, modify `scripts/render_profile.py`. Then regenerate the architecture graphic without clearing the populated stats:

```bash
python3 scripts/render_profile.py --hero-only
```

The stats generator is `scripts/update_stats.py`; it can also be run locally with a `GITHUB_TOKEN` in the environment:

```bash
python3 scripts/update_stats.py --login dil3mm4
```
