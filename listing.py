# list_neighborhoods.py

def load_neighborhoods(file_path):
    """Mahalle verilerini dosyadan oku ve liste olarak döndür."""
    neighborhoods = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                neighborhoods.append(line.strip())
    except FileNotFoundError:
        print("Hata: Dosya bulunamadı.")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
    return neighborhoods


def list_by_province(neighborhoods, province_name, ascending=True):
    """İl ismine göre mahalleleri listele."""
    matches = []
    for record in neighborhoods:
        parts = record.split('->')
        if len(parts) >= 2:
            # "MAHALLE IL -> ILCE -> ILCE-MERKEZ"
            left_side = parts[0].strip()
            right_side = parts[1].strip()

            neighborhood_name, province = left_side.rsplit(' ', 1)

            if province.upper() == province_name.upper():
                matches.append(record)

    def get_neighborhood_name(record):
        parts = record.split('->')
        left_side = parts[0].strip()
        # Mahalle adı ile il adı arasında son boşluk var
        neighborhood_name = left_side.rsplit(' ', 1)[0].strip()
        return neighborhood_name

    matches.sort(key=get_neighborhood_name, reverse=not ascending)
    return matches


def list_by_district(neighborhoods, province_name, district_name, ascending=True):
    """İl ve ilçe ismine göre mahalleleri listele."""
    matches = []
    for record in neighborhoods:
        parts = record.split('->')
        if len(parts) >= 3:
            left_side = parts[0].strip()
            province_part = parts[1].strip()

            neighborhood_name, province = left_side.rsplit(' ', 1)
            district = province_part

            if province.upper() == province_name.upper() and district.upper() == district_name.upper():
                matches.append(record)

    def get_neighborhood_name(record):
        parts = record.split('->')
        left_side = parts[0].strip()
        # Mahalle adı ile il adı arasında son boşluk var
        neighborhood_name = left_side.rsplit(' ', 1)[0].strip()
        return neighborhood_name

    matches.sort(key=get_neighborhood_name, reverse=not ascending)
    return matches


def main():
    file_path = 'neighborhoods.txt'
    neighborhoods = load_neighborhoods(file_path)

    if not neighborhoods:
        return

    while True:
        print("\n--- MAHALLE LİSTELEME MENÜSÜ ---")
        print("1. Bir ildeki mahalleleri listele")
        print("2. Bir ilçedeki mahalleleri listele")
        print("3. Çıkış")

        choice = input("Seçiminizi yapın (1-2-3): ")

        if choice == '1':
            province = input("İl ismini girin: ").strip()
            order_choice = input("Sıralama (A-Z için 1, Z-A için 2): ").strip()
            ascending = order_choice == '1'
            results = list_by_province(neighborhoods, province, ascending)
            if results:
                print("\nİstediğiniz İldeki Mahalleler:")
                for result in results:
                    # Satırı parse et: "MAHALLE IL -> ILCE -> ILCE-MERKEZ"
                    parts = result.split('->')
                    if len(parts) >= 2:
                        left_side = parts[0].strip()
                        right_side = parts[1].strip()
                        neighborhood_name, province = left_side.rsplit(' ', 1)
                        if len(parts) == 2:
                            # Sadece il var
                            print(f"İl: {province}, Mahalle: {neighborhood_name}")
                        elif len(parts) >= 3:
                            district = parts[1].strip()
                            print(f"İl: {province}, İlçe: {district}, Mahalle: {neighborhood_name}")
                    else:
                        print(result)
            else:
                print("\nUyarı: Girilen ilde mahalle bulunamadı.")

        elif choice == '2':
            province = input("İl ismini girin: ").strip()
            district = input("İlçe ismini girin: ").strip()
            order_choice = input("Sıralama (A-Z için 1, Z-A için 2): ").strip()
            ascending = order_choice == '1'
            results = list_by_district(neighborhoods, province, district, ascending)
            if results:
                print("\nİstediğiniz İlçedeki Mahalleler:")
                for result in results:
                    # Satırı parse et: "MAHALLE IL -> ILCE -> ILCE-MERKEZ"
                    parts = result.split('->')
                    if len(parts) >= 2:
                        left_side = parts[0].strip()
                        right_side = parts[1].strip()
                        neighborhood_name, province = left_side.rsplit(' ', 1)
                        if len(parts) == 2:
                            # Sadece il var
                            print(f"İl: {province}, Mahalle: {neighborhood_name}")
                        elif len(parts) >= 3:
                            district = parts[1].strip()
                            print(f"İl: {province}, İlçe: {district}, Mahalle: {neighborhood_name}")
                    else:
                        print(result)
            else:
                print("\nUyarı: Girilen il ve ilçede mahalle bulunamadı.")

        elif choice == '3':
            print("Programdan çıkılıyor...")
            break

        else:
            print("Geçersiz seçim! Lütfen 1, 2 ya da 3 girin.")


if __name__ == "__main__":
    main()
