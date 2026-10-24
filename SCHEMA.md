# Schema: data/updates.json (markt-intelligentie 4PS & Business Central)

`data/updates.json` is een UTF-8 JSON-array en de bron van waarheid van deze repo. `feed.xml` (RSS 2.0) wordt hieruit gegenereerd met `scripts/build_feed.py`. Elk element is één marktbevinding over 4PS / Microsoft Dynamics 365 Business Central.

| Veld | Type | Beschrijving |
|---|---|---|
| `id` | string | Stabiele slug, uniek. Prefix `radar-` = dagelijkse radar, `ba-` = basisanalyse. Wijzigt niet bij updates. |
| `datum` | string (yyyy-mm-dd) | Datum van het nieuws/de bron. Als die onbekend is: de meldingsdatum (`gemeld_op`). Bij basisanalyse-items zonder specifieke brondatum: peildatum 2026-10-19. |
| `gemeld_op` | string (yyyy-mm-dd) | Datum waarop het item gemeld/vastgelegd is (radar-meldingsdatum of rapportdatum). |
| `onderwerp` | string | Korte titel. |
| `samenvatting` | string | 1-3 zinnen in het Nederlands, alleen feiten uit de bronbestanden. |
| `relevantie` | string | 1 zin NL: waarom relevant voor BC/4PS. |
| `categorie` | enum | Precies één van: `product_release`, `concurrentie`, `partners`, `prijzen_licenties`, `ai_features`, `markt`, `regelgeving`, `events`. |
| `tags` | string[] | Vrije trefwoorden, lowercase, met koppeltekens. |
| `bronnen` | object[] | Lijst van `{ "titel": string, "url": string }`. Kan leeg zijn als de bevinding een constatering zonder bron-URL is. |
| `bron_type` | enum | `dagelijkse_radar` (uit het AI-radar-log) of `basisanalyse` (uit het rapport van 19-10-2026). |

## Voorbeeld
```json
{
  "id": "radar-bc-mirroring-fabric-rm574126",
  "datum": "2026-10-20",
  "gemeld_op": "2026-10-21",
  "onderwerp": "BC data mirroring naar Microsoft Fabric (preview nov 2026)",
  "samenvatting": "...",
  "relevantie": "...",
  "categorie": "product_release",
  "tags": ["microsoft", "fabric"],
  "bronnen": [{"titel": "...", "url": "https://mc.merill.net/message/RM574126"}],
  "bron_type": "dagelijkse_radar"
}
```

## Bronnen
- Basisanalyse: `rapporten/2026-10-19-ai-agents-bc-4ps-analyse.md`
- Dagelijkse radar: log `ai-radar-gemeld.md` (meldingen 20 en 21 okt 2026)

## Paden
| Pad | Inhoud |
|---|---|
| `data/updates.json` | Bron van waarheid (dit schema) |
| `feed.xml` | Gegenereerde RSS 2.0-feed, nieuwste eerst (niet handmatig bewerken) |
| `rapporten/` | Achtergrondrapporten (markdown) |
| `scripts/build_feed.py` | Validatie + feed-generatie |
| `scripts/publish.sh` | Build + commit + push naar `main` |

## RSS-mapping (feed.xml)
`title` = `onderwerp`, `description` = `samenvatting` + "Relevantie: " + `relevantie`, `link` = eerste `bronnen[].url` (anders link naar deze repo), `pubDate` = `datum`, `category` = `categorie`, `guid` = `id`.

## Aanvullen
Voeg nieuwe items toe aan de array met een nieuwe unieke `id`. Bestaande `id`'s blijven ongewijzigd (alleen-toevoegen). Draai daarna `scripts/publish.sh`; die valideert (unieke `id`, verplichte velden, toegestane `categorie`/`bron_type`, datumformaat) en breekt af bij fouten.
