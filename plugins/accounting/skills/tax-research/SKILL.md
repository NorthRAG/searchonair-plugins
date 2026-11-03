---
name: tax-research
description: Türk vergi ya da muhasebe mevzuatıyla ilgili bir soru sorulduğunda kullan (VUK, KDV, gelir/kurumlar vergisi, e-fatura, GİB tebliğ/sirküler/özelgeleri, muhasebe standartları). Search on Air muhasebe araçlarıyla (search, get_document, ask) ilgili mevzuatı bulur, okur ve madde numarasıyla atıf yapar.
---

# Vergi ve muhasebe mevzuatı araştırması (Search on Air)

Bu plugin, Search on Air muhasebe ve vergi veri setine bağlanır: vergi kanunları, GİB
tebliğ/sirküler/özelgeleri ve muhasebe standartları. Araçlar `accounting` MCP sunucusundadır.

| araç | ne zaman | kota |
|---|---|---|
| `search` | Her araştırmanın ilk adımı. Birkaç kez, farklı terimlerle çağır. | arama |
| `get_document` | İlgili kanun maddesini/tebliği tam okumak için. Uzunsa `offset` ile devam et. | arama |
| `ask` | Kullanıcı hızlı, hazır ve atıflı bir cevap istiyorsa. | soru (düşük) |
| `list_sources` | Kaynakların kapsamını görmek için. | yok |

## Akış

1. **Konuyu belirle:** hangi vergi/kanun (VUK, KDVK, GVK, KVK...), hangi dönem? Mükellefin
   türü (gerçek kişi, şirket, basit usul) önemli mi?
2. **Ara:** mevzuat diliyle sorgula ("faturanın düzenlenme süresi", "indirim hakkının
   kullanılma zamanı"). Kanun ve madde numarası geçiyorsa `mode: "hybrid"`. Kanun metni ile
   uygulamayı açıklayan tebliği birlikte bul.
3. **Oku:** cevabı taşıyan maddeleri `get_document` ile aç; istisnaları ve yürürlük
   tarihlerini kontrol et.
4. **Yaz:** önce kısa cevap, sonra gerekçe. Her tespitte belgenin adını ve maddesini ver
   ("213 sayılı VUK md. 231/5"). **Tutar, oran ve hadler yıl yıl değişir:** hangi tarihli
   metne dayandığını yaz, güncelliğinin doğrulanması gerektiğini belirt.
5. **Sınırla:** belgelerde olmayanı mevzuata dayandırma. Sonda bunun genel bilgi olduğunu ve
   somut durum için mali müşavire danışılması gerektiğini söyle.

## Hatalar

- **Token yok/geçersiz:** https://searchonair.com/dashboard adresinden token alınmalı; Claude
  Code'da `/plugin configure searchonair-accounting@searchonair`, Codex'te
  `SEARCHONAIR_ACCOUNTING_TOKEN` ortam değişkeni.
- **Veri seti henüz yüklenmedi:** araç bunu söyler; kullanıcıya bildir, mevzuat uydurma.
- **Kota doldu:** günlük hak gece yarısı (İstanbul saati) sıfırlanır; `ask` bittiyse
  `search` + `get_document` ile devam edilebilir.
