import ast
from pool import Pool
import os
import instrumentor
from pprint import pprint
from metadata import TestCases,File

class Functions(ast.NodeVisitor):

    def __init__(self):
        self.funcs = {}
        self.branches = {}
        self.conds = 0

    def visit_FunctionDef(self,node):
        args = []
        for arg in node.args.args :
            args.append(arg.annotation.id)
        self.funcs[node.name] = args
        self.generic_visit(node)
        self.branches[node.name] = self.conds
        self.conds = 0
    
    def visit_If(self,node):
        self.conds += 1
        self.generic_visit(node)


def test_class_gen(func_name, funcs, testcases):
    
    test_imp = ast.ImportFrom(module='unittest', names=[ast.alias(name='TestCase')], level=0)
    func_imp = ast.ImportFrom(module=f'benchmark.{func_name}', names=[ast.alias(name='*')], level=0)

    test_class = ast.ClassDef(
        name='Test_example',
        bases=[ast.Name(id='TestCase', ctx=ast.Load())],
        keywords=[],
        body=[],
        decorator_list=[]
    )

    body = [test_imp, func_imp, test_class]
    for i in range(len(funcs)):
        func_name = funcs[i].replace('_instrumented', '')
        counter = 1
        cases = testcases[i]
        for entry in cases.testcases:
            test_input = entry.input
            expected_output = entry.output

            if isinstance(test_input, list):
                arg_nodes = [ast.Constant(value=val) for val in test_input]
            else:
                arg_nodes = [ast.Constant(value=test_input)]

            func_def = ast.FunctionDef(
                name=f'test_{func_name}_{counter}',
                args=ast.arguments(
                    posonlyargs=[],
                    args=[ast.arg(arg='self', annotation=None)],
                    vararg=None,
                    kwonlyargs=[],
                    kw_defaults=[],
                    kwarg=None,
                    defaults=[]
                ),
                body=[],
                decorator_list=[]
            )

            func_call = ast.Call(
                func=ast.Name(id=func_name, ctx=ast.Load()),
                args=arg_nodes,
                keywords=[]
            )

            assign_node = ast.Assign(
                targets=[ast.Name(id='y', ctx=ast.Store())],
                value=func_call
            )

            assert_node = ast.Assert(
                test=ast.Compare(
                    left=ast.Name(id='y', ctx=ast.Load()),
                    ops=[ast.Eq()],
                    comparators=[ast.Constant(value=expected_output)]
                ),
                msg=None
            )

            func_def.body = [assign_node, assert_node]
            test_class.body.append(func_def)
            counter += 1



    module = ast.Module(body=body, type_ignores=[])
    ast.fix_missing_locations(module)
    return module




    

def fuzzer_test_exec(path,iter):
    
    for file in os.listdir(path):
        full_path = os.path.join(path,file)
        source_code = open(full_path).read()
        exec(source_code,globals())
        visitor = Functions()
        visitor.visit(ast.parse(source_code))
        total_testcases  = []
        total_funcs = []
        for func,parameters in visitor.funcs.items():
            total_funcs.append(func)
            print(f'Parameters for this function {func} are {parameters}')
            testcases = TestCases(func)
            test_gen = Pool(parameters)
            iterations = 0
            skips = 0
            total = 0
            while len(testcases.current_cov) < visitor.branches[func] and iterations < 100 :
                iterations += 1
                pool = test_gen.fuzzer_test_gen(10)
                total += len(pool)
                #print(pool)
                output = None
                for entry in pool :
                    try :
                        if type(entry) == list :
                            input = ''
                            for i in range(len(entry)) :
                                input = input + str(entry[i]) + ', ' if i <= len(entry) - 2 else input + str(entry[i]) 
                            output = globals()[func](*entry)
                            #print(output)
                            if type(output) == str :
                                #print(output)
                                output.replace('\\','\\\\').replace('"','\\"').replace("'","\\'")
                        else :
                            output = globals()[func](entry)
                            if type(output) == str :
                                output.replace('\\','\\\\').replace('"','\\"').replace("'","\\'")
                        cov_map = instrumentor.distance_map
                        instrumentor.distance_map = {}
                        testcases.updater(cov_map,entry,output)
            
                    except Exception as e :
                        skips += 1

            print(f'Skipped {skips} test cases out of {total} test cases in {iterations} iterations')
            total_testcases.append(testcases)
        
        test_code_tree = test_class_gen(file.replace('_instrumented.py',''),total_funcs,total_testcases)
        test_file = file.replace('instrumented','test')
        os.makedirs(f'test/fuzzer_{iter}',exist_ok = True)

        with open(f'test/fuzzer_{iter}/{test_file}','w') as file :
            file.write(ast.unparse(test_code_tree))
    
    with open(f'test/fuzzer_{iter}/__init__.py','w') as file :
        file.write('')    
        

            







