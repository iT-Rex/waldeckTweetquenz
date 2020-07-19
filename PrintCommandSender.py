import os

class PrintCommandSender():
  def setPrinterCharacterMode():
    with open("/dev/lp0", "w") as printer:
      printer.write("\x1bW1\x1bx1")

  def sendPrintLineToConsole(self, line):
    with open("/dev/lp0", "w") as printer:
      printer.write(line + chr(13) + line + chr(10))
