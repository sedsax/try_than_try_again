# neighborhoods_module.py

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


def exact_search(neighborhoods, search_name):
    """Tam isim eşleşmesiyle mahalle araması yap."""
    matches = []
    for record in neighborhoods:
        neighborhood_name = record.split(' ')[0]
        if neighborhood_name.upper() == search_name.upper():
            matches.append(record)
    return matches


def partial_search(neighborhoods, search_term):
    """Parçalı isim eşleşmesiyle mahalle araması yap."""
    matches = []
    for record in neighborhoods:
        neighborhood_name = record.split(' ')[0]
        if search_term.upper() in neighborhood_name.upper():
            matches.append(record)
    return matches


def main():
    file_path = 'neighborhoods.txt'
    neighborhoods = load_neighborhoods(file_path)

    if not neighborhoods:
        return

    while True:
        print("\n--- MAHALLE ARAMA MENÜSÜ ---")
        print("1. Tam Eşleşme ile Mahalle Arama")
        print("2. Kısmi Eşleşme ile Mahalle Arama")
        print("3. Çıkış")

        choice = input("Seçiminizi yapın (1-2-3): ")

        if choice == '1':
            search_name = input("Aramak istediğiniz mahalle adını tam olarak girin: ").strip()
            results = exact_search(neighborhoods, search_name)
            if results:
                print("\nBulunan Mahalleler:")
                for result in results:
                    print(result)
            else:
                print("\nUyarı: Aranan isimde mahalle bulunamadı.")

        elif choice == '2':
            search_term = input("Aramak istediğiniz mahalle adının bir parçasını girin: ").strip()
            results = partial_search(neighborhoods, search_term)
            if results:
                print("\nBulunan Mahalleler:")
                for result in results:
                    print(result)
            else:
                print("\nUyarı: Aranan ismin parçasını içeren mahalle bulunamadı.")

        elif choice == '3':
            print("Programdan çıkılıyor...")
            break

        else:
            print("Geçersiz seçim! Lütfen 1, 2 ya da 3 girin.")


if __name__ == "__main__":
    main()
