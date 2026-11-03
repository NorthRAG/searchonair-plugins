# Search on Air plugin'leri

Claude Code ve Codex için Search on Air plugin'leri. Her plugin bir veri setine bağlanır ve
o veri setinin MCP araçlarını (`search`, `get_document`, `ask`, `list_sources`) ve bir
araştırma skill'ini getirir.

| plugin | veri seti | MCP adresi |
|---|---|---|
| `searchonair-lawyer` | Hukuk: Yargıtay, Danıştay, UYAP emsal, Anayasa Mahkemesi kararları | `https://api.searchonair.com/lawyer/mcp` |
| `searchonair-accounting` | Muhasebe ve vergi: vergi kanunları, GİB tebliğ/sirküler/özelge, standartlar | `https://api.searchonair.com/accounting/mcp` |
| `searchonair-health` | Sağlık: sağlık mevzuatı, SUT, hasta hakları | `https://api.searchonair.com/health/mcp` |

Kullanmak için bir **Search on Air token'ı** gerekir: https://searchonair.com adresinde kayıt
olun. Kayıtta seçtiğiniz veri seti için ücretsiz bir token (günde 5 soru, 50 arama)
oluşturulur. Token'lar veri setine bağlıdır: her plugin kendi veri setinin token'ını ister.

## Claude Code

```
/plugin marketplace add NorthRAG/searchonair-plugins
/plugin install searchonair-lawyer@searchonair
```

Kurulumda Claude Code token'ı sorar ve işletim sisteminin güvenli deposunda saklar. Tek
adımda: `/plugin install searchonair-lawyer --marketplace NorthRAG/searchonair-plugins`.

Token'ı değiştirmek (yeniledikten sonra): `/plugin configure searchonair-lawyer@searchonair`,
sonra Claude Code'u yeniden başlatın.

Skill'ler `/searchonair-lawyer:legal-research`, `/searchonair-accounting:tax-research`,
`/searchonair-health:health-regulation-research` olarak da çağrılabilir; Claude onları ilgili
sorularda kendisi de kullanır.

## Codex

Codex kurulum sırasında token sormuyor; token bir ortam değişkeninden okunur:

```bash
# ~/.zshrc ya da ~/.bashrc
export SEARCHONAIR_LAWYER_TOKEN=soa_...
```

```bash
codex plugin marketplace add NorthRAG/searchonair-plugins
codex plugin add searchonair-lawyer@searchonair
```

Değişkenler: `SEARCHONAIR_LAWYER_TOKEN`, `SEARCHONAIR_ACCOUNTING_TOKEN`,
`SEARCHONAIR_HEALTH_TOKEN`. Değişikliğin geçerli olması için Codex'i yeni bir terminalde
yeniden başlatın.

## Kotalar

| plan | fiyat | soru (`ask`) / gün | arama + belge okuma / gün |
|---|---:|---:|---:|
| Free | $0 | 5 | 50 |
| Basic | $10/ay | 50 | 500 |
| Pro | $40/ay | 250 | 2.500 |
| Enterprise | $100/ay | 2.000 | 20.000 |

`search` ve `get_document` arama kotasından, `ask` (sunucuda üretilen atıflı cevap) soru
kotasından düşer. Kotalar her gece yarısı (İstanbul saati) sıfırlanır. Her aracın cevabının
sonunda o günkü kullanım yazar.

## Gizlilik

Araç çağrılarındaki sorgular ve sorular Search on Air API'sine gönderilir ve hizmet
kalitesini ölçmek için kaydedilir. Kişisel veri, hasta bilgisi ya da müvekkil sırrı
içeren metinleri sorguya koymayın.

## Geliştirme

Manifestler tek kaynaktan üretilir; adresi ya da sürümü değiştirmek için JSON dosyalarını
elle düzenlemek yerine üretici betiği kullanın (bkz. `scripts/generate.py`). Sürüm
artırılmazsa Claude Code kullanıcıları güncellemeyi almaz.

```bash
python3 scripts/generate.py
claude plugin validate .            # Claude Code doğrulaması
```
