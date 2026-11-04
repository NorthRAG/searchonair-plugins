# Search on Air plugins

Claude Code and Codex plugins for [Search on Air](https://searchonair.com): retrieval tools
over Turkish legal, tax and health sources. Each plugin connects to one dataset and brings
its MCP tools (`search`, `get_document`, `ask`, `list_sources`) plus a research skill that
tells the model how to use them and how to cite.

| plugin | dataset | MCP endpoint |
|---|---|---|
| `searchonair-lawyer` | Turkish court decisions: Court of Cassation, Council of State, regional and first-instance courts, Constitutional Court (11M+) | `https://api.searchonair.com/lawyer/mcp` |
| `searchonair-accounting` | Turkish tax laws, Revenue Administration (GİB) communiqués, circulars and rulings, accounting standards | `https://api.searchonair.com/accounting/mcp` |
| `searchonair-health` | Turkish health legislation, SGK Health Implementation Communiqué (SUT), patient rights | `https://api.searchonair.com/health/mcp` |

You need a **Search on Air token**. Sign up at https://searchonair.com: a free token for the
dataset you pick is created on sign-up (5 questions and 50 searches per day). Tokens are bound
to one dataset, so each plugin needs the token for its own dataset.

## Claude Code

```
/plugin marketplace add SearchOnAir/plugins
/plugin install searchonair-lawyer@searchonair
```

Claude Code asks for the token during installation and keeps it in the operating system's
secure credential store. One-step alternative:
`/plugin install searchonair-lawyer --marketplace SearchOnAir/plugins`.

To change the token (for example after rotating it):
`/plugin configure searchonair-lawyer@searchonair`, then restart Claude Code.

The skills can also be invoked directly: `/searchonair-lawyer:legal-research`,
`/searchonair-accounting:tax-research`, `/searchonair-health:health-regulation-research`.
Claude also uses them on its own for relevant questions.

## Codex

Codex does not prompt for secrets at install time; the token is read from an environment
variable:

```bash
# ~/.zshrc or ~/.bashrc
export SEARCHONAIR_LAWYER_TOKEN=soa_...
```

```bash
codex plugin marketplace add SearchOnAir/plugins
codex plugin add searchonair-lawyer@searchonair
```

Variables: `SEARCHONAIR_LAWYER_TOKEN`, `SEARCHONAIR_ACCOUNTING_TOKEN`,
`SEARCHONAIR_HEALTH_TOKEN`. Restart Codex in a new terminal for changes to take effect.

## Quotas

| plan | price | questions (`ask`) / day | searches + document reads / day |
|---|---:|---:|---:|
| Free | $0 | 5 | 50 |
| Basic | $10/month | 50 | 500 |
| Pro | $40/month | 250 | 2,500 |
| Enterprise | $100/month | 2,000 | 20,000 |

`search` and `get_document` count against the search quota; `ask` (a cited answer generated
on the server) counts against the question quota. Quotas reset every day at midnight
(Istanbul time). Every tool result ends with that day's usage.

## Languages

The sources are Turkish, so the models search them in Turkish and quote citations in the
original Turkish. You can ask in any language; answers follow your language.

## Privacy

Queries and questions sent through the tools go to the Search on Air API and are logged to
measure service quality. Do not put personal data, patient information or privileged client
information into queries.

## Development

The manifests are generated from a single source. Do not edit the JSON files by hand; change
`scripts/generate.py`, bump `VERSION` (Claude Code only delivers updates when the version
changes) and regenerate:

```bash
python3 scripts/generate.py
claude plugin validate .
for p in plugins/*; do claude plugin validate "$p"; done
```
