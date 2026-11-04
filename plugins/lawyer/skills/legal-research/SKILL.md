---
name: legal-research
description: Use when the user asks a question about Turkish law, a legal dispute, case law (içtihat) or a Turkish court decision. Finds, reads and cites decisions of the Court of Cassation (Yargıtay), Council of State (Danıştay), regional and first-instance courts (UYAP emsal) and the Constitutional Court (Anayasa Mahkemesi) with the Search on Air tools (search, get_document, ask).
---

# Turkish case-law research (Search on Air)

This plugin connects to the Search on Air law dataset: more than 11 million Turkish court
decisions. The tools live on the `lawyer` MCP server. The decisions are in Turkish, so write
search queries in Turkish legal language; answer in the user's language.

| tool | when | quota |
|---|---|---|
| `search` | First step of every research task. Call it several times with different terms. | search |
| `get_document` | Read the full text of a decision that looks important. Use `offset` to continue long texts. | search |
| `ask` | The user wants a quick, ready-made answer with citations. Runs an LLM on the server. | ask (lower) |
| `list_sources` | See what each source covers. | none |

Sources: `yargitay` (Court of Cassation: civil and criminal chambers), `danistay` (Council of
State: administrative and tax), `emsal` (UYAP: regional appeal and first-instance courts,
mostly commercial), `aym_bb` (Constitutional Court individual applications: fundamental
rights), `aym_norm` (Constitutional Court review of statutes).

## Workflow

1. **Frame the question.** Which branch of law? Private law (Yargıtay civil chambers + emsal),
   administrative or tax (Danıştay), a fundamental-rights violation (aym_bb) or the
   constitutionality of a statute (aym_norm)? Is there a date constraint?
2. **Search.** Phrase `search` queries with the Turkish legal terms a decision would use, e.g.
   "kıdem tazminatı haklı fesih ücretin ödenmemesi". For statute or article numbers and docket
   numbers (esas/karar no) use `mode: "hybrid"` or `"sparse"`. Only add source and year filters
   when the question calls for them. If the first results are weak, retry with synonyms or
   without filters.
3. **Read.** Open the 2-4 decisions that carry the answer with `get_document`. A search snippet
   may not show the outcome; confirm the holding and reasoning in the full text.
4. **Write.** Give the short answer first, then the reasoning. After every finding, cite the
   decision exactly as the tool labels it (e.g. "Yargıtay 9. Hukuk Dairesi, E. 2015/4260,
   K. 2015/11423, T. 12.03.2015"). If decisions conflict, show both with their dates; chamber
   names and their division of work changed over the years, so weigh older decisions accordingly.
5. **Stay within the sources.** Do not attribute to a decision anything it does not say; mark
   general legal knowledge as such. End by noting that this is not legal advice and that a
   lawyer should be consulted for the specific case.

## Errors

- **Missing or invalid token:** the tool explains what to do. Tell the user to get a token at
  https://searchonair.com/dashboard and enter it with `/plugin configure searchonair-lawyer@searchonair`
  in Claude Code (or the `SEARCHONAIR_LAWYER_TOKEN` environment variable in Codex).
- **Quota reached:** daily quotas reset at midnight (Istanbul time). Tell the user; if only the
  `ask` quota is used up, continue with `search` + `get_document`.
- **No results:** broaden the query, remove filters, try synonyms. If there is still nothing,
  say so plainly. Never invent decisions.
