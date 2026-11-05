"""Generate the marketplace and plugin manifests for SearchOnAir/plugins from one source.

Run after changing anything below, then bump VERSION: Claude Code only delivers an
update to installed plugins when the version in plugin.json changes.

    python3 scripts/generate.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://api.searchonair.com"
SITE = "https://searchonair.com"
REPO = "https://github.com/SearchOnAir/plugins"
VERSION = "1.0.3"
LICENSE = "Apache-2.0"
OWNER = {"name": "Search on Air", "url": SITE}

DOMAINS = {
    "lawyer": {
        "title": "Law", "display": "Search on Air: Turkish Law",
        "short": "Search Turkish court decisions and cite them precisely",
        "desc": ("Semantic and keyword search over 11M+ Turkish court decisions (Court of "
                 "Cassation, Council of State, regional and first-instance courts, Constitutional "
                 "Court), full-text reading and answers with exact case citations. Requires a "
                 "Search on Air token."),
        "keywords": ["law", "legal research", "case law", "turkey", "turkish", "court decisions",
                     "rag"],
        "prompts": ["Can an employee who resigns over unpaid wages claim severance pay?",
                    "Find Court of Cassation decisions on rent adjustment cases.",
                    "What has the Constitutional Court said about length of proceedings?"],
    },
    "accounting": {
        "title": "Accounting & Tax", "display": "Search on Air: Turkish Accounting & Tax",
        "short": "Sourced answers from Turkish tax law and Revenue Administration guidance",
        "desc": ("Search Turkish tax laws, Revenue Administration (GİB) communiqués, circulars "
                 "and rulings, and accounting standards; read full texts and get answers that "
                 "cite the exact article. Requires a Search on Air token."),
        "keywords": ["accounting", "tax", "vat", "e-invoice", "turkey", "turkish", "rag"],
        "prompts": ["Within how many days must an invoice be issued after delivery?",
                    "Can VAT on a late-arriving purchase invoice still be deducted?",
                    "Who must switch to e-Invoice in 2026?"],
    },
    "health": {
        "title": "Health", "display": "Search on Air: Turkish Health Regulations",
        "short": "Search Turkish health regulations, SGK coverage rules and patient rights",
        "desc": ("Search Turkish health legislation, the Social Security Institution's Health "
                 "Implementation Communiqué (SUT), patient-rights regulations and official public "
                 "health guidance, with answers that cite the exact article. Not medical advice. "
                 "Requires a Search on Air token."),
        "keywords": ["health", "healthcare regulation", "patient rights", "insurance", "turkey",
                     "turkish", "rag"],
        "prompts": ["Can a patient get a copy of their hospital medical records?",
                    "How often can I change my family physician?",
                    "What co-payment applies to prescription drugs for retirees?"],
    },
}


def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


claude_entries, codex_entries = [], []
for slug, d in DOMAINS.items():
    name = f"searchonair-{slug}"
    base = ROOT / "plugins" / slug
    mcp_url = f"{API}/{slug}/mcp"
    env = f"SEARCHONAIR_{slug.upper()}_TOKEN"
    # Claude Code asks for the token at install time (sensitive: stored in the OS secure
    # store) and sends it in the Authorization header of every MCP request.
    dump(base / ".claude-plugin" / "plugin.json", {
        "name": name, "version": VERSION, "description": d["desc"],
        "author": OWNER, "homepage": f"{SITE}/install/{slug}", "repository": REPO,
        "license": LICENSE, "keywords": d["keywords"],
        "userConfig": {"api_token": {
            "type": "string", "title": "Search on Air token",
            "description": (f"Your {d['title']} token (starts with soa_). Get one at "
                            f"{SITE}/dashboard"),
            "required": True, "sensitive": True}},
        "mcpServers": {slug: {"type": "http", "url": mcp_url,
                              "headers": {"Authorization": "Bearer ${user_config.api_token}"}}},
    })
    # Codex (compatibility format): Codex has no install-time prompt for secrets, so the
    # token is read from an environment variable and sent as a Bearer token.
    dump(base / ".codex-plugin" / "plugin.json", {
        "name": name, "version": VERSION, "description": d["desc"],
        "author": {"name": OWNER["name"], "url": SITE}, "homepage": f"{SITE}/install/{slug}",
        "repository": REPO, "license": LICENSE, "keywords": d["keywords"],
        "skills": "./skills/", "mcpServers": "./codex.mcp.json",
        "interface": {"displayName": d["display"], "shortDescription": d["short"],
                      "longDescription": d["desc"], "developerName": OWNER["name"],
                      "category": "Research", "websiteURL": SITE,
                      "defaultPrompt": d["prompts"]},
    })
    dump(base / "codex.mcp.json", {"mcpServers": {slug: {
        "type": "http", "url": mcp_url, "bearer_token_env_var": env}}})
    claude_entries.append({"name": name, "source": f"./plugins/{slug}", "description": d["desc"],
                           "category": "research", "keywords": d["keywords"],
                           "homepage": f"{SITE}/install/{slug}"})
    codex_entries.append({"name": name, "source": {"source": "local", "path": f"./plugins/{slug}"},
                          "policy": {"installation": "AVAILABLE"}, "category": "Research"})

dump(ROOT / ".claude-plugin" / "marketplace.json", {
    "name": "searchonair",
    "description": "Search on Air: research tools over Turkish legal, tax and health sources",
    "owner": OWNER, "plugins": claude_entries})
dump(ROOT / ".agents" / "plugins" / "marketplace.json", {
    "name": "searchonair", "interface": {"displayName": "Search on Air"}, "plugins": codex_entries})
print("ok")
