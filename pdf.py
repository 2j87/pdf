from pypdf import PdfReader, PdfWriter, Transformation

def scale_pdf(input_file, output_file, scale_factor):
    reader = PdfReader(input_file)
    writer = PdfWriter()

    for page in reader.pages:
        # 1. Mevcut sayfa sınırlarını al
        mb = page.mediabox
        
        # 2. İçeriği ölçeklendirme objesini oluştur
        op = Transformation().scale(scale_factor, scale_factor)
        page.add_transformation(op)

        # 3. Sayfanın tüm sınırlarını (kutularını) 5 katına çıkar
        # Sadece içeriği değil, 'kağıdı' da büyütüyoruz.
        page.mediabox.lower_left = (float(mb.left) * scale_factor, float(mb.bottom) * scale_factor)
        page.mediabox.upper_right = (float(mb.right) * scale_factor, float(mb.top) * scale_factor)
        
        # Varsa CropBox (kesme sınırı) gibi diğer kutuları da güncellemek gerekebilir
        if "/CropBox" in page:
            cb = page.cropbox
            page.cropbox.lower_left = (float(cb.left) * scale_factor, float(cb.bottom) * scale_factor)
            page.cropbox.upper_right = (float(cb.right) * scale_factor, float(cb.top) * scale_factor)

        writer.add_page(page)

    with open(output_file, "wb") as f:
        writer.write(f)

# Kullanım:
scale_pdf("giris.pdf", "cikis_tam_boyut.pdf", 5)