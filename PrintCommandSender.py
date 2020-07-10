import os

class PrintCommandSender():
  def sendPrintLineToConsole(self, line):
    printLineCommand = "echo -e '\x1bW1\x1bx1'" + line + "\r > /dev/lp0"
    os.system(printLineCommand)
