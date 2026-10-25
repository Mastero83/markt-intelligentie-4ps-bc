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

## Consumeren (publiek, geen token nodig)

De repo is publiek; apps lezen de bestanden direct via raw-URL's:

- JSON: https://raw.githubusercontent.com/Mastero83/markt-intelligentie-4ps-bc/main/data/updates.json
- RSS: https://raw.githubusercontent.com/Mastero83/markt-intelligentie-4ps-bc/main/feed.xml

```bash
curl -s https://raw.githubusercontent.com/Mastero83/markt-intelligentie-4ps-bc/main/data/updates.json
```

Raw-URL's worden door GitHub enkele minuten gecachet. Wil je weten of er iets nieuws is, vergelijk dan de laatste commit op `main` (`https://api.github.com/repos/Mastero83/markt-intelligentie-4ps-bc/commits/main`) of de `sha` uit `https://api.github.com/repos/Mastero83/markt-intelligentie-4ps-bc/contents/data/updates.json` (zonder token: 60 requests/uur per IP).

**Importregels**
- Sleutel = `id` (stabiel en uniek). Importeer als upsert op `id`; nieuwe `id`'s = nieuwe items.
- De bron is alleen-toevoegen: verwijder niets lokaal op basis van ontbrekende items.
- Use cases ter inspiratie voor klantgesprekken staan in hetzelfde bestand met `categorie: "use_case"`.
- Filter/sorteer op `datum` (nieuwsdatum), `gemeld_op` (registratiedatum), `categorie`, `tags`, `bron_type`.

## Aanbevolen architectuur

1. **DAS Klant Intelligentie-webapp**: een geplande job (bv. dagelijks ~09:00 Europe/Amsterdam, na de radar) haalt `data/updates.json` op en importeert op `id` in de eigen database. De webapp toont/filtert vanuit die database, niet live vanuit GitHub.
2. **Dassie (Foundry-agent)**: indexeer de items (vanuit de webapp-database of direct uit deze repo) in een zoekindex, bv. **Azure AI Search** (velden: `id` als key, `onderwerp`, `samenvatting`, `relevantie` als doorzoekbare tekst, `categorie`/`tags`/`datum` als filters, `bronnen` als metadata). Koppel de index als knowledge/tool aan Dassie, zodat antwoorden bronnen kunnen citeren.
3. **Andere apps**: gebruik de RSS-feed (`feed.xml`, bv. RSS-lezers, Teams/Power Automate) of de raw JSON-URL.

## Lokaal bijwerken

```bash
# item(s) toevoegen aan data/updates.json, dan:
scripts/publish.sh
```
