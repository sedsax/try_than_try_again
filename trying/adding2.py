import os

def load_neighborhoods(file_path):
    """Mahalle verilerini dosyadan oku ve liste olarak döndür."""
    neighborhoods = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    neighborhoods.append(line)
    except FileNotFoundError:
        print("Hata: neighborhoods.txt dosyası bulunamadı.")
    except Exception as e:
        print(f"Okuma hatası: {e}")
    return neighborhoods

def save_neighborhoods(file_path, neighborhoods):
    """Mahalle listesini dosyaya kaydet."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            for item in neighborhoods:
                file.write(item + "\n")
    except Exception as e:
        print(f"Yazma hatası: {e}")

def parse_neighborhood(line):
    """Bir satırı mahalle, il, ilçe olarak ayır."""
    try:
        parts = line.split("->")
        neighborhood = parts[0].strip()
        province = parts[1].strip() if len(parts) > 1 else ""
        district = parts[2].strip() if len(parts) > 2 else ""
        return neighborhood, province, district
    except Exception:
        return "", "", ""

def add_neighborhood(file_path):
    """Kullanıcıdan mahalle, il ve ilçe alıp ekleme işlemini yapar."""
    neighborhoods = load_neighborhoods(file_path)
    if not neighborhoods:
        return

    while True:
        new_neigh = input("Yeni mahalle adını girin: ").strip().upper()
        province = input("İl adını girin: ").strip().upper()
        district = input("İlçe adını girin: ").strip().upper()

        # Aynı mahalle, il ve ilçe var mı kontrol et
        exists = False
        for line in neighborhoods:
            n, p, d = parse_neighborhood(line)
            if n == new_neigh and p == province and d == district:
                exists = True
                break

        if exists:
            print("Bu mahalle zaten mevcut! Lütfen farklı bir mahalle girin.")
            continue

        # Format: MAHALLE İL -> İLÇE -> İLÇE-DISTRICT CENTER
        new_line = f"{new_neigh} {province} -> {district} -> {district}-DISTRICT CENTER"
        neighborhoods.append(new_line)
        save_neighborhoods(file_path, neighborhoods)
        print("Mahalle başarıyla eklendi.\n")
        list_neighborhoods(neighborhoods, province, district)
        break

def list_neighborhoods(neighborhoods, province, district):
    """Belirtilen il ve ilçedeki mahalleleri listeler."""
    print(f"\n{province} ili, {district} ilçesindeki mahalleler:")
    found = False
    for line in neighborhoods:
        n, p, d = parse_neighborhood(line)
        if p == province and d == district:
            print("-", n)
            found = True
    if not found:
        print("Kayıtlı mahalle bulunamadı.")

def main():
    file_path = "neighborhoods.txt"
    add_neighborhood(file_path)

if __name__ == "__main__":
    main()