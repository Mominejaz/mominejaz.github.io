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
