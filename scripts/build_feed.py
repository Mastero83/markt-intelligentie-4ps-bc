#!/usr/bin/env python3
"""Valideert data/updates.json en genereert feed.xml (RSS 2.0), nieuwste eerst."""
import json
import re
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "updates.json"
FEED = ROOT / "feed.xml"
REPO_URL = "https://github.com/Mastero83/markt-intelligentie-4ps-bc"

VERPLICHT = {
    "id": str, "datum": str, "gemeld_op": str, "onderwerp": str,
    "samenvatting": str, "relevantie": str, "categorie": str,
    "tags": list, "bronnen": list, "bron_type": str,
}
CATEGORIEEN = {"product_release", "concurrentie", "partners", "prijzen_licenties",
               "ai_features", "markt", "regelgeving", "events"}
BRON_TYPES = {"dagelijkse_radar", "basisanalyse"}
DATUM_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def valideer(items):
    fouten = []
    if not isinstance(items, list):
        return ["updates.json moet een JSON-array zijn"]
    gezien = set()
    for i, it in enumerate(items):
        label = f"item {i} ({it.get('id', '?') if isinstance(it, dict) else '?'})"
        if not isinstance(it, dict):
            fouten.append(f"{label}: geen object"); continue
        for veld, typ in VERPLICHT.items():
            if veld not in it:
                fouten.append(f"{label}: verplicht veld '{veld}' ontbreekt")
            elif not isinstance(it[veld], typ):
                fouten.append(f"{label}: veld '{veld}' moet {typ.__name__} zijn")
        if isinstance(it.get("id"), str):
            if not it["id"].strip():
                fouten.append(f"{label}: lege id")
            if it["id"] in gezien:
                fouten.append(f"{label}: dubbele id '{it['id']}'")
            gezien.add(it["id"])
        for veld in ("datum", "gemeld_op"):
            v = it.get(veld)
            if isinstance(v, str):
                try:
                    if not DATUM_RE.match(v):
                        raise ValueError
                    datetime.strptime(v, "%Y-%m-%d")
                except ValueError:
                    fouten.append(f"{label}: '{veld}' is geen geldige yyyy-mm-dd ({v})")
        if isinstance(it.get("categorie"), str) and it["categorie"] not in CATEGORIEEN:
            fouten.append(f"{label}: ongeldige categorie '{it['categorie']}'")
        if isinstance(it.get("bron_type"), str) and it["bron_type"] not in BRON_TYPES:
            fouten.append(f"{label}: ongeldig bron_type '{it['bron_type']}'")
        for b in it.get("bronnen", []) if isinstance(it.get("bronnen"), list) else []:
            if not (isinstance(b, dict) and isinstance(b.get("titel"), str) and isinstance(b.get("url"), str)):
                fouten.append(f"{label}: bron moet {{titel, url}} (strings) zijn")
    return fouten


def rfc822(datum):
    d = datetime.strptime(datum, "%Y-%m-%d").replace(hour=8, minute=30, tzinfo=timezone.utc)
    return format_datetime(d)


def bouw_feed(items):
    items = sorted(items, key=lambda x: (x["datum"], x["gemeld_op"], x["id"]), reverse=True)
    laatste = max((x["gemeld_op"] for x in items), default="2026-01-01")
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0">',
           "<channel>",
           "<title>Markt-intelligentie 4PS &amp; Business Central</title>",
           f"<link>{REPO_URL}</link>",
           "<description>Dagelijkse markt- en AI-intelligentie rond 4PS Construct en Microsoft Dynamics 365 Business Central</description>",
           "<language>nl-nl</language>",
           f"<lastBuildDate>{rfc822(laatste)}</lastBuildDate>"]
    for it in items:
        link = it["bronnen"][0]["url"] if it["bronnen"] else f"{REPO_URL}/blob/main/data/updates.json"
        desc = f"{it['samenvatting']}\n\nRelevantie: {it['relevantie']}"
        out += ["<item>",
                f"<title>{escape(it['onderwerp'])}</title>",
                f"<link>{escape(link)}</link>",
                f"<description>{escape(desc)}</description>",
                f"<pubDate>{rfc822(it['datum'])}</pubDate>",
                f"<category>{escape(it['categorie'])}</category>",
                f'<guid isPermaLink="false">{escape(it["id"])}</guid>',
                "</item>"]
    out += ["</channel>", "</rss>", ""]
    return "\n".join(out)


def main():
    items = json.loads(DATA.read_text(encoding="utf-8"))
    fouten = valideer(items)
    if fouten:
        print("Validatie mislukt:", file=sys.stderr)
        for f in fouten:
            print(f"  - {f}", file=sys.stderr)
        sys.exit(1)
    FEED.write_text(bouw_feed(items), encoding="utf-8")
    print(f"OK: {len(items)} items gevalideerd, feed.xml geschreven")


if __name__ == "__main__":
    main()
