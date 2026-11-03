---
name: health-regulation-research
description: Türkiye'deki sağlık sistemi, hasta hakları, SGK sağlık kapsamı (SUT, katılım payı), aile hekimliği ya da sağlık mevzuatıyla ilgili bir soru sorulduğunda kullan. Search on Air sağlık araçlarıyla (search, get_document, ask) resmî kaynakları bulur, okur ve madde numarasıyla atıf yapar. Teşhis ya da tedavi önerisi için değildir.
---

# Sağlık mevzuatı araştırması (Search on Air)

Bu plugin, Search on Air sağlık veri setine bağlanır: sağlık mevzuatı, SGK Sağlık Uygulama
Tebliği (SUT), hasta hakları ve resmî sağlık bilgilendirmeleri. Araçlar `health` MCP
sunucusundadır.

| araç | ne zaman | kota |
|---|---|---|
| `search` | Her araştırmanın ilk adımı. Birkaç kez, farklı terimlerle çağır. | arama |
| `get_document` | İlgili yönetmelik/tebliğ maddesini tam okumak için. | arama |
| `ask` | Kullanıcı hızlı, hazır ve atıflı bir cevap istiyorsa. | soru (düşük) |
| `list_sources` | Kaynakların kapsamını görmek için. | yok |

## Akış

1. **Sorunun türünü belirle:** hasta hakkı mı, SGK kapsamı/ödeme mi, sağlık kuruluşu
   işleyişi mi? Teşhis, tedavi ya da ilaç dozu soruluyorsa bu plugin'in kapsamı dışında
   olduğunu söyle ve hekime yönlendir. **Acil bir durum anlatılıyorsa 112'yi hatırlat.**
2. **Ara:** mevzuat diliyle sorgula ("tıbbi kayıtlara erişim hakkı", "aile hekimi değişikliği",
   "reçete katılım payı muafiyeti").
3. **Oku:** cevabı taşıyan maddeleri `get_document` ile aç; istisnaları ve değişiklik
   tarihlerini kontrol et.
4. **Yaz:** önce kısa cevap, sonra gerekçe; her tespitte belgenin adını ve maddesini ver.
   Tutar ve süreler değişebilir: hangi tarihli metne dayandığını yaz.
5. **Sınırla:** belgelerde olmayanı mevzuata dayandırma. Sonda bunun genel bilgi olduğunu,
   tıbbi ya da hukuki tavsiye olmadığını, somut durum için hekime veya ilgili sağlık
   kuruluşuna danışılması gerektiğini söyle.

## Hatalar

- **Token yok/geçersiz:** https://searchonair.com/dashboard adresinden token alınmalı; Claude
  Code'da `/plugin configure searchonair-health@searchonair`, Codex'te
  `SEARCHONAIR_HEALTH_TOKEN` ortam değişkeni.
- **Veri seti henüz yüklenmedi:** araç bunu söyler; kullanıcıya bildir, bilgi uydurma.
- **Kota doldu:** günlük hak gece yarısı (İstanbul saati) sıfırlanır.
