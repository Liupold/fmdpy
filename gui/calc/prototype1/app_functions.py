from functools import partial

def partialify(fn):
    def newfn(self, *args):
        return partial(fn, self, *args)
    return newfn

@partialify
def put_char(self, num):
    if self.line2txt == "0" or self.line2auto:
        self.line2txt = ""
        self.line2auto = 0
    self.line2txt += num
    self.setLine2(self.line2txt)

@partialify
def backspace(self):
    if self.line2txt.replace('-', '').replace('.', '').isdecimal():
        self.line2txt = self.line2txt[:-1]
        self.setLine2(self.line2txt)

@partialify
def cls(self):
    self.line1txt = ""
    self.line2txt = "0"
    self.setLine1("")
    self.setLine2("0")
    self.ans = 0

@partialify
def negate(self):
    if self.line2txt[0] == '-':
        self.line2txt = self.line2txt[1:]
    else:
        self.line2txt = '-' + self.line2txt
    self.setLine2(self.line2txt)

@partialify
def add(self):
    val = float(self.line2txt)
    if self.line1txt == "":
        self.line1txt = f"{self.line2txt} + "
    else:
        self.line1txt = f"{self.ans} + {self.line2txt} + "

    self.setLine1(self.line1txt)
    self.ans += val
    if self.ans.is_integer():
        self.ans = int(self.ans)

    self.line2txt = str(self.ans)
    self.setLine2(self.line2txt)
    self.line2auto = 1
