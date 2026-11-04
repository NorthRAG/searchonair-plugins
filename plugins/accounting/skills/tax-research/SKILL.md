---
name: tax-research
description: Use when the user asks about Turkish tax or accounting rules (Tax Procedure Law VUK, VAT/KDV, income and corporate tax, e-invoice/e-archive, Revenue Administration (GİB) communiqués, circulars and rulings, accounting standards). Finds, reads and cites the relevant legislation article by article with the Search on Air tools (search, get_document, ask).
---

# Turkish tax and accounting research (Search on Air)

This plugin connects to the Search on Air accounting and tax dataset: Turkish tax laws,
Revenue Administration (GİB) communiqués, circulars and rulings, and accounting standards.
The tools live on the `accounting` MCP server. The sources are in Turkish, so write search
queries in Turkish legislative language; answer in the user's language.

| tool | when | quota |
|---|---|---|
| `search` | First step of every research task. Call it several times with different terms. | search |
| `get_document` | Read the full article or communiqué. Use `offset` to continue long texts. | search |
| `ask` | The user wants a quick, ready-made answer with citations. | ask (lower) |
| `list_sources` | See what each source covers. | none |

## Workflow

1. **Frame the question:** which tax or law (VUK, KDVK, GVK, KVK...), which period? Does the
   taxpayer type matter (individual, company, simplified-method taxpayer)?
2. **Search** in legislative Turkish ("faturanın düzenlenme süresi", "indirim hakkının
   kullanılma zamanı"). Use `mode: "hybrid"` when a law or article number is involved. Find
   both the statute and the communiqué that explains how it is applied.
3. **Read** the articles that carry the answer with `get_document`; check exceptions and
   effective dates.
4. **Write:** short answer first, then the reasoning. Cite the document and article for every
   finding ("213 sayılı VUK md. 231/5"). **Amounts, rates and thresholds change every year:**
   state which dated text you relied on and that it should be checked for currency.
5. **Stay within the sources.** End by noting that this is general information, not
   professional advice, and that a certified accountant (mali müşavir) should be consulted for
   the specific case.

## Errors

- **Missing or invalid token:** get a token at https://searchonair.com/dashboard; enter it with
  `/plugin configure searchonair-accounting@searchonair` in Claude Code, or set
  `SEARCHONAIR_ACCOUNTING_TOKEN` for Codex.
- **Dataset not loaded yet:** the tool says so. Tell the user; never make up legislation.
- **Quota reached:** daily quotas reset at midnight (Istanbul time); if only the `ask` quota
  is used up, continue with `search` + `get_document`.
