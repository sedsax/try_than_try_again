import matplotlib.pyplot as plt
from collections import defaultdict
import unicodedata


def turkish_normalize(text):
    if not isinstance(text, str):
        return ''
    text = text.strip().lower()
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')


def turkish_upper(text):
    replacements = str.maketrans({
        'i': 'İ', 'ı': 'I',
        'ş': 'Ş', 'ğ': 'Ğ',
        'ü': 'Ü', 'ö': 'Ö',
        'ç': 'Ç'
    })
    parts = text.strip().split()
    result = []
    for word in parts:
        result.append(word.translate(replacements).upper())
    return ' '.join(result)


def read_lines(file_path):
    try:
        with open(file_path, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []


def count_neighborhoods_by_district(province_name, lines):
    counts = defaultdict(int)
    normalized_province = turkish_normalize(province_name)
    merkez_kume = {normalized_province, 'merkez', 'province'}

    for line in lines:
        parts = line.split("->")
        if len(parts) >= 2:
            left = parts[0].strip()
            right = [p.strip() for p in parts[1:]]
            left_parts = left.split()
            if len(left_parts) < 2:
                continue
            mahalle = " ".join(left_parts[:-1])
            province = left_parts[-1]
            if turkish_normalize(province) != normalized_province:
                continue
            district = right[0] if right else "Bilinmeyen"
            # Eğer district il adı ile aynıysa ve başka parça varsa, ikinci parçayı district olarak al
            if turkish_normalize(district) == normalized_province and len(right) > 1:
                district = right[1]
            # Sondaki merkez tipi gibi ekleri at, sadece ilk ilçe adını al
            district_clean = district.split("-")[0].strip()
            district_norm = turkish_normalize(district_clean)
            # Merkez kümeye dahilse anahtar olarak 'MERKEZ' kullan
            if district_norm in merkez_kume:
                counts['MERKEZ'] += 1
            else:
                counts[turkish_upper(district_clean)] += 1
    return counts


def plot_bar_chart(province, counts):
    if not counts:
        print("Girilen ilde mahalle verisi bulunamadı.")
        return

    districts = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(districts, values, color='skyblue')
    plt.title(f"{turkish_upper(province)} İli İlçelere Göre Mahalle Sayısı")
    plt.xlabel("İlçeler")
    plt.ylabel("Mahalle Sayısı")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_pie_chart(province, counts):
    if not counts:
        print("Girilen ilde mahalle verisi bulunamadı.")
        return

    districts = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=districts, autopct='%1.1f%%', startangle=140)
    plt.title(f"{turkish_upper(province)} İli İlçelere Göre Mahalle Dağılımı")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    file_path = "neighborhoods.txt"
    lines = read_lines(file_path)

    province = input("İl adı girin: ")
    counts = count_neighborhoods_by_district(province, lines)

    chart_type = input("Grafik türü seçin (bar/pie): ").lower().strip()
    if chart_type == "bar":
        plot_bar_chart(province, counts)
    elif chart_type == "pie":
        plot_pie_chart(province, counts)
    else:
        print("Geçersiz grafik türü. Lütfen 'bar' veya 'pie' girin.")
