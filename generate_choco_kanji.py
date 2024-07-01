# Derived from https://github.com/NicholasARossi/generative_artforms/blob/main/generative_fonts/chinese/generate_chinese_font.py

import pandas as pd
import xml.etree.ElementTree as ET
from pprint import pprint


header = """<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd" >

<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">

<metadata>

</metadata>
<defs>
<font id="ChocoKanji SVG" horiz-adv-x="378" >
<font-face
font-family="ChocoKanji SVG"
units-per-em="1000"
ascent="800"
descent="-200"
cap-height="500"
x-height="300"
/>
<missing-glyph horiz-adv-x="800"/>
"""
footer = """
</font>
</defs>
</svg>"""

x_advance = 1000

KANJI_VG_FOLDER = ""


def convert_string_strokes(strokes):
  running_string = ''
  for stroke in strokes:
    current_stroke = ''
    for i, substroke in enumerate(stroke):
      if i == 0:
        current_stroke += f'M {substroke[0]} {substroke[1]} '
      else:
        current_stroke += f'L {substroke[0]} {substroke[1]} '
    running_string += current_stroke
  return running_string
  
def convert_full_entry(row):
  return f'<glyph unicode="{row.character}" glyph-name="{row.character}" horiz-adv-x="{x_advance}" d="{row.combined_lines}"/>\n'


def fix_path_string(p):
  p = p.rstrip()
  p = p.replace("M", "M ")
  p = p.replace("c", " C ")
  p = p.replace(",", " ")

  return p

def convert_kanji(svg: str) -> str:
  root = ET.fromstring(svg)

  character = root[0][0].attrib['{http://kanjivg.tagaini.net}element']

  svg_paths = root.findall(".//*[@d]")
  pprint(svg_paths)

  paths = [fix_path_string(path.attrib['d']) for path in svg_paths]
  pprint(paths)
  print(repr(paths[0]))

  combined_strokes = " ".join(paths)
  pprint(combined_strokes)
  pprint(type(combined_strokes))

  return f'<glyph unicode="{character}" glyph-name="{character}" horiz-adv-x="{x_advance}" d="{combined_strokes}"/>\n'

def main():
  df = pd.read_json('makemeahanzi.json', lines=True)
  df['combined_lines'] = df.medians.apply(convert_string_strokes)
  df['full_entries'] = df.apply(lambda x: convert_full_entry(x), axis=1)
  with open('choco-kanji.svg', 'w') as f:
    f.write(header)
    for entry in df['full_entries'].values:
      f.write(entry)
    f.write(footer)

def main2():
  with open('choco-kanji.svg', 'w') as f:
    f.write(header)

    with open('04e56.svg', 'r') as example_kanji:
      example_kanji_svg: str = example_kanji.read()
      entry = convert_kanji(example_kanji_svg)
      f.write(entry)

    f.write(footer)


main2()