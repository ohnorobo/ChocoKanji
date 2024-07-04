
import os
import svgpathtools
from unittest.mock import patch
import xml.etree.ElementTree as ET

import alternative_d


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
ascent="100"
descent="20"
cap-height="90"
x-height="30"
/>
<missing-glyph horiz-adv-x="{x_advance}" d="M 0,0 0,80 80,80 80,0 0,0 M 0,0 80,80 M 20,0 80,60 M 40,0 80,40 M 0,20 60,80"/> 
<glyph unicode=" " glyph-name="space" horiz-adv-x="50" />
"""

footer = """
</font>
</defs>
</svg>"""

KANJI_VG_FOLDER = 'kanjivg location not set'


def fix_path_string(d):
  path = svgpathtools.parse_path(d)

  vertical_flip = svgpathtools.parser.parse_transform('scale(1, -1)')
  shift_up = svgpathtools.parser.parse_transform('translate(0, 49)')
  
  flipped_path = svgpathtools.path.transform(path, vertical_flip)
  shifted_path = svgpathtools.path.transform(flipped_path, shift_up)

  # Monkeypatch svgtools.path.d function
  with patch('svgpathtools.path.Path.d', new=alternative_d.alternative_d):
    return shifted_path.d()

def convert_kanji(svg):
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
    open_file.write(entry)

def main():
  with open('choco-kanji.svg', 'w') as f:
    f.write(header)

    kanji_files = os.listdir(KANJI_VG_FOLDER)
    simple_kanji_files = [filename for filename in kanji_files if len(filename) == 9]
    for kanji_filename in simple_kanji_files:
      write_kanji_file(f, KANJI_VG_FOLDER + kanji_filename)
    
    f.write(footer)


main()