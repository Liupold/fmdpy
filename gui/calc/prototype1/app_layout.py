import app_functions as afn


def input_layout(self):

    # row 1
    self.add_input_button('mod', (0, 0), (1, 1))
    self.add_input_button('MC', (0, 6), (1, 1))
    self.add_input_button('MR', (0, 7), (1, 1))
    self.add_input_button('MS', (0, 8), (1, 1))
    self.add_input_button('M+', (0, 9), (1, 1))
    self.add_input_button('M-', (0, 10), (1, 1))

    # row 2
    self.add_input_button('sinh', (1, 0), (1, 1))
    self.add_input_button('cosh', (1, 1), (1, 1))
    self.add_input_button('tanh', (1, 2), (1, 1))
    self.add_input_button('Exp', (1, 3), (1, 1))
    self.add_input_button('(', (1, 4), (1, 1))
    self.add_input_button(')', (1, 5), (1, 1))
    self.add_input_button("&#x25c0;", (1, 6), (1, 2), afn.backspace(self))
    self.add_input_button('C', (1, 8), (1, 1), afn.cls(self))
    self.add_input_button('+/-', (1, 9), (1, 1), afn.negate(self))
    self.add_input_button('&#8730;', (1, 10), (1, 1))

    #row 3
    self.add_input_button('sinh<sup>-1</sup>', (2, 0), (1, 1))
    self.add_input_button('cosh<sup>-1</sup>', (2, 1), (1, 1))
    self.add_input_button('tanh<sup>-1</sup>', (2, 2), (1, 1))
    self.add_input_button('log <sub>2</sub> X', (2, 3), (1, 1))
    self.add_input_button('ln', (2, 4), (1, 1))
    self.add_input_button('log', (2, 5), (1, 1))
    self.add_input_button('7', (2, 6), (1, 1), afn.put_char(self, '7'))
    self.add_input_button('8', (2, 7), (1, 1), afn.put_char(self, '8'))
    self.add_input_button('9', (2, 8), (1, 1), afn.put_char(self, '9'))
    self.add_input_button('/', (2, 9), (1, 1))
    self.add_input_button('%', (2, 10), (1, 1))

    # row 4
    self.add_input_button('&pi', (3, 0), (1, 1))
    self.add_input_button('e', (3, 1), (1, 1))
    self.add_input_button('n!', (3, 2), (1, 1))
    self.add_input_button('log<sub>y</sub>X', (3, 3), (1, 1))
    self.add_input_button('e<sup>x</sup>', (3, 4), (1, 1))
    self.add_input_button('10<sup>x</sup>', (3, 5), (1, 1))
    self.add_input_button('4', (3, 6), (1, 1), afn.put_char(self, '4'))
    self.add_input_button('5', (3, 7), (1, 1), afn.put_char(self, '5'))
    self.add_input_button('6', (3, 8), (1, 1), afn.put_char(self, '6'))
    self.add_input_button('*', (3, 9), (1, 1))
    self.add_input_button('1/x', (3, 10), (1, 1))

    # row 5
    self.add_input_button('sin', (4, 0), (1, 1))
    self.add_input_button('cos', (4, 1), (1, 1))
    self.add_input_button('tan', (4, 2), (1, 1))
    self.add_input_button('x<sup>y</sup>', (4, 3), (1, 1))
    self.add_input_button('x<sup>3</sup>', (4, 4), (1, 1))
    self.add_input_button('x<sup>2</sup>', (4, 5), (1, 1))
    self.add_input_button('1', (4, 6), (1, 1), afn.put_char(self, '1'))
    self.add_input_button('2', (4, 7), (1, 1), afn.put_char(self, '2'))
    self.add_input_button('3', (4, 8), (1, 1), afn.put_char(self, '3'))
    self.add_input_button('-', (4, 9), (1, 1))
    self.add_input_button('=', (4, 10), (1, 1))

    # row 6
    self.add_input_button('sin<sup>-1</sup>', (5, 0), (1, 1))
    self.add_input_button('cos<sup>-1</sup>', (5, 1), (1, 1))
    self.add_input_button('tan<sup>-1</sup>', (5, 2), (1, 1))
    self.add_input_button('<span> <sup>y</sup> </span> <span> √x </span>', (5, 3), (1, 1))
    self.add_input_button('<span> <sup>3</sup> </span> <span> √ </span>', (5, 4), (1, 1))
    self.add_input_button('|x|', (5, 5), (1, 1))
    self.add_input_button('0', (5, 6), (1, 2), afn.put_char(self, '0'))
    self.add_input_button('.', (5, 8), (1, 1), afn.put_char(self, '.'))
    self.add_input_button('+', (5, 9), (1, 1), afn.add(self))
    self.add_input_button('=', (5, 10), (1, 1))
