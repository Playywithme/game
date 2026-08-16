# Play With Me Reveal Puzzles

Static GitHub Pages gender-reveal puzzle games.

## Live Paths

- `https://playywithme.github.io/game/boy/`
- `https://playywithme.github.io/game/girl/`
- `https://playywithme.github.io/game/twins/`

Each variant is a separate folder with its own `index.html`. There is no backend,
database, personalization form, query string, or URL-encoded data.

## Editing

Open the variant file you want to change:

- `boy/index.html`
- `girl/index.html`
- `twins/index.html`

At the bottom of each file, edit the config constants:

```html
const GAME_URL = "https://playywithme.github.io/game/boy/";
const REVEAL_MESSAGE = "Congratulations — it's a boy! 💙";
```

Moving to a custom domain later only requires changing `GAME_URL` in the
variant file and regenerating that variant's PDF link.

## PDFs

Static wrappers live in `pdfs/`. To regenerate them after changing a URL, run:

```powershell
python tools/create_fixed_variant_pdfs.py
```
