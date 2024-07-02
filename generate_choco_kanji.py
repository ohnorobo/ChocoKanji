import pandas as pd
import xml.etree.ElementTree as ET
from pprint import pprint
import svgpathtools

x_advance = 109

header = f"""<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd" >

<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">

<metadata>

</metadata>
<defs>
<font id="ChocoKanji SVG" horiz-adv-x="{x_advance}" >
<font-face
font-family="ChocoKanji SVG"
units-per-em="{x_advance}"
ascent="80"
descent="-20"
cap-height="50"
x-height="30"
/>
<missing-glyph horiz-adv-x="{x_advance}" d="M 0,0 0,80 80,80 80,0 0,0 M 0,0 80,80 M 20,0 80,60 M 40,0 80,40 M 0,20 60,80"/> 
"""
footer = """
</font>
</defs>
</svg>"""

alt_header = """<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd" >

<svg xmlns="http://www.w3.org/2000/svg" width="{x_advance}" height="{x_advance}" viewBox="0 0 {x_advance} {x_advance}">
<g style="fill:none;stroke:#000000;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;">
"""

alt_footer = """
</g>
</svg>"""




KANJI_VG_FOLDER = ""


def flip_svg_path(d):
  path = svgpathtools.parse_path(d)
  pprint(("p", path))

  vertical_flip = svgpathtools.parser.parse_transform('scale(1, -1)')
  shift_up = svgpathtools.parser.parse_transform('translate(0, 59)')
  
  flipped_path = svgpathtools.path.transform(path, vertical_flip)
  shifted_path = svgpathtools.path.transform(flipped_path, shift_up)
  pprint(shifted_path)

  return shifted_path.d()


def fix_path_string(p):
  p = p.rstrip()
  p = flip_svg_path(p)
  return p

def convert_kanji(svg: str) -> str:
  root = ET.fromstring(svg)

  character = root[0][0].attrib['{http://kanjivg.tagaini.net}element']

  svg_paths = root.findall(".//*[@d]")
  paths = [fix_path_string(path.attrib['d']) for path in svg_paths]
  combined_strokes = " ".join(paths)

  return f'<glyph unicode="{character}" glyph-name="{character}" horiz-adv-x="{x_advance}" d="{combined_strokes}" />\n'


def write_kanji_file(open_file, kanji_filename):
  with open(kanji_filename, 'r') as example_kanji:
    example_kanji_svg: str = example_kanji.read()
    entry = convert_kanji(example_kanji_svg)

    pprint(entry)

    open_file.write(entry)

def main():
  with open('choco-kanji.svg', 'w') as f:
    f.write(header)

    write_kanji_file(f, '04e56.svg')
    write_kanji_file(f, '04e57.svg')
    write_kanji_file(f, '04e58.svg')
    
    f.write(footer)


main()