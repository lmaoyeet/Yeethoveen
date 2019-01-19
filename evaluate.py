class Lexer:

    def __init__(self, data):
        self.data     = data
        self.tokens   = []
        self.keywords = [
            'print',
            'goto',
            'fin'
        ]

    def tokenizer(self):
        for loc in self.data:
            tmp  = []
            tid  = ''

            for l in loc:
                if l == '"' and tid == '':
                    tid = 'char'
                    tmp = []
                elif l == '"' and tid == 'char':
                    self.tokens.append({'id': tid, 'value': ''.join(tmp)})
                    tid = ''
                    tmp = []
                elif l == ':':
                    self.tokens.append({'id': 'label', 'value': ''.join(tmp)})
                    tmp = []
                elif ''.join(tmp) in self.keywords:
                    self.tokens.append({'id': 'keyword', 'value': ''.join(tmp)})
                    tmp = []
                elif l == "\n":
                    if len(tmp) > 0:
                        self.tokens.append({'id': 'atom', 'value': ''.join(tmp)})
                        tmp = []
                elif l == ' ' and tid != 'char':
                    continue
                else:
                    tmp.append(l)
class Evaluator:

    def __init__(self, AST):
        self.AST = AST
        pass

    def run(self, node):
        if isinstance(node, list):
            for n in node:
                for k, v in n.items():
                    self.execute([k, v])
        elif isinstance(node, dict):
            for k, v in node.items():
                self.execute([k, v])

    def execute(self, loc):
        if isinstance(loc[1], list):
            self.run(loc[1])
        elif loc[0] == 'print':
            self.echo(loc[1])
        elif loc[0] == 'goto':
            self.goto(loc[1])
        elif loc[0] == 'fin':
            self.stop()

    def echo(self, v):
        print(v)

    def goto(self, v):
        for node in self.AST:
            try:
                self.run(node[v])
            except KeyError:
                pass

    def stop(self):
        quit()
#mien
class Parse:

    def __init__(self, tokens):
        self.tokens = tokens
        self.AST    = []

    def add_node(self, parent, node):
        for a in self.AST:
            if parent in a:
                a[parent].append(node)

    def build_AST(self):
        saved   = {}
        parent  = {}
        collect = False

        for token in self.tokens:
            if token['id'] == 'label':
                t = {token['value']: []}

                if parent != t:
                    parent = token['value']
                    self.AST.append(t)

            elif token['id'] == 'keyword':
                if token['value'] == 'fin':
                    t = {token['value']: 0}
                    self.add_node(parent, t)
                else:
                    if collect == False:
                        saved   = token
                        collect = True
                    else:
                        t = {saved['value']: token['value']}
                        self.add_node(parent, t)
                        collect = False

            elif token['id'] == 'char' or token['id'] == 'atom':
                    if collect == False:
                        saved   = token
                        collect = True
                    else:
                        t = {saved['value']: token['value']}
                        self.add_node(parent, t)
                        collect = False
