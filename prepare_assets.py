"""
Prepare final, email-ready image assets into ./ftp-upload/ (LOCAL ONLY - nothing is uploaded).

Outputs (file names must match the <img src> names in index.html):
  hero.jpg            650x574 @2x (1300x1148) baseline JPEG (Outlook-safe, not progressive)
  logo-fourteen-park.png   350x170 @2x transparent PNG with a soft brand-brown halo
  footer-logos.png         650x65  @2x transparent PNG with a soft brand-brown halo

Why the halo: the logos are white. If a dark-mode client recolors the brown section
background, a baked-in brown box would show as a visible rectangle, while a plain
transparent PNG could become invisible on a lightened background. A transparent PNG
with a #3F342A halo blends invisibly into the brand brown and still outlines the
white artwork on any other background.
"""
import os
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ftp-upload")
BRAND_BROWN = (63, 52, 42)  # #3F342A

os.makedirs(OUT, exist_ok=True)


def halo_png(src, dst, grow=5, blur=1.6, strength=0.9):
    im = Image.open(os.path.join(HERE, src)).convert("RGBA")
    alpha = im.getchannel("A")
    halo_a = alpha.filter(ImageFilter.MaxFilter(grow)).filter(ImageFilter.GaussianBlur(blur))
    halo_a = halo_a.point(lambda p: int(min(255, p * strength * 1.6)))
    halo = Image.new("RGBA", im.size, BRAND_BROWN + (0,))
    halo.putalpha(halo_a)
    halo.alpha_composite(im)
    halo.save(os.path.join(OUT, dst), optimize=True)
    print(dst, halo.size, os.path.getsize(os.path.join(OUT, dst)) // 1024, "KB")


def hero(src, dst, quality=84):
    im = Image.open(os.path.join(HERE, src)).convert("RGB")
    im.save(os.path.join(OUT, dst), "JPEG", quality=quality, optimize=True, progressive=False, subsampling=0)
    print(dst, im.size, os.path.getsize(os.path.join(OUT, dst)) // 1024, "KB")


if __name__ == "__main__":
    hero("hero_banner_2x.png", "hero.jpg")
    halo_png("logo-fourteen-park-trans.png", "logo-fourteen-park.png")
    halo_png("footer-logos-trans.png", "footer-logos.png")
