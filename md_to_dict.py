import re
import sys
from lark import Lark, Transformer, v_args
from lark.exceptions import *
from collections import ChainMap

class TreeToJson(Transformer):
    @v_args(inline=True)
    def key(self, s):
        """
        Replace spaces with underscore and strip leading
        and trailing whitespaces
        """
        return re.sub(r"\s+", '_', s.lower().lstrip(' ').rstrip(' '))

    @v_args(inline=True)
    def string(self, s):
        """
        Strip leading and trailing whitespaces
        Parse float, bool, null
        """
        val = s.lstrip(' ').rstrip(' ')
        try:
            val = float(s)
            return val
        except Exception:
            pass
        values = {"null": None, "true": True, "false": False}
        if val in values:
            return values[val]
        return val

    def header(self, s):
        return s[0]

    def pair(self, s):
        # Convert to dictionary
        return {s[0] : s[1]}

    def invalid(self, s):
        return None

    def header_pair(self, s):
        # Assign pair dictionaries to header
        return {s[0]: dict(ChainMap(*[x for x in s[1:] if x]))}

    def invalid_header_pair(self, s):
        return None

    def dictionary(self, s):
        # Merge everything into a single dictionary
        s = [x for x in s if x]
        return dict(ChainMap(*s))

class MarkdownParser():
    """
        Parse markdown into python dictionary
        Example:
            from md_to_dict import MarkdownParser
            md_parser = MarkdownParser(path_to_file)
            md_dict = md_parser.parse()
        TODO:
            1. Retain integer/float/array data type when parsing numbers/array
    """
    def __init__(self, filename='', input_md=''):
        self.markdown_grammar = r"""
                ?start: dictionary
                dictionary: (header_pair | invalid_header_pair)*
                invalid_header_pair: invalid_header (pair+ | invalid)*
                header_pair: header (pair+ | invalid)*
                header: "#" key
                invalid_header: /\#{2,}/ string
                pair : "*" key ":" value
                invalid: string
                ?value: string
                string: /[a-z0-9A-Z.'\-\!\?\,\/ ]+/
                key: /[a-z0-9A-Z.'\-\!\?\,\/ ]+/

                %import common.WS
                %import common.SIGNED_NUMBER
                %ignore WS
            """
        self.filename = filename
        self.input_md = input_md
        self.parser = Lark(self.markdown_grammar, parser='lalr', lexer='standard', transformer=TreeToJson())

        if self.filename:
            with open(filename) as f:
                self.input_md = f.read()

    def parse(self):
        try:
            output = self.parser.parse(self.input_md)
            return output
        except (ParseError, UnexpectedInput, UnexpectedToken) as e:
            print('Markdown provided cannot be parsed into a dictionary. Please use proper formatting.', e)
        except Exception as e:
            print('Exception occured: ', e)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Invalid Usage')
        print('Correct Usage: python md_to_dict.py <path_to_markdown_file>')
    else:
        md_parser = MarkdownParser(sys.argv[1])
        print(md_parser.parse())
