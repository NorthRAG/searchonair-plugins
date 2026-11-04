---
name: health-regulation-research
description: Use when the user asks about the Turkish healthcare system, patient rights, Social Security Institution (SGK) health coverage (SUT, co-payments), family physicians or Turkish health legislation. Finds, reads and cites official sources article by article with the Search on Air tools (search, get_document, ask). Not for diagnosis or treatment advice.
---

# Turkish health regulation research (Search on Air)

This plugin connects to the Search on Air health dataset: Turkish health legislation, the
SGK Health Implementation Communiqué (SUT), patient-rights regulations and official public
health guidance. The tools live on the `health` MCP server. The sources are in Turkish, so
write search queries in Turkish regulatory language; answer in the user's language.

| tool | when | quota |
|---|---|---|
| `search` | First step of every research task. Call it several times with different terms. | search |
| `get_document` | Read the full regulation or communiqué article. | search |
| `ask` | The user wants a quick, ready-made answer with citations. | ask (lower) |
| `list_sources` | See what each source covers. | none |

## Workflow

1. **Classify the question:** patient right, SGK coverage or payment, or how a health
   institution operates? If the user asks for a diagnosis, treatment or drug dosage, say that
   this is outside the plugin's scope and refer them to a physician. **If the user describes an
   emergency, tell them to call 112.**
2. **Search** in regulatory Turkish ("tıbbi kayıtlara erişim hakkı", "aile hekimi
   değişikliği", "reçete katılım payı muafiyeti").
3. **Read** the articles that carry the answer with `get_document`; check exceptions and
   amendment dates.
4. **Write:** short answer first, then the reasoning; cite the document and article for every
   finding. Amounts and periods can change: state which dated text you relied on.
5. **Stay within the sources.** End by noting that this is general information, not medical or
   legal advice, and that a physician or the relevant health institution should be consulted
   for the specific case.

## Errors

- **Missing or invalid token:** get a token at https://searchonair.com/dashboard; enter it with
  `/plugin configure searchonair-health@searchonair` in Claude Code, or set
  `SEARCHONAIR_HEALTH_TOKEN` for Codex.
- **Dataset not loaded yet:** the tool says so. Tell the user; never make up information.
- **Quota reached:** daily quotas reset at midnight (Istanbul time).
