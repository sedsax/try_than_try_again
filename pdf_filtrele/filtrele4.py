import fitz  # PyMuPDF
import pandas as pd

# PDF dosyasını aç
pdf_path = "kontenjanlar.pdf"
doc = fitz.open(pdf_path)

# Tüm sayfalardan metni al
full_text = ""
for page in doc:
    full_text += page.get_text()

# Satırları ayır ve "EBE" geçenleri filtrele
lines = full_text.split("\n")
ebe_satirlari = []
for i in range(len(lines)):
    if lines[i].strip() == "EBE":
        # Önceki ve sonraki 5 satırla birlikte al (bağlam için)
        start = max(0, i - 4)
        end = min(len(lines), i + 5)
        ebe_satirlari.append("\n".join(lines[start:end]))
        ebe_satirlari.append("-" * 40)  # Ayraç

# Sonuçları Excel dosyasına yaz
output_excel = "ebe_sonuclar.xlsx"
df = pd.DataFrame({'EBE_Satirlari': ebe_satirlari})
df.to_excel(output_excel, index=False)
print(f"Sonuçlar '{output_excel}' dosyasına kaydedildi.")
