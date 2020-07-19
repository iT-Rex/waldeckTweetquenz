from textwrap import wrap

class TweetTextFormatter():
  def chop(text, line_length=30):
    for paragraph in text.split("\n"):
      yield from wrap(paragraph, width=line_length)

  def getFormattedPrintText(self, tweetText):
    formattedPrintText = self.chop(tweetText)
    return formattedPrintText
