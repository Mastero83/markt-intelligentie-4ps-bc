# AI-agents in Microsoft Dynamics 365 Business Central en 4PS Construct: basisanalyse

*Peildatum: 19 oktober 2026. Opgesteld met openbare bronnen (Microsoft Learn, websites en LinkedIn van 4PS, partner- en concurrentiesites, EU). Bij elke feitelijke claim staat een bron-URL. Waar ik zelf iets afleid of inschat, staat **[Eigen inschatting]**. Prijzen staan in USD zoals Microsoft ze publiceert; de prijzen in EUR voor Nederland kunnen afwijken.*

---

## 0. Samenvatting

- **Microsoft:** BC heeft nu drie kant-en-klare agents. De **Sales Order Agent** en de **Payables Agent** zijn GA in alle BC-landen, dus ook in NL. De **Expense Agent** is nog *public preview*. Daarnaast is er **agent-ontwerp**: Agent Designer en de AL Agent SDK. Microsoft Learn noemt dit nog *preview*, met productie-inzet vanaf 28.1. Verder is er een **BC MCP-server**: GA, verplicht aan sinds 28.0, en vanaf 29.0 GA met data queries. Die kan samenwerken met Copilot Studio. Copilot-assistentie zit zonder meerkosten in de BC-licentie. Agents betaal je per gebruik in **Copilot Credits**.
- **4PS:** 4PS Construct heeft de Copilot-functies van Microsoft ("4PS Copilot"), zoals chat over ERP-data, nummerreeks-suggesties en teksten voor het afmelden van serviceorders. In openbare releasecommunicatie (2026-1, 2026-3) vond ik **geen eigen, gelanceerde 4PS-agent**. 4PS laat wel duidelijk zien dat het ermee bezig is: een 4PS-medewerker bouwde in een webinar live een eigen BC-agent, op de 4PS Customer Day (15-09-2026) werden AI-agents gedemonstreerd, en 4PS UK houdt webinars over "Copilot and AI Agents".
- **Markt:** BC-partners voor de installatiebranche, zoals Bluace, implementeren de standaardagents van Microsoft. ISV's zoals Yaveon bouwen eigen agents. Concurrent Exact heeft eigen agents (Purchase, Bank, Debtor, Support en Financial) en zegt dat AI-agents in alle edities van Exact voor Bouw zitten. Syntess zet in op BI/AI-rapportage met Bisharp. Agents bovenop Syntess of AFAS komen vooral van externe maatwerkbouwers.
- **Waarom het langer duurt:** de redenen zijn goed te onderbouwen. Veel onderdelen zijn nog preview of alleen gevalideerd voor Engels. Agents werken alleen in BC online, niet on-prem. Er zijn toestemmingen voor dataverplaatsing binnen de EU-datagrens nodig. De kosten hangen af van het gebruik. De kwaliteit van stamdata en tooltips bepaalt hoe goed agents werken. De standaardagents zijn generiek (e-mail, PDF-facturen, verkooporders) en niet bouwspecifiek. En 4PS zit vast aan de cyclus van Microsoft plus de eigen releasecyclus, met grote technische overgangen in 2026-3 en 2027-1.

---

## 1. Microsoft: Copilot en agents in Business Central

### 1.1 Uitgangspunten

- Copilot en agents zijn **alleen beschikbaar voor BC online**. Bron: https://learn.microsoft.com/en-us/dynamics365/release-plan/2026wave1/smb/dynamics365-business-central/copilot-agents. Microsoft is ook niet van plan Copilot on-prem te leveren. Bron: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/features-not-implemented-on-premises
- "With your Business Central license, everyone gets a copilot at no extra cost". De assistentiefuncties kosten dus niets extra. Bron: https://learn.microsoft.com/en-us/dynamics365/release-plan/2026wave1/smb/dynamics365-business-central/copilot-agents
- Agents kosten wel geld per gebruik. Betaald worden de Expense Agent (preview), de Payables Agent, de Sales Order Agent en "Designing and coding agents (preview)". Bron: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/administration/tenant-admin-center-manage-consumption-billing
- Releases: 2026 release wave 2 = **versie 29.0, oktober 2026**. Admins kunnen de update plannen tot februari 2027. Bron: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/whatsnew/whatsnew-update-29-0
- Sinds september 2026 publiceert Microsoft **geen release plans meer**. Nieuwe functies verschijnen op de "AI at Work roadmap". Bron: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/whatsnew/overview

### 1.2 Overzicht per agent of functie

| Agent / functie | Wat doet het | Status (okt 2026) | NL / Nederlands | Kosten |
|---|---|---|---|---|
| **Sales Order Agent** | Bewaakt een mailbox en leest klantverzoeken, ook PDF's en afbeeldingen. Zoekt de klant op via het e-mailadres, zoekt artikelen en controleert de voorraad (eventueel met capable-to-promise). Maakt eerst altijd een offerte en daarna een order. Mailt heen en weer met de klant. Een mens keurt alle uitgaande mails goed. | **GA** in alle BC-landen | Nederlands (nl-NL, nl-BE) wordt ondersteund | Per stap: e-mail analyseren 2 credits, bijlage met verkoopdata 5, beschikbaarheid 5, offerte/order 5, antwoordmail 2. Microsoft rekent met een typische aanvraag van ca. 14 credits. |
| **Payables Agent** | Bewaakt een mailbox voor inkoopfacturen (PDF). OCR via Azure Document Intelligence, herkent de leverancier (kan een nieuwe aanmaken, geblokkeerd), stelt regels voor op basis van factuurhistorie, en sinds 29.0 een betere match met inkooporders. Een mens controleert het concept. De agent boekt niet zelf. | **GA** in alle BC-landen. Verbeterde PO-matching GA in 29.0 | Nederlands staat in de taaltabel, maar de agentpagina zegt "validated and supported in English only" | 50 credits per factuur + 5 per factuurregel |
| **Expense Agent** | Bonnetjes via webapp, Outlook of e-mail → declaraties, inclusief dubbele bonnen en per diem. Uitbreidingen in 29.0 (btw, AI-goedkeuringen, meer landen en talen) zijn ook preview. | **Public preview** (sinds 8 mei 2026) | Nederlands staat in de taaltabel. De uitrol per land is beperkt (eerst VS, daarna o.a. AU/NZ/UK) | 50 credits per bonnetje |
| **Agent Designer / AI development toolkit** | Zelf agents ontwerpen in natuurlijke taal, met eigen rol, rechten en instructies | **Public preview**. De toolkit werkt alleen in sandboxes. Volgens 28.1 nu ook "on production environments". Ondersteunde taal: alleen Engels | Alleen Engels gevalideerd | Copilot Credits (preview) |
| **Agent SDK voor AL** | Agents in code (AL), bijv. voor ISV's / AppSource | **Preview**. Productie ondersteund vanaf 28.1 | n.v.t. | Copilot Credits |
| **BC MCP-server** | Externe AI-clients (Copilot Studio, VS Code, andere MCP-clients) lezen BC-API's en kunnen ze bij configuratie ook aanroepen. Standaard alleen-lezen | **GA** (28.0, verplicht aan). "Run data queries with MCP Server" GA in 29.0. Admin center via MCP: preview | n.v.t. | Via Copilot Studio of de client |
| **Copilot Studio-integratie** | Agents in Copilot Studio met BC als tool via de MCP-connector (omgeving, bedrijf, configuratie) | Beschikbaar (documentatie Learn) | n.v.t. | Copilot Studio-credits |
| **Microsoft Copilot chat in BC** | Nieuwe chat-ervaring in BC 29 | **Public preview** (29.0) | Volgt de talen van Microsoft Copilot | Valt onder Microsoft Copilot |
| **Assistentiefuncties** | O.a. chat, analysis assist, hulp bij bankafletteren, samenvatten, marketingteksten. Sommige (sales line suggestions, autofill, nummerreeksen) alleen in het Engels | GA | Veel functies ondersteunen Nederlands, enkele alleen Engels | Inbegrepen |

Bronnen bij de tabel:
- Sales Order Agent: https://learn.microsoft.com/en-us/dynamics365/business-central/sales-order-agent
- Payables Agent: https://learn.microsoft.com/en-us/dynamics365/business-central/payables-agent
- GA in alle landen (Microsoft BC LinkedIn, 27-04-2026): https://www.linkedin.com/posts/microsoft-dynamics-365-business-central_sales-order-agent-and-payables-agent-generally-activity-7454533099687665665-9kKz
- Talen en landen per functie: https://learn.microsoft.com/en-us/dynamics365/business-central/copilot-agents-region-language-availability
- Kosten per agent: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/administration/tenant-admin-center-manage-consumption-billing
- Expense Agent: https://learn.microsoft.com/en-us/dynamics365/release-plan/2026wave1/smb/dynamics365-business-central/manage-expenses-business-central-using-expense-agent en https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/whatsnew/whatsnew-update-28-1
- Agent Designer / toolkit: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/ai/ai-development-toolkit-overview en https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/whatsnew/whatsnew-update-28-1
- Agent SDK: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/ai/ai-agent-sdk-overview
- MCP-server: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/whatsnew/whatsnew-update-28-0, https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/ai/configure-mcp-server en https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/whatsnew/whatsnew-update-29-0
- Copilot Studio + MCP: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/ai/create-agent-in-copilot-studio

**Let op, bronnen spreken elkaar tegen:** partnerblog Tigunia noemt Agent Designer "generally available in May 2026" (https://tigunia.com/blog/complete-guide-to-business-central-ai-agents/). De officiële documentatie van Microsoft noemt het nog "public preview" en "prerelease documentation" (zie links hierboven). In dit rapport volg ik Microsoft.

### 1.3 Andere agentfuncties in 28.x/29.0 (GA)
- Een apart takenvenster voor alle agents, controle van door agents gemaakte inhoud direct op pagina's, alle taken van een agent in één keer stoppen, eenvoudiger beheer van agentrechten, meldingen voor agentacties in lijsten. Bronnen: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/whatsnew/whatsnew-update-28-0 en https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/whatsnew/whatsnew-update-29-0
- Voor ontwikkelaars (29.0): AL MCP-workspaces, agents die vrije object-ID's toewijzen, AI-agents die fouten debuggen en trage sessies profileren. Bron: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/whatsnew/whatsnew-update-29-0

### 1.4 Licentie en kosten (Copilot Credits)
- Pay-as-you-go: **$0,01 per Copilot Credit**, achteraf per maand gefactureerd. Daarnaast bestaat een Pre-Purchase Plan. Credits worden gedeeld op tenantniveau. Bron: https://www.microsoft.com/licensing/guidance/Copilot-Credits
- Capaciteitspakketten: **$200 per 25.000 credits per maand**. Bron: https://www.microsoft.com/en-us/copilot/pricing/copilot-studio
- Pay-as-you-go vereist een gekoppeld Azure-abonnement. Bron: https://www.microsoft.com/en/dynamics-365/products/business-central/pricing
- Rekenvoorbeeld van Microsoft: 100 facturen met elk 3 regels = 6.500 credits per maand (≈ $65). Bron: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/administration/tenant-admin-center-manage-consumption-billing
- Als de credits op zijn, stopt de Sales Order Agent met verwerken. Als er weer credits zijn, verwerkt hij alles wat is blijven liggen. Bron: https://learn.microsoft.com/en-us/dynamics365/business-central/sales-order-agent

### 1.5 Hoe Microsoft de lagen inricht
Microsoft scheidt de lagen bewust:
- agents *in* BC (eigen rechtenmodel, audit), voor processen binnen BC;
- de MCP-server als koppellaag;
- Copilot Studio voor agents die over meerdere systemen heen werken.

Bron: Tigunia, met citaat uit de Agent Designer-documentatie: https://tigunia.com/blog/complete-guide-to-business-central-ai-agents/. Op Directions NA 2026 riep Microsoft ISV's op om "productized agents" te bouwen, met voorbeelden als tijdregistratie, retouren en de intake van onderhoudsmeldingen. Bron: https://msdynamicsworld.com/story/directions-north-america-2026-ai-driven-devops-business-central-breeds-new-opportunities

---

## 2. 4PS (4PS Construct)

**Context.** Hilti heeft de overname van 4PS op 5 oktober 2023 afgerond. 4PS had toen meer dan 70.000 dagelijkse gebruikers en ongeveer 350 medewerkers. Bron: https://www.hilti.group/content/hilti/CP/XX/en/company/media-relations/media-releases/4ps_group_acquisition_erp_software_solutions_conclusion.html. 4PS is opnieuw lid van de Microsoft AI Business Applications Inner Circle 2025/2026 en heeft daardoor "vroegtijdig inzicht in de productroadmap … waaronder toepassingen van kunstmatige intelligentie". Bron: https://www.4ps.nl/actueel/4ps-opnieuw-microsoft-inner-circle-2025-2026/

**Wat 4PS openbaar heeft uitgebracht of aangekondigd:**
1. **Copilot in 4PS Construct ("4PS Copilot"), gebaseerd op Microsoft Copilot.** Een chatvenster om vragen te stellen over ERP-data, zoals lopende projecten en openstaande offertes. Bronnen: https://www.4ps.nl/actueel/ai-in-de-bouw-dichterbij-dan-je-denkt/ en https://www.4ps.co.uk/insights/construction-worker-shortages-four-digital-anchors/
2. **Release UK 2025-1:** "Microsoft and 4PS Copilot AI feature additions", bijvoorbeeld nummerreeks-suggesties en teksten voor het afmelden van serviceorders. Bron: https://www.4ps.co.uk/insights/4ps-construct-uk-2025-1-release-now-available/
3. **4PS UK (juli 2025):** Copilot is "now integrated into 4PS Construct", zonder "separate licensing". Bron: https://www.4ps.co.uk/insights/how-will-ai-transform-the-construction-industry/
4. **Webinars 4PS UK:** "AI in Action", met onder meer "Integrate Microsoft AI tools like Copilot and AI Agents". Bronnen: https://www.4ps.co.uk/ai-transformation-for-construction/ en https://www.linkedin.com/posts/4ps-uk_webinar-constructiontechnology-copilot-activity-7407796963355705344-5uaV
5. **Community (juli 2026):** Bert Verbeek (4PS) bouwt in een Areopa-webinar live een BC-agent: een e-mail over voorraad leidt tot een voorraadcheck, een inkooporder en een conceptantwoord. Daarbij: "Sandbox and preview only for now". Dit is een **generieke BC-demo**, geen 4PS-product. Bronnen: https://www.linkedin.com/posts/areopawebinars_new-webinar-recording-from-zero-to-agent-activity-7490370586574082048-QGPn en https://www.youtube.com/watch?v=nbGw2g3KMXI
6. **4PS Customer Day, 15-09-2026 (Den Haag):** een bezoeker schrijft over een "praxisnahe Demonstration verschiedener KI-Agenten" en "Agentic ERP wird Realität". Een Hilti-manager noemt "AI-toepassingen" voor ca. 400 bestuurders. Dit zijn **persoonlijke LinkedIn-posts**. Welke agents het waren, staat er niet bij. Bronnen: https://de.linkedin.com/posts/marc-oliver-bader-807142231_aftermovie-4ps-customer-day-2026-activity-7506700191538831361-y4kl en https://nl.linkedin.com/posts/bastian-danzebrink-a6204114a_hilti-hiltinederland-4ps-activity-7505913223045373952-0xM3
7. **Releases 2026:** de openbare samenvatting van 2026-1 (SE) noemt prijsstelling, workflow voor goedkeuring van inkoopontvangsten, Field Service App en live datasync via de BC API. AI wordt niet genoemd. Bron: https://www.4ps.se/aktuellt/release-ny-version-av-4ps-construct-2026-01/. Release **2026-3** (NL, september 2026) bevat o.a. een Mollie Payments-extensie en de overgang naar Microsoft External File Storage. Voor **2027-1** staan aangekondigd: overgang naar Microsoft MDM, andere veldlengtes en het uitfaseren van SOAP-webservices. AI-agents worden niet genoemd. De volledige release notes staan alleen op het (afgeschermde) Customer Portal. Bronnen: https://nl.linkedin.com/posts/marjoleindommers_4ps-businesscentral-erp-activity-7503478617637601281-cLUQ en https://nl.linkedin.com/posts/marjoleindommers_4ps-erp-businesscentral-activity-7511385647874678785-aQQU

**Eerlijke conclusie.** Openbaar is er bij 4PS weinig te vinden over een **eigen, bouwspecifieke agent die in productie draait**. Wat wel vaststaat: Copilot-functies van Microsoft en 4PS, demo's en webinars, en kennisopbouw via Inner Circle en de community. **[Eigen inschatting]** De release notes zijn afgeschermd. Er kan daarom meer zijn dan openbaar zichtbaar is. Dit is te controleren via het Customer Portal of de accountmanager.

**Cloud.** 4PS richt zich "volledig op cloudsoftware". In 2023 migreerden 68 klanten. Het doel voor 2024 was 90 migraties. Bron: https://www.4ps.nl/actueel/in-2023-migreerden-68-klanten-naar-de-cloud/

---

## 3. Partners, ISV's en concurrenten

**Op of rond BC:**
- **Bluace** (BC-partner voor de installatiebranche, NL) implementeert de Sales Order, Payables en Expense Agent en Agent Designer "for installation, service, and technical companies". Bron: https://bluace.nl/en/dynamics-software-apps/business-central/
- **Yaveon** (Duitse BC-ISV, procesindustrie) heeft een "Supply Chain Agent" in Copilot Studio en een **native BC-agent** die incidenten aanmaakt uit inkomende e-mails. Klanten kunnen koppelen via MCP, API's of het interne agentmodel van BC. Bron (15-10-2026): https://msdynamicsworld.com/story/building-ai-agents-erp-process-optimization-one-isvs-experiences-addressing-new-supply-chain
- **Microsoft** noemde op Directions NA 2026 "over a dozen" ISV-agents. Bron: https://msdynamicsworld.com/story/directions-north-america-2026-ai-driven-devops-business-central-breeds-new-opportunities
- Ik heb **geen bouwspecifieke BC-agent op AppSource of Marketplace** gevonden die openbaar en GA is. **[Eigen inschatting:** dit betekent niet dat er geen zijn. Mijn zoektocht was beperkt.**]**

**Andere bouw- en installatie-ERP in NL:**
- **Exact (Exact Online Bouw, voorheen Bouw7):** AI-agents zitten volgens de prijspagina in alle edities (Purchase Agent, Bank Agent, Debtor Agent, Support Agent). Bron: https://www.exact.com/nl/producten/bouw/features-en-prijzen. Op 3 september 2026 lanceerde Exact de **Financial Agent**. Bron: https://www.exact.com/nl/nieuws/nieuwe-ai-agent-brengt-financieel-professionals-sneller-van-cijfers-naar-beslissingen
- **Syntess (Atrium):** exclusief partnership met Bisharp voor een standaard "BI & AI-rapportageproduct" (19-03-2026). Bron: https://www.syntess.nl/nieuws/syntess-en-bisharp-sluiten-exclusief-partnership-voor-bi-en-ai-rapportage/
- **Externe maatwerkbouwers** maken agents bovenop Syntess, AFAS en Admicom, bijvoorbeeld **Retrii**: intake van storingen en werkbonnen, vanaf €5.000, "mens als laatste controle". Bron: https://retrii.com/ai-voor-installatiebedrijven/. Er bestaan ook MCP-koppelingen voor Exact Online Bouw, zoals Bouw Botje: https://bouwbotje.nl/ (niet verder gecontroleerd).

**[Eigen inschatting]** Exact zet zijn agents duidelijk als onderdeel van het pakket in de markt. Bij BC/4PS zijn de agents op dit moment **generieke Microsoft-agents met betaling per gebruik**, en bouwspecifieke varianten moeten nog komen.

---

## 4. Waarom gaat het langer duren?

### 4.1 Preview-status en gevalideerde talen *(onderbouwd)*
- De Expense Agent, Agent Designer/toolkit, de AL Agent SDK en de Copilot chat in 29.0 zijn **preview**. Bronnen: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/whatsnew/whatsnew-update-29-0 en https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/ai/ai-development-toolkit-overview
- De Payables Agent is "validated and supported in English only". Het ontwerpen van agents ondersteunt alleen Engels. Bronnen: https://learn.microsoft.com/en-us/dynamics365/business-central/payables-agent en de toolkit-pagina hierboven.
- Microsoft legt zelf uit waarom niet alles tegelijk overal verschijnt: regelgeving (o.a. AVG), Azure-infrastructuur, kwaliteitsvalidatie en taalmodellen per taal. Het advies is: "Use Copilot features only in officially supported languages for business-critical processes". Bron: https://learn.microsoft.com/en-us/dynamics365/business-central/copilot-agents-region-language-availability
- De beperkingen van de Payables Agent: geen goedkeuringsflows en geen detectie van afwijkingen. Alleen PDF, maximaal 10 pagina's of 5 MB, maximaal 100 e-mails en 500 facturen per dag. Bron: https://learn.microsoft.com/en-us/dynamics365/business-central/payables-agent

### 4.2 EU-datagrens en AVG *(onderbouwd)*
- Voor BC-omgevingen in de EU gebruikt Microsoft een Azure OpenAI-endpoint binnen de EU-datagrens. De verwerking kan wel tussen EU-geografieën plaatsvinden. Daarvoor is **toestemming** nodig via de schakelaar "Allow data movement". Zet je die uit, dan werken de Copilot-functies niet. Prompts en output kunnen tot 24 uur worden bewaard voor misbruikmonitoring. Bron: https://learn.microsoft.com/en-us/dynamics365/business-central/ai-copilot-data-movement
- **[Eigen inschatting]** Bij bouw- en installatiebedrijven moeten de functionaris gegevensbescherming of IT dit expliciet beoordelen, bijvoorbeeld in een DPIA. Dat kost doorlooptijd.

### 4.3 EU AI Act *(onderbouwd voor de tijdlijn, eigen inschatting voor de impact)*
- De AI Omnibus is op 27-07-2026 in werking getreden. Regels voor hoog-risico-AI (Annex III) gelden vanaf 2 december 2027, voor Annex I vanaf 2 augustus 2028. Bron: https://digital-strategy.ec.europa.eu/en/news/ai-omnibus-enters-force. Een overzicht van de tijdlijn: https://ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act
- **[Eigen inschatting]** ERP-agents voor orders en facturen vallen waarschijnlijk niet onder hoog-risico. De AI Act is daarom vooral een bron van onzekerheid en extra governance, geen harde blokkade. Bij HR- of personeelsplanning ligt dat anders.

### 4.4 Licentie- en kostenmodel *(onderbouwd)*
- Er is een apart model met betaling per gebruik (Copilot Credits) en een gekoppeld Azure-abonnement voor pay-as-you-go. Hoeveel het kost, hangt af van het volume. Bronnen: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/administration/tenant-admin-center-manage-consumption-billing en https://www.microsoft.com/en/dynamics-365/products/business-central/pricing
- **[Eigen inschatting]** De bedragen per factuur zijn klein (≈ $0,65 per factuur met 3 regels). Toch maakt het variabele model budgettering en inkoop lastiger, zeker als een concurrent (Exact) agents bij de edities inbegrepen noemt.

### 4.5 Datakwaliteit en procesinrichting *(onderbouwd)*
- De Sales Order Agent herkent klanten **alleen via het e-mailveld op contactkaarten**. "The quality of product information … affects its effectiveness". Bron: https://learn.microsoft.com/en-us/dynamics365/business-central/sales-order-agent
- Agents navigeren via UI-metadata (captions, tooltips) en lossen fouten op aan de hand van foutmeldingen. Daardoor tellen maatwerk en tooltips van ISV's mee. Bronnen: https://learn.microsoft.com/en-us/dynamics365/business-central/payables-agent en de 4PS-demo "Why your tooltips and error messages suddenly matter a lot more": https://www.linkedin.com/posts/areopawebinars_new-webinar-recording-from-zero-to-agent-activity-7490370586574082048-QGPn
- Microsoft raadt een aparte, interne mailbox aan voor de Payables Agent, met volledige eigenaarschap door de agent. Bron: https://learn.microsoft.com/en-us/dynamics365/business-central/payables-agent
- Voor de bouw specifiek: Fieldwire (Hilti) noemt "gefragmenteerde en inconsistente data" de belangrijkste beperking voor AI in de bouw. Bron: https://www.fieldwire.com/nl/blog/toekomst-ai-bouw-verbonden-data/. Volgens de CBS AI Monitor 2024 loopt de bouw achter (9% van de bedrijven gebruikt AI). Bron: https://www.aannemervak.nl/bouwpraktijk/bouwtrends/datagedreven-bouwen/cbs-ai-monitor-2024-bouw-loopt-achter-in-ai-implementatie/

### 4.6 4PS als ISV is afhankelijk van Microsoft *(deels onderbouwd)*
- Productie-agents in AL kunnen pas vanaf 28.1, en de SDK is nog preview. Bron: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/ai/ai-agent-sdk-overview. Zolang de API's preview zijn, "might change without notice". Bron: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/ai/ai-development-toolkit-overview
- 4PS heeft een eigen releasecyclus en grote technische overgangen in 2026-3 en 2027-1 (External File Storage, MDM, veldlengtes, SOAP). Veel klanten waren in september 2026 nog bezig met 2026-2. Bron: https://nl.linkedin.com/posts/marjoleindommers_4ps-businesscentral-erp-activity-7503478617637601281-cLUQ
- Microsoft stopt met release plans en gaat over op een doorlopende roadmap. Bron: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/whatsnew/overview
- **[Eigen inschatting]** Een ISV ontwikkelt meestal pas een product op een functie als die GA en stabiel is. Daarna volgt de eigen release, en dan de update en adoptie bij klanten. Dat kost per stap gauw een half jaar of meer.

### 4.7 Bouwspecifieke processen *(eigen inschatting, deels onderbouwd)*
- De standaardagents dekken generieke processen: e-mail → offerte/order, PDF → inkoopfactuur, bonnetjes → declaratie. Bronnen: zie §1.2.
- **[Eigen inschatting]** De kernprocessen in de bouw zijn complexer en hangen veel meer van de context af: calculatie, meer- en minderwerk, termijnen, onderaanneming, G-rekening/WKA, projectbewaking en materieel. De standaard-Payables Agent heeft bijvoorbeeld geen goedkeuringsflows (bron: §4.1). Bouwbedrijven hebben die juist veel, bijvoorbeeld voor projectfiattering. Daarvoor zijn verticale agents van 4PS of partners nodig.

### 4.8 Vertrouwen en menselijke controle *(onderbouwd)*
- Microsoft ontwerpt de agents met de mens erbij: de Sales Order Agent laat "always" alle uitgaande berichten controleren. De Payables Agent boekt niet zelf, en een nieuwe leverancier blijft geblokkeerd tot een mens hem vrijgeeft. Bronnen: https://learn.microsoft.com/en-us/dynamics365/business-central/sales-order-agent en https://learn.microsoft.com/en-us/dynamics365/business-central/payables-agent
- **[Eigen inschatting]** Dat is verstandig, maar het beperkt de tijdwinst in het begin. Organisaties moeten nieuwe rollen inrichten, zoals agent supervisor.

### 4.9 Migratie van on-prem naar SaaS *(onderbouwd)*
- Copilot en agents werken alleen in BC online. Bronnen: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/features-not-implemented-on-premises en https://learn.microsoft.com/en-us/dynamics365/release-plan/2026wave1/smb/dynamics365-business-central/copilot-agents
- 4PS migreert klanten in tientallen per jaar: 68 in 2023, doel 90 in 2024. Bron: https://www.4ps.nl/actueel/in-2023-migreerden-68-klanten-naar-de-cloud/
- **[Eigen inschatting]** Klanten die nog on-prem of op NAV draaien, kunnen pas met agents werken na hun cloudmigratie.

---

## 5. Conclusie en vervolgstappen *(eigen inschatting)*
1. **Nu al te gebruiken in 4PS/BC online:** de Payables Agent (vooral Engelstalige facturen, of met extra controle) en de Sales Order Agent (Nederlands ondersteund). Het meest geschikt voor installatie, service en groothandelsachtige stromen.
2. **Pilot 2026/27:** eigen agents met Agent Designer (preview) of via Copilot Studio + MCP, bijvoorbeeld voor de intake van storingen en werkbonnen. Begin met een sandbox, minimale rechten en een aparte mailbox.
3. **Voorbereiden:** stamdata op orde brengen (e-mail op contactkaarten, artikelomschrijvingen en -attributen), toestemming voor dataverplaatsing en een DPIA regelen, een budget voor Copilot Credits vastleggen, en de cloudmigratie afronden.
4. **4PS volgen:** de release notes op het Customer Portal en de vervolgstappen na de demo's op de Customer Day. Vraag 4PS concreet naar de roadmap voor bouwspecifieke agents.

## 6. Kanttekeningen bij dit onderzoek
- Bronnen achter een login (4PS Customer Portal, het volledige MSDynamicsWorld-artikel, Microsoft Viva Engage) heb ik niet kunnen lezen.
- LinkedIn-posts zijn persoonlijke uitspraken, geen officiële productaankondigingen.
- De Exact-pagina over de Innovation Day/MCP-server (https://lb.exact.com/nl/innovation-day/ecosystem) gaf een time-out. Claims daarover heb ik daarom weggelaten.
