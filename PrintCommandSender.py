import os

class PrintCommandSender():
  def sendPrintLineToConsole(self, line):
    printLineCommand = 'printf "\x1bW1\x1bx1' + line + '\r"> /dev/lp0'
    os.system(printLineCommand)
