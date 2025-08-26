import os
import re
from test_gen_deap import deap_test_exec
from test_gen_random import fuzzer_test_exec
from pprint import pprint



def create_tests(path,iter) :
    fuzzer_test_exec(path,iter)
    deap_test_exec(path,iter)
    ga_scores = {}
    fuzzer_scores = {}
    for folder in ['fuzzer','GA']:
        for file in os.listdir('benchmark') :
            if file == '__init__.py':
                continue
            test_file = file.replace('.py','_test.py')
            stream = os.popen(f'mut.py --target benchmark/{file} --unit-test test/{folder}_{iter}/{test_file}')
            output = stream.read()
            print(output)
            mut_score = re.search('Mutation score \[.*\]: (\d+\.\d+)%', output).group(1)
            if folder == 'GA':
                ga_scores[file] = mut_score
            else :
                fuzzer_scores[file] = mut_score

    return ga_scores,fuzzer_scores        


def main() :
    n = 10 
    scores = {}
    for i in range(n) :
        results = create_tests('instrumented',i)
        scores[i] = {f'GA_{i}' :results[0],f'Fuzzer_{i}' : results[1]}
    pprint(scores)
if __name__ == '__main__' :
    main()
