# Markt-intelligentie 4PS & Business Central

Dagelijkse markt- en AI-intelligentie rond **4PS Construct** en **Microsoft Dynamics 365 Business Central** (BC), als herbruikbare databron voor andere apps, zoals de **DAS Klant Intelligentie-webapp** en de Foundry-agent **Dassie**.

## Structuur

```
data/updates.json        Bron van waarheid: JSON-array met marktbevindingen (zie SCHEMA.md)
feed.xml                 RSS 2.0-feed, gegenereerd uit data/updates.json (nieuwste eerst)
SCHEMA.md                Veldbeschrijving, categorieën, RSS-mapping
rapporten/               Achtergrondrapporten (o.a. basisanalyse 2026-10-19)
scripts/build_feed.py    Valideert de JSON en bouwt feed.xml
scripts/publish.sh       Build + commit ("Radar-update <datum>") + push naar main, alleen bij wijzigingen
```

## Updates

De dagelijkse AI-radar voegt **elke werkdag rond 08:30 (Europe/Amsterdam)** nieuwe items toe aan `data/updates.json` en publiceert via `scripts/publish.sh`. Items worden alleen toegevoegd; een bestaande `id` wijzigt niet.

## Consumeren (privé repo: token nodig)

De repo is privé, dus elke app heeft een GitHub-token met leesrechten op deze repo nodig (bij voorkeur een fine-grained PAT of GitHub App met alleen `Contents: Read-only` op deze repo).

Met `gh`:

```bash
gh api repos/Mastero83/markt-intelligentie-4ps-bc/contents/data/updates.json \
  -H "Accept: application/vnd.github.raw" > updates.json
```

Met HTTP (bv. vanuit de webapp of een Azure Function):

```bash
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github.raw" \
     https://api.github.com/repos/Mastero83/markt-intelligentie-4ps-bc/contents/data/updates.json
```

Hetzelfde werkt voor `feed.xml`. Om onnodige downloads te voorkomen: vergelijk eerst de `sha` van het bestand (`GET .../contents/data/updates.json` zonder raw-header) of de laatste commit op `main`.

**Importregels**
- Sleutel = `id` (stabiel en uniek). Importeer als upsert op `id`; nieuwe `id`'s = nieuwe items.
- De bron is alleen-toevoegen: verwijder niets lokaal op basis van ontbrekende items.
- Filter/sorteer op `datum` (nieuwsdatum), `gemeld_op` (registratiedatum), `categorie`, `tags`, `bron_type`.

## Aanbevolen architectuur

1. **DAS Klant Intelligentie-webapp**: een geplande job (bv. dagelijks ~09:00 Europe/Amsterdam, na de radar) haalt `data/updates.json` op en importeert op `id` in de eigen database. De webapp toont/filtert vanuit die database, niet live vanuit GitHub.
2. **Dassie (Foundry-agent)**: indexeer de items (vanuit de webapp-database of direct uit deze repo) in een zoekindex, bv. **Azure AI Search** (velden: `id` als key, `onderwerp`, `samenvatting`, `relevantie` als doorzoekbare tekst, `categorie`/`tags`/`datum` als filters, `bronnen` als metadata). Koppel de index als knowledge/tool aan Dassie, zodat antwoorden bronnen kunnen citeren.
3. **Andere apps**: gebruik `feed.xml` (RSS-lezers, Teams/Power Automate) of de GitHub Contents API voor JSON.

## Lokaal bijwerken

```bash
# item(s) toevoegen aan data/updates.json, dan:
scripts/publish.sh
```
