import os

class PrintCommandSender():
  def sendPrintLineToConsole(self, line):
    with open("/dev/lp0", "w") as printer:
      printer.write("\x1bW1\x1bx1")
      printer.write(line)
      printer.write("\r")
      printer.write(line)
      printer.write("\r")
      printer.write(line)