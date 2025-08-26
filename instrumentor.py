import ast
import os
from nltk.metrics import edit_distance

true_distance_map = {}
false_distance_map = {}
distance_map  = {}

def matcher(op,lhs,rhs,flag = 0) :
    true_dist = 0
    false_dist = 0
    if not flag :
        match op :
            case 'Lt' :
                true_dist = lhs - rhs + 1 if lhs >= rhs else 0
                false_dist = rhs - lhs if rhs > lhs else 0
            
            case 'Gt':
                true_dist = rhs - lhs + 1 if rhs >= lhs else 0
                false_dist = lhs - rhs if lhs > rhs else 0

            case 'LtE' :
                true_dist = lhs - rhs if lhs > rhs else 0
                false_dist = rhs - lhs + 1 if rhs >= lhs else 0
            
            case 'GtE' :
                true_dist = rhs - lhs if rhs > lhs else 0
                false_dist = lhs - rhs + 1 if lhs >= rhs else 0

            case 'Eq' :
                true_dist = abs(lhs - rhs)
                false_dist = 1 if lhs == rhs else 0
            
            case 'NotEq' :
                true_dist = 1 if lhs == rhs else 0
                false_dist = abs(lhs - rhs)
    else :
        match op :
            case 'Eq' :
                true_dist = edit_distance(lhs,rhs)
                false_dist = 1 if lhs == rhs else 0
            
            case 'NotEq' :
                true_dist = 1 if lhs == rhs else 0
                false_dist = edit_distance(lhs,rhs)

    return [true_dist,false_dist]


def evaluate_condition(num,op,lhs,rhs):
    true_dist = 0
    false_dist = 0
    
    if isinstance(lhs,str) and isinstance(rhs,str) :
        if len(lhs) == 1 and len(rhs) == 1:
            lhs = ord(lhs)
            rhs = ord(rhs)
            true_dist,false_dist = matcher(op,lhs,rhs)
        else :
            true_dist,false_dist = matcher(op,lhs,rhs,1)
    
    else :
        true_dist,false_dist = matcher(op,lhs,rhs)

    '''if true_dist :
        if num in false_distance_map.keys() :
            false_distance_map[num] = min(false_dist,false_distance_map[num])
        else :
            false_distance_map[num] = false_dist
    
    else :
        if num in true_distance_map.keys() :
            true_distance_map[num] = min(true_distance_map[num],true_dist)
        else :
            true_distance_map[num] = true_dist'''
    
    if num in distance_map.keys() :
        distance_map[num].append((true_dist,false_dist))
    else :
        distance_map[num] = [(true_dist,false_dist)]

    return True if true_dist == 0 else False

operator_map = {ast.Gt : 'Gt',
                ast.Lt : 'Lt',
                ast.Eq : 'Eq',
                ast.GtE:'GtE',
                ast.LtE : 'LtE',
                ast.NotEq : 'NotEq',
                }

class Instrumentor(ast.NodeTransformer):

    def __init__(self):
        self.num = 0
        self.branches = 0
        self.funcs = []
        self.return_scope = False
        self.scope = None
        

    def visit_If(self,node):
        if self.return_scope :
            return node
        self.num += 1
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        self.funcs.append(node.name)
        node.name = node.name + '_instrumented'
        self.generic_visit(node)
        self.branches += self.num
        self.num = 0
        return node
    
    def visit_Assert(self,node):

        return node

    def visit_Return(self,node) :

        self.return_scope = True
        self.generic_visit(node)
        self.return_scope = False
        return node    
    
    def visit_Call(self,node):
        
        if isinstance(node.func,ast.Name) and node.func.id in self.funcs :
            node.func.id = node.func.id + '_instrumented'
        return node
     
    def visit_Compare(self,node):

        if isinstance(self.scope,ast.While):
            return node

        if node.ops[0] in [ast.In,ast.NotIn,ast.Is,ast.IsNot] :
            return node
        
        new_call = ast.Call(
        func=ast.Name(id='evaluate_condition', ctx=ast.Load()),
        args=[
            ast.Constant(value=self.num),
            ast.Constant(value=operator_map[type(node.ops[0])]),
            node.left,
            node.comparators[0]
        ],
        keywords=[]
        )
        return new_call
    
    def visit_While(self, node) :
        self.scope = node
        self.generic_visit(node)
        self.scope = None
        return node

    


def gen_instr():
    
    os.makedirs("instrumented", exist_ok=True)
    file_count = 0
    func_count = 0
    branch_count = 0
    for file in os.listdir('benchmark'):
        file_name,ext = os.path.splitext(file)
        print(f'Intrumenting file {file}')
        source_code = open(os.path.join('benchmark',file)).read()
        tree = ast.parse(source_code)
        instr = Instrumentor()
        instr.visit(tree)
        func_count += len(instr.funcs)
        branch_count += instr.branch
        #tree.body.insert(0,ast.Assign(targets = [ast.Name(id = 'distance_map',ctx = ast.Store())],value = ast.Dict(keys=[],values=[])))
        tree.body.insert(0,ast.ImportFrom(module = 'instrumentor',names = [ast.alias(name='evaluate_condition')]))
        ast.fix_missing_locations(tree)
        
        new_file = os.path.join('instrumented',f'{file_name}_instrumented{ext}')
        with open(new_file,'w') as f:
            f.write(ast.unparse(tree))
        file_count += 1
    
    print(f'Total files instrumented = {file_count}')
    print(f'Total number of functions found = {func_count}')
    print(f'Total number of branches encountered = {branch_count}')
        





if __name__ == '__main__':

    gen_instr()

