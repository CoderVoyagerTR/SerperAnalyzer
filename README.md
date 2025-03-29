# SEO Position Checker

SEO Position Checker, Serper.dev API'sini kullanarak birden fazla domainın Google arama sonuçlarındaki pozisyonlarını takip etmenizi sağlayan bir Streamlit uygulamasıdır.

## Özellikler

- Birden fazla domainın pozisyonlarını aynı anda kontrol edin
- Organik arama ve görsel arama sonuçlarını görüntüleyin
- Farklı lokasyonlar (Türkiye ve ABD) ve diller için arama yapın
- "İnsanlar Ayrıca Şunu Soruyor" ve "İlgili Aramalar" bilgilerini görüntüleyin
- Sonuçları CSV veya Excel olarak dışa aktarın
- Görsel aramalarda hem sayfa URL'si hem de görsel URL'si bilgilerini görüntüleyin

## Kurulum

1. Bu repo'yu klonlayın:
```bash
git clone https://github.com/your-username/seo-position-checker.git
cd seo-position-checker
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Serper.dev API anahtarınızı ayarlayın:
   - [Serper.dev](https://serper.dev) sitesinden bir API anahtarı alın
   - `.streamlit/secrets.toml.example` dosyasını `.streamlit/secrets.toml` olarak kopyalayın
   - `secrets.toml` dosyasında `your_serper_api_key_here` kısmını kendi API anahtarınızla değiştirin

## Kullanım

Uygulamayı başlatmak için:
```bash
streamlit run app.py
```

### Streamlit Cloud'da Çalıştırma

Bu uygulamayı [Streamlit Cloud](https://streamlit.io/cloud) üzerinde de çalıştırabilirsiniz:

1. GitHub reponuzu Streamlit Cloud'a bağlayın
2. Settings > Secrets bölümünde API anahtarınızı ekleyin:
   - Anahtar adı: `api_keys.serper`
   - Değer: Serper.dev API anahtarınız

## Nasıl Kullanılır?

1. Domainleri satır satır girin (örn., example.com, mysite.com)
2. Anahtar kelimeleri satır satır girin (örn., en iyi ayakkabılar, dijital pazarlama)
3. Arama tipini seçin: Organik Arama veya Görsel Arama
4. Lokasyon seçin: Türkiye (varsayılan) veya ABD
5. Sonuç boyutu seçin (10 ila 100)
6. "Pozisyonları Kontrol Et" butonuna tıklayın

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır - detaylar için LICENSE dosyasına bakın.

## İletişim

Sorularınız veya önerileriniz varsa, lütfen GitHub üzerinden issue açın.