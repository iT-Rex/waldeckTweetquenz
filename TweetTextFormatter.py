class TweetTextFormatter():
  def chopUpIntoThirtyCharacterLines(self, tweetText):
    characterCountLeftToParse = len(tweetText)
    desiredLineLength = 30
    nextLineEnd = desiredLineLength
    nextLineStart = 0
    choppedUpLines = list()
    
    while characterCountLeftToParse > desiredLineLength:
      choppedUpLines.append(tweetText[nextLineStart:nextLineEnd])
      characterCountLeftToParse = characterCountLeftToParse - desiredLineLength
      nextLineStart = nextLineEnd
      nextLineEnd = nextLineStart + desiredLineLength

    choppedUpLines.append(tweetText[nextLineStart:nextLineStart + characterCountLeftToParse])

    return choppedUpLines

  def getFormattedPrintText(self, tweetText):
    formattedPrintText = self.chopUpIntoThirtyCharacterLines(tweetText)
    return formattedPrintText
