from textwrap import wrap

def chop(text, line_length=30):
  for paragraph in text.split("\n"):
    yield from wrap(paragraph, width=line_length)
