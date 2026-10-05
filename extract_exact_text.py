import fitz

doc = fitz.open('4498470078- FourteenPark Amenities & Lifestyle Eblast V2.pdf')
page = doc[0]

with open('exact_text_analysis.txt', 'w', encoding='utf-8') as f:
    for b in page.get_text('dict')['blocks']:
        if b.get('type') == 0:
            for l in b['lines']:
                s = ''.join([sp['text'] for sp in l['spans']])
                font = l['spans'][0]['font']
                size = l['spans'][0]['size']
                color = f"#{l['spans'][0]['color']:06x}"
                f.write(f"({font}, {size:.1f}pt, {color}): {s}\n")

print("Saved exact_text_analysis.txt")
