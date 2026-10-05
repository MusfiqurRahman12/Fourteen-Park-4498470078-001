import fitz

doc = fitz.open('4498470078- FourteenPark Amenities & Lifestyle Eblast V2.pdf')
page = doc[0]

with open('pdf_structure.txt', 'w', encoding='utf-8') as out:
    out.write(f"Page rect: {page.rect.width} x {page.rect.height}\n")
    
    images = page.get_images(full=True)
    out.write(f"\nTotal images embedded: {len(images)}\n")
    for i, img in enumerate(images):
        xref = img[0]
        base_image = doc.extract_image(xref)
        out.write(f"Image {i} (xref {xref}): {base_image['width']}x{base_image['height']}, {base_image['ext']}, {base_image['colorspace']}\n")

    out.write("\n--- TEXT BLOCKS ---\n")
    text_dict = page.get_text("dict")
    for block in text_dict["blocks"]:
        if block.get("type") == 0:
            for line in block["lines"]:
                spans_str = " | ".join([f"'{s['text']}' (font={s['font']}, sz={s['size']:.1f}, col=#{s['color']:06x})" for s in line["spans"]])
                bbox = [round(x, 1) for x in line["bbox"]]
                out.write(f"Line bbox {bbox}: {spans_str}\n")
        elif block.get("type") == 1:
            out.write(f"Image block: bbox={[round(x, 1) for x in block['bbox']]}\n")

    out.write("\n--- RECTANGLES / BACKGROUNDS ---\n")
    for d in page.get_drawings():
        if d.get("fill"):
            out.write(f"Fill {d['fill']} rect {[round(x, 1) for x in d['rect']]}\n")

print("Saved pdf_structure.txt")
