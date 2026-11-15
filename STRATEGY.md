# Trailhead Picks — editorial playbook (read by the daily publishing run)

**Niche:** outdoor gear for hikers, campers and cold-weather adventurers (the Associates tracking ID is `outdoorexp-20`).
**Audience:** gift-givers and beginner-to-intermediate outdoorspeople who find us through Pinterest and Google.
**Traffic engine:** each post → one auto-generated Pinterest pin linking to the post (GitHub Action). Posts also build Google search traffic over months.

## Rules (Amazon Associates + FTC + honesty)
1. Every Amazon link uses `{% include amzn.html asin="..." %}` or `{% include amzn.html q="..." %}`. Never raw amazon.com URLs, never shorteners.
2. Use an ASIN only if you saw it in an amazon.com `/dp/ASIN` URL **for that exact product** during this run's research. Otherwise use a `q="brand model"` search link (always works, still earns).
3. No prices, no star ratings, no "deal" claims (they go stale and Amazon restricts showing them outside its API). Words like "budget", "splurge" are fine.
4. Never claim hands-on testing. We research: specs, owner reviews, published expert testing, and we credit the outlet when citing a test result ("in Outdoor Life's testing…").
5. Original commentary is required (Amazon's April 2026 policy): for each pick say **why it works, who should skip it, and a buying tip**. No copied manufacturer text and no quotes over 15 words.
6. Never run paid ads to Amazon links (purchases from paid ads don't earn under the April 2026 agreement).
7. No weapons, ammo, knives marketed for fighting, or supplements/medical claims.

## Seasonal calendar
| Window | Focus |
|---|---|
| Nov 15 – Dec 20 | Gift guides: by recipient (hikers, campers, backpackers, dads, kids, beginners), by budget (stocking stuffers, under-$50 *without listing prices*), last-minute |
| Dec 21 – Feb | Winter hiking, snowshoeing, traction, layering, staying warm, New Year "start hiking" guides |
| Mar – Apr | Spring camping prep, beginner camping checklists, backpacking gear lists, rain gear |
| May – Jun | Camping season, Mother's/Father's Day outdoor gifts, hammocks, camp kitchen |
| Jul – Aug | Summer heat/water gear, family camping, lake/river trips, Prime Day gear picks (no prices) |
| Sep – Oct | Fall hiking, layering, headlamps for shorter days, early holiday gift guides |

## Post formats (rotate; don't repeat a format two days running)
- **Gift guide** – 8–12 picks grouped by type/budget.
- **Best X for Y** – 5–8 picks for one job ("best headlamps for winter hiking").
- **Checklist** – "what to pack for…" with 8–15 linked items.
- **Problem → fix** – "how to keep your hands warm on winter hikes" with 4–6 products woven into practical advice.

## Post spec
- File `_posts/YYYY-MM-DD-slug.md`, slug = main keyword phrase, lowercase-hyphenated.
- Front matter: `layout: post`, `title` (keyword first, ≤ 65 chars), `date`, `description` (≤ 155 chars), `pin_title` (≤ 60 chars, punchy), `pin_text` (≤ 70 chars), `keywords`, `tags`.
- 600–1,200 words, ≥ 3 Amazon links (5–10 typical), each pick in a `<div class="pick" markdown="1">` block.
- Must pass `python3 scripts/check_post.py <file>`.
- Log it in `_data/topics.json`: `{"date","slug","format","keyword"}`. Never publish a keyword already in the log.
