#Universal Rule-Based Classification Framework
#Bu proje, herhangi bir müşteri veri setini (User-Level Data) profesyonelce segmente etmek ve potansiyel gelir tahmini yapmak için kullanılan evrensel bir iş akışı sunar. Veri setiniz değişse bile takip etmeniz gereken 4 altın adım aşağıdadır.

#🚀 Uygulama Adımları (Step-by-Step Pipeline)
#Bir veri bilimci olarak, elindeki ham veriyi şu sırayla işlemen gerekir:

#Adım 1: Veriyi "Mikro-Segment" Seviyesinde Tekilleştirme
#Ham veri setinde aynı kullanıcı birden fazla işlem yapmış olabilir. İlk görevimiz, tüm demografik özellikleri (Ülke, Cihaz, Cinsiyet vb.) baz alarak veriyi gruplamak ve ortalama kazancı (PRICE) hesaplamaktır.

#Python
# VERİDEN BAĞIMSIZ KOD (Generic Code):
# 'features' listesine elinizdeki kategorik sütunları yazın.
features = ["COUNTRY", "SOURCE", "SEX", "AGE"] 
target = "PRICE"

agg_df = df.groupby(features).agg({target: "mean"}).sort_values(target, ascending=False).reset_index()

#Adım 2: Sayısal Değişkenleri Kategorize Etme (Binning)
#Yaş gibi sürekli sayısal verileri kurallara dökebilmek için aralıklara (bins) bölmelisiniz. Bu, modelin "gürültüden" kurtulmasını ve daha genel kurallar koymasını sağlar.

#Python
# Yaş aralıklarını veriye göre belirleyin
bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]
labels = ["0_18", "19_23", "24_30", "31_40", "41_plus"]

agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], bins=bins, labels=labels)

#Adım 3: Seviye Tabanlı Persona Tanımlama (Persona Engineering)
#Tüm demografik özellikleri tek bir "Kural Dizisi" (String) haline getiriyoruz. Bu, her bir müşteri tipine bir "isim" vermek gibidir.

#Python
# Tüm sütunları birleştirerek tek bir kimlik oluşturma
# Örn: TUR_ANDROID_FEMALE_24_30
agg_df["customers_level_based"] = agg_df[features[:-1] + ["AGE_CAT"]].apply(lambda x: '_'.join(x).upper(), axis=1)

# Aynı personadan birden fazla satır kalmış olabilir, tekrar ortalama alarak tekilleştirin:
agg_df = agg_df.groupby("customers_level_based").agg({target: "mean"}).reset_index()

# Adım 4: İstatistiksel Segmentasyon (Quartile-Based)
# Müşterileri kazandırdıkları paraya göre 4 ana gruba (A, B, C, D) ayırıyoruz. Bu, istatistiksel bir "qcut" işlemidir.

# Python
# En değerli %25 'A', en az değerli %25 'D' segmenti olur.
agg_df["SEGMENT"] = pd.qcut(agg_df[target], 4, labels=["D", "C", "B", "A"])

# 📈 Yeni Gelen Veriyi Sınıflandırma (Tahmin)
# Sistem kurulduktan sonra, sisteme hiç girmemiş bir kullanıcıyı şu fonksiyonla anında tahmin edebilirsiniz:

# Python
def predict_new_user(persona_string):
    result = agg_df[agg_df["customers_level_based"] == persona_string.upper()]
    return result

# Kullanım:
# predict_new_user("FRA_IOS_FEMALE_31_40")

# 💎 Neden Bu Metot?
# Esnektir: Sütun isimlerini değiştirerek her veriye uyarlayabilirsiniz.

# Açıklanabilirdir: "Neden bu segmentte?" sorusuna "Çünkü bu kurala uyuyor" diyebilirsiniz (Black box değildir).

# Profesyoneldir: İstatistiki çeyreklikler (qcut) kullanarak objektif bir gruplama yapar.# Universal-Rule-Based-Classification-Framework
# Universal-Rule-Based-Classification-Framework
# Universal-Rule-Based-Classification-Framework
# Universal-Rule-Based-Classification-Framework

