from math import ceil

class TweetTextFormatter():
  def chop(text, line_length=30):
    for paragraph in text.split("\n"):
      for line in range(ceil(len(paragraph) / line_length)):
        start = line * 30
        end = start + line_length
        yield paragraph[start:end]

  def getFormattedPrintText(self, tweetText):
    formattedPrintText = self.chop(tweetText)
    return formattedPrintText
