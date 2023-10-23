import openai

with open("secrets/openai.txt", "r") as file:
    openai.api_key = file.read().strip()

statement = "the new season of rick and morty sucks"

prompt = """
    Dissect the statement at the bottom into the following fields.
    Each answer should be 1 to 5 words long.
    If one field is not mentioned in the statement, infer what it would be in relation to the other fields.
        1. Subject: The subject that is covetting something
        2. New Thing: The thing that is being covetted
        3. Old Thing: The thing being cast asside, forgotten, replaced

"""
prompt += statement

messages = [
    {"role": "user", "content": prompt},
]

model = "gpt-3.5-turbo"
response = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=50)

generated_text = response.choices[0].message.content.strip()

lines = generated_text.split("\n")
filler_text = []
for line in lines:
    field = line.split(":")[0].strip()
    field = " ".join(field.split(" ")[1:])
    answer = ":".join(line.split(":")[1:])
    filler_text.append({
        "field": field,
        "text": answer
    })




from PIL import Image, ImageDraw, ImageFont
import textwrap

img_file = "memes/distracted_boyfriend/DistractedBoyfriend.png"
img = Image.open(img_file)
draw = ImageDraw.Draw(img)

FONT = "/usr/share/fonts/truetype/tlwg/Loma.ttf"

texts = [
    {
        "field": "New Thing",
        "meta": "The thing that is being covetted",
        "x": 420,
        "y": 1100,
        "x2": 975,
        "y2": 1320,
    },
    {
        "field": "Subject",
        "meta": "The subject that is covetting something",
        "x": 1299,
        "y": 735,
        "x2": 1788,
        "y2": 957,
    },
    {
        "field": "Old Thing",
        "meta": "The thing being cast asside, forgotten, replaced",
        "x": 1872,
        "y": 855,
        "x2": 2268,
        "y2": 1053,
    },
]

filler_text_static = [
    {
        "field": "New Thing",
        "text": "I very much like burgers they are very good and tasty",
        #"text": "Burger",
    },
    {
        "field": "Subject",
        "text": "Me",
    },
    {
        "field": "Old Thing",
        "text": "The diet I told myself I would stick to but you know that's not happening",
        #"text": "Diet",
    },
]

def get_longest_line(lines):
    if len(lines) == 1:
        return lines[0]
    font = ImageFont.truetype(FONT, 12)
    longest = 0
    idx = -1
    for i in range(len(lines)):
        text_width = draw.textlength(lines[i], font=font)
        if text_width > longest:
            idx = i
            longest = text_width
    return lines[idx]

def get_text_width(text, font_size):
    font = ImageFont.truetype(FONT, font_size)
    return draw.textlength(text, font=font)

def get_text_height(text, font_size):
    font = ImageFont.truetype(FONT, font_size)
    return font.getmetrics()[0]

def calculate_lines(text, width, height):
    font_size = 1
    line_length = len(text)
    num_lines = 1
    while True:
        lines = textwrap.TextWrapper(width=line_length, break_long_words=False).wrap(text=text)

        longest_line = get_longest_line(lines)

        if len(lines) > num_lines and (get_text_height(longest_line, font_size) * len(lines)) > height:
            line_length += 1
            break

        while get_text_width(longest_line, font_size + 1) < width:
            font_size += 1

        if line_length == 1:
            break
        line_length -= 1

    lines = textwrap.TextWrapper(width=line_length, break_long_words=False).wrap(text=text)
    return {
        "lines": lines,
        "font_size": font_size,
        "height": get_text_height(lines[0], font_size),
    }

def add_text(meta, text):
    text_color="white"
    border_color="black"
    border_size=2 # XXX Dynamic

    line_data = calculate_lines(text, meta['x2'] - meta['x'], meta['y2'] - meta['y'])
    lines = line_data['lines']
    font_size = line_data['font_size']
    height = line_data['height']
    font = ImageFont.truetype(FONT, font_size)
    for i in range(len(lines)):
        line = lines[i]
        # XXX: Center text
        y = meta['y'] + (i * height)
        x = meta['x']

        draw.text((x-border_size, y-border_size), line, font=font, fill=border_color)
        draw.text((x+border_size, y-border_size), line, font=font, fill=border_color)
        draw.text((x-border_size, y+border_size), line, font=font, fill=border_color)
        draw.text((x+border_size, y+border_size), line, font=font, fill=border_color)
        draw.text((x, y), line, fill=text_color, font=font)

for txt in filler_text:
    for meta in texts:
        if meta['field'] == txt['field']:
            add_text(meta, txt['text'])
            break

img.show()
