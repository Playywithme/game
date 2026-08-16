# Play With Me Puzzle

GitHub Pages wrapper for the hosted customizable puzzle game.

## Public URLs

- Buyer customizer: `https://playywithme.github.io/game/customize.html`
- Personalized game links: `https://playywithme.github.io/game/?c=<ENCODED>`
- Older direct game path: `https://playywithme.github.io/game/game.html?c=<ENCODED>`

## How It Works

The GitHub Pages files are lightweight wrappers. They forward the visitor and the full query string to the hosted game/customizer.

All personalization is stored in the URL parameter `c`, which is base64-url encoded JSON. There is no backend and no database.
