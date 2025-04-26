import unicodedata

def turkish_normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').casefold()

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
    search_words = search_name.strip().split()
    word_count = len(search_words)
    for record in neighborhoods:
        record_words = record.strip().split()
        neighborhood_name = ' '.join(record_words[:word_count])
        if turkish_normalize(neighborhood_name) == turkish_normalize(search_name):
            matches.append(record)
    return matches

def partial_search(neighborhoods, search_name):
    """Arama terimi ne olursa olsun, kayıttaki ilk iki kelimede arama yap."""
    matches = []
    for record in neighborhoods:
        record_words = record.strip().split()
        neighborhood_name = ' '.join(record_words[:2])
        if turkish_normalize(search_name) in turkish_normalize(neighborhood_name):
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