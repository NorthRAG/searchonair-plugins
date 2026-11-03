"""searchonair-plugins: marketplace + plugin manifestlerini tek kaynaktan uretir."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://api.searchonair.com"
SITE = "https://searchonair.com"
REPO = "https://github.com/NorthRAG/searchonair-plugins"
VERSION = "1.0.0"
OWNER = {"name": "NorthRAG", "url": SITE}

DOMAINS = {
    "lawyer": {
        "title": "Hukuk", "display": "Search on Air: Hukuk",
        "short": "Türk mahkeme kararlarında arama ve künyeli atıf",
        "desc": ("Yargıtay, Danıştay, UYAP emsal ve Anayasa Mahkemesi kararlarında (11M+) anlamsal "
                 "ve lafzi arama, tam metin okuma ve künyeli atıflı cevaplar. Search on Air token'ı gerekir."),
        "keywords": ["hukuk", "içtihat", "yargıtay", "danıştay", "anayasa mahkemesi", "türkçe", "rag"],
        "skill": "legal-research",
    },
    "accounting": {
        "title": "Muhasebe ve vergi", "display": "Search on Air: Muhasebe ve vergi",
        "short": "Türk vergi mevzuatı ve GİB kaynaklarında kaynaklı cevaplar",
        "desc": ("Vergi kanunları, GİB tebliğ/sirküler/özelgeleri ve muhasebe standartlarında arama, "
                 "tam metin okuma ve maddeli atıflı cevaplar. Search on Air token'ı gerekir."),
        "keywords": ["muhasebe", "vergi", "gib", "vuk", "kdv", "mali müşavir", "türkçe", "rag"],
        "skill": "tax-research",
    },
    "health": {
        "title": "Sağlık", "display": "Search on Air: Sağlık",
        "short": "Sağlık mevzuatı, SUT ve hasta hakları kaynaklarında arama",
        "desc": ("Sağlık mevzuatı, SGK Sağlık Uygulama Tebliği, hasta hakları ve resmî sağlık "
                 "bilgilendirmelerinde arama ve kaynaklı cevaplar. Search on Air token'ı gerekir."),
        "keywords": ["sağlık", "sut", "sgk", "hasta hakları", "mevzuat", "türkçe", "rag"],
        "skill": "health-regulation-research",
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
    # Claude Code: token kurulumda sorulur (sensitive -> isletim sisteminin guvenli deposu),
    # MCP isteginin Authorization basligina konur.
    dump(base / ".claude-plugin" / "plugin.json", {
        "name": name, "version": VERSION, "description": d["desc"],
        "author": OWNER, "homepage": f"{SITE}/install/{slug}", "repository": REPO,
        "keywords": d["keywords"],
        "userConfig": {"api_token": {
            "type": "string", "title": "Search on Air token",
            "description": (f"{SITE}/dashboard adresinden aldığınız, soa_ ile başlayan "
                            f"{d['title']} token'ı."),
            "required": True, "sensitive": True}},
        "mcpServers": {slug: {"type": "http", "url": mcp_url,
                              "headers": {"Authorization": "Bearer ${user_config.api_token}"}}},
    })
    # Codex (uyumluluk bicimi): kurulumda soru sorma mekanizmasi yok; token ortam
    # degiskeninden Bearer olarak gonderilir.
    dump(base / ".codex-plugin" / "plugin.json", {
        "name": name, "version": VERSION, "description": d["desc"],
        "author": {"name": OWNER["name"], "url": SITE}, "homepage": f"{SITE}/install/{slug}",
        "repository": REPO, "keywords": d["keywords"],
        "skills": "./skills/", "mcpServers": "./codex.mcp.json",
        "interface": {"displayName": d["display"], "shortDescription": d["short"],
                      "longDescription": d["desc"], "developerName": OWNER["name"],
                      "category": "Research", "websiteURL": SITE},
    })
    dump(base / "codex.mcp.json", {"mcpServers": {slug: {
        "type": "http", "url": mcp_url, "bearer_token_env_var": env}}})
    claude_entries.append({"name": name, "source": f"./plugins/{slug}", "description": d["desc"],
                           "category": "research", "keywords": d["keywords"],
                           "homepage": f"{SITE}/install/{slug}"})
    codex_entries.append({"name": name, "source": {"source": "local", "path": f"./plugins/{slug}"},
                          "policy": {"installation": "AVAILABLE"}, "category": "Research"})

dump(ROOT / ".claude-plugin" / "marketplace.json", {
    "name": "searchonair", "description": "Search on Air: Türkçe kaynaklar üzerinde RAG araçları",
    "owner": OWNER, "plugins": claude_entries})
dump(ROOT / ".agents" / "plugins" / "marketplace.json", {
    "name": "searchonair", "interface": {"displayName": "Search on Air"}, "plugins": codex_entries})
print("ok")
