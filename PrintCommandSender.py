import os

class PrintCommandSender():
  def sendPrintLineToConsole(self, line):
    with open("/dev/lp0", "w") as printer:
      printer.write(line + chr(13) + line + chr(10))
