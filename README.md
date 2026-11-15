# Trailhead Picks

Amazon-affiliate outdoor gear site (Jekyll on GitHub Pages). A daily Claude run researches a topic, writes one post and pushes it; a GitHub Action validates it and pins it to Pinterest.

- Tracking ID lives in `_config.yml` → `amazon_tag`.
- Editorial rules: `STRATEGY.md`. Validator: `scripts/check_post.py`.
- Pinterest pins: `.github/workflows/pin-new-posts.yml` (needs repo secret `PINTEREST_TOKEN` (or app id/secret/refresh token); pins go to the "Outdoor Gear & Gift Ideas" board). Without secrets it just skips pinning.
