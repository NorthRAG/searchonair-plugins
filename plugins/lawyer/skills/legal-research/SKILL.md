---
name: legal-research
description: Türk hukukuyla ilgili bir soru, dava, içtihat ya da mahkeme kararı araştırması istendiğinde kullan. Search on Air hukuk araçlarıyla (search, get_document, ask) Yargıtay, Danıştay, UYAP emsal ve Anayasa Mahkemesi kararlarını bulur, okur ve künyeyle atıf yapar.
---

# Türk içtihat araştırması (Search on Air)

Bu plugin, 11 milyonu aşkın Türk mahkeme kararını içeren Search on Air hukuk veri setine
bağlanır. Araçlar `lawyer` MCP sunucusundadır.

| araç | ne zaman | kota |
|---|---|---|
| `search` | Her araştırmanın ilk adımı. Birkaç kez, farklı terimlerle çağır. | arama |
| `get_document` | Önemli görünen kararın tam metnini okumak için. Uzunsa `offset` ile devam et. | arama |
| `ask` | Kullanıcı hızlı, hazır ve atıflı bir cevap istiyorsa. Sunucuda LLM çalışır. | soru (düşük) |
| `list_sources` | Kaynakların kapsamını görmek için. | yok |

## Akış

1. **Soruyu ayrıştır.** Hangi hukuk dalı? Özel hukuk mu (Yargıtay hukuk daireleri + emsal),
   idare/vergi mi (Danıştay), temel hak ihlali mi (AYM bireysel başvuru), kanunun Anayasa'ya
   uygunluğu mu (AYM norm denetimi)? Tarih kısıtı var mı?
2. **Ara.** `search` sorgusunu kararlarda geçecek hukuki terimlerle yaz: "kıdem tazminatı haklı
   fesih ücretin ödenmemesi" gibi. Kanun/madde numarası, esas/karar numarası gibi lafzi
   ifadeler için `mode: "hybrid"` ya da `"sparse"` kullan. Kaynak ve yıl filtrelerini yalnızca
   soru gerektiriyorsa koy. İlk sonuçlar zayıfsa eş anlamlı terimlerle ya da filtresiz tekrar ara.
3. **Oku.** Cevabı taşıyacak 2-4 kararı `get_document` ile aç. Arama parçası kararın sonucunu
   göstermeyebilir; hükmü ve gerekçeyi tam metinden doğrula.
4. **Yaz.** Önce kısa cevap, sonra gerekçe. Her tespitin yanına kararın künyesini aynen yaz
   (ör. "Yargıtay 9. Hukuk Dairesi, E. 2015/4260, K. 2015/11423, T. 12.03.2015"). Kararlar
   arasında görüş ayrılığı varsa ikisini de tarihleriyle göster; daire ve iş bölümü yıllar
   içinde değişti, eski kararları buna göre değerlendir.
5. **Sınırla.** Kararlarda olmayan bilgiyi kararlara dayandırma; genel hukuk bilgini ayrıca ve
   açıkça belirt. Sonda bunun hukuki danışmanlık olmadığını, somut olay için avukata
   danışılması gerektiğini söyle.

## Hatalar

- **Token yok/geçersiz:** Araç ne yapılacağını söyler. Kullanıcıya https://searchonair.com/dashboard
  adresinden token almasını, Claude Code'da `/plugin configure searchonair-lawyer@searchonair`
  ile girmesini (Codex'te `SEARCHONAIR_LAWYER_TOKEN` ortam değişkeni) ilet.
- **Kota doldu:** Günlük hak gece yarısı (İstanbul saati) sıfırlanır. Kullanıcıya bildir;
  `ask` kotası bittiyse `search` + `get_document` ile devam edebilirsin.
- **Sonuç yok:** Sorguyu genelleştir, filtreleri kaldır, eş anlamlı terim dene. Hâlâ yoksa
  bunu açıkça söyle; karar uydurma.
