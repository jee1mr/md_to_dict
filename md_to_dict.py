import re
import sys
from lark import Lark, Transformer, v_args
from collections import ChainMap

markdown_grammar = r"""
?start: dictionary
dictionary: (header_pair | invalid_header_pair)*
invalid_header_pair: invalid_header (pair+ | invalid)*
header_pair: header (pair+ | invalid)*
header: "#" string
invalid_header: /\#{2,}/ string
pair : "*" string ":" string
invalid: string
string: /[a-z0-9A-Z. ]+/
key: string
value: string

%import common.WS
%ignore WS
"""

output = {}

class TreeToJson(Transformer):
    # TODO: do not strip spaces from value
    @v_args(inline=True)
    def string(self, s):
        """
        Replace spaces with underscore and strip leading
        and trailing whitespaces
        """
        return re.sub(r"\s+", '_', s.lower().lstrip(' ').rstrip(' '))

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

markdown_parser = Lark(markdown_grammar, parser='lalr', lexer='standard', transformer=TreeToJson())

def test():
    test_markdown = '''
    
    # Vendor
    
    * Vendor name: test vendor
    * Vendor website: www.test.com
    
    # Data
    
    this text is ignored
    
    * Data Description: awesome stuff
    * Asset class: Equity
    
    ## subheading 
    
    '''

    print(markdown_parser.parse(test_markdown))

if __name__ == '__main__':
    # test()
    with open(sys.argv[1]) as f:
        print(markdown_parser.parse(f.read()))
