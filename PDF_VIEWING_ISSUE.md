# PDF not rendering on GitHub?

If a PDF in this repo shows a blank preview, spins forever, or displays **"Unable to render rich display"** / **"Sorry, we cannot display this file"** — this is a known, recurring issue with GitHub's in-browser PDF renderer. It is **not** a corrupted or broken file.

## Quick fixes (try in this order)

1. **Click "Download" or "View raw"** at the top of the file page. If the file opens fine outside GitHub, the PDF itself is fine — it's purely a display glitch.
2. **Hard refresh the page**, or open it in an **incognito/private window**. GitHub's renderer is served from a separate subdomain (`raw.githubusercontent.com` / a rendering iframe) that occasionally times out independently of github.com itself.
3. **Try a different browser**, or wait a few minutes and reload — this is a widely reported, server-side GitHub issue (see [community discussion #42258](https://github.com/orgs/community/discussions/42258)) that often resolves on its own.
4. **Clone the repo locally** and open the PDF directly if you need guaranteed access right away:
   ```bash
   git clone <repo-url>
   ```

## Why this happens

GitHub's rich-display preview for PDFs (and other file types like Jupyter notebooks and Mermaid diagrams) runs through a separate rendering pipeline from the raw file storage. When that pipeline is slow, overloaded, or times out, GitHub shows a generic "unable to render" message even though the underlying file is completely intact. Larger or more complex PDFs are somewhat more prone to this, but it has also been reported for small files.

## Not the cause

- ❌ The file is not corrupted (downloading/opening it directly will confirm this)
- ❌ It is not something wrong with how the PDF was created or uploaded
- ❌ It is not specific to one repo or one file — it happens across GitHub broadly and comes and goes

---
*Reusable note — copy this file into any repo where PDF previews act up.*
