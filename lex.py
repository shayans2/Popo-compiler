from constants import TokenType
import sys


class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText
        self.kind = tokenKind

    @staticmethod
    def isKeyWord(tokenText):
        for kind in TokenType:
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None


class Lexer:
    def __init__(self, input):
        self.source = input + '\n'
        self.curChar = ''
        self.curPos = -1

        # Initialize first char
        self.nextChar()

    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'  # End Of Line (EOF)
        else:
            self.curChar = self.source[self.curPos]

    # Get the lookahead character.
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos+1]

    def abort(self, message):
        sys.exit("(Lexical error) " + message)

    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    def skipComment(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None

        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)

        elif self.curChar == '\"':
            # Check for strings in between double quotes " "
            # Todo check for special chars
            val = ""
            self.nextChar()
            while self.curChar != '\"':
                val += self.curChar
                self.nextChar()
            token = Token(val, TokenType.STRING)

        elif self.curChar.isdigit():
            # Check for numbers
            # Todo check for special chars or decimals
            val = ""
            while self.peek().isdigit():
                val += self.curChar
                self.nextChar()
            val += self.curChar
            token = Token(val, TokenType.NUMBER)

        elif self.curChar.isalpha():
            # Check for Keywords or Identifiers
            val = ""
            while self.peek().isalnum():
                val += self.curChar
                self.nextChar()
            val += self.curChar

            # Check if the token is in the list of keywords.
            keyword = Token.isKeyWord(val)
            if keyword == None:
                # Identifier
                token = Token(val, TokenType.IDENT)
            else:
                # Keyword
                token = Token(val, keyword)

        elif self.curChar == '=':
            # Check if this token is = or ==
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == '>':
            # Check if this token is > or >=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == '<':
            # Check if this token is < or <=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == '\0':
            token = Token('', TokenType.EOF)
        else:
            self.abort("Unknown token: " + self.curChar)

        self.nextChar()
        return token
