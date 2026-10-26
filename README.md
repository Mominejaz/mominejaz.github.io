# Momin Ejaz portfolio

Static portfolio source prepared for GitHub Pages. The published files live in `dist/`, so no build step is required.

## Site structure

- `dist/index.html` is the main portfolio page, including project filters, the MeTech consulting section, and the experience timeline.
- `dist/projects/<slug>/index.html` contains one static case-study page per project.
- `dist/assets/styles.css` contains the responsive design and print styles.
- `dist/assets/site.js` handles the menu, project filters, section reveals, and active navigation.
- `dist/assets/background.js` draws the decorative hero background. Visitors can pause it; the page also honours reduced-motion preferences and stops rendering when hidden or offscreen.

All operational-system visuals use fictionalized, synthetic data. Review professional project wording and examples against employer publication requirements before publishing.

## Local preview

From this directory:

```powershell
python -m http.server 4173 --directory dist
```

Open `http://localhost:4173`.

## GitHub Pages

Create a dedicated public repository for this `site` folder, including its `.github` folder and `dist` folder. Push it to `main`, then open **Settings → Pages** and select **GitHub Actions** as the publishing source. The included workflow deploys `dist/` after each push to `main`.

If the repository is named `<your-github-username>.github.io`, the site will be available at `https://<your-github-username>.github.io/`. A differently named repository is normally served from `https://<your-github-username>.github.io/<repository-name>/`.

Before publishing, review all professional project wording against employer publication requirements.

## Public evidence and assets

- `dist/demos/inventory-review/` is a self-contained, fictional workflow demonstration. It is not the professional application; all state stays in memory in the visitor's browser.
- `dist/assets/demo.js` implements review, exception resolution, snapshot locking, JSON download, and reset.
- `content/resume.md` is the reviewed public resume source, using the current contact email and omitting unsupported numeric improvement claims.
- `tools/build_resume.py` generates the two-page PDF from an explicit source and destination; `tools/build_assets.py` uses it for the public PDF and also generates the 1200 x 630 social-sharing image (requires reportlab, Pillow, and Windows Arial fonts). Visually review regenerated assets before committing them.
- Version query strings on asset URLs prevent returning visitors from mixing old styles with updated markup. Increment them when changing public styles or scripts.
