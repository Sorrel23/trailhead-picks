---
layout: home
title: Latest picks
---
## Holiday gift guides

Shopping for an outdoorsy friend? Start with these researched gift lists, from stocking stuffers to splurges.

{% assign gifts = site.posts | where_exp: "p", "p.tags contains 'gift guide'" %}
<ul>
{%- for p in gifts limit: 6 %}
  <li><a href="{{ p.url | relative_url }}">{{ p.title }}</a></li>
{%- endfor %}
</ul>
