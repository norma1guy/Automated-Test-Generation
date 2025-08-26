from deap import base,creator,tools,algorithms
from metadata import TestCases
from pool import Pool
import os
from test_gen_random import Functions,test_class_gen
import ast
import random
import instrumentor

INT_MAX = 1000
INT_MIN = -1000
MAX_STRING = 10
POOL_SIZE = 100

def normalize(distance):

    return distance/(distance + 1)

def random_index(list1) :
    index1 = random.randrange(len(list1))
    return [index1,list1[index1]]

def mutate_helper(entry):
    if type(entry) == str :
        if len(entry) == 0 :
            return entry
        rand_index = random.randrange(0,len(entry))
        return entry[:rand_index] + chr(random.randrange(97,122)) + entry[rand_index:]
    elif type(entry) == int :
        return random.randrange(INT_MIN,INT_MAX)
    
    else :
        index = random.randint(0,1)
        entry[index] = mutate_helper(entry[index])

    
def mutate(individual):
    if isinstance(individual[0], list):  # nested (pair) case
        choice = random.randrange(len(individual[0]))
        individual[0][choice] = mutate_helper(individual[0][choice])
    else:
        choice = random.randrange(len(individual))
        individual[choice] = mutate_helper(individual[choice])
    
    return (individual,) 





def crossover(ind1, ind2):
    if len(ind1) <= 1 or len(ind2) <= 1:
        return ind1, ind2
    if isinstance(ind1[0], list): 
        ind1[0], ind2[0] = ind2[0], ind1[0]
    else:
        cxpoint = random.randint(1, len(ind1)-1)
        ind1[cxpoint:], ind2[cxpoint:] = ind2[cxpoint:], ind1[cxpoint:]
    
    return ind1, ind2 


def random_string():
    length = random.randint(0,MAX_STRING)
    rand_str = ''

    for i in range(length):
        rand_str += chr(random.randrange(97,122))

    return rand_str

def random_pair():

    return [random_string(),random.randint(INT_MIN,INT_MAX)]


def deap_fitness(individual) :
    dist_map = instrumentor.distance_map
    fitness = 0
    for branch, tuples in dist_map.items():
        if branch not in testcases.current_cov: 
            for true_dist, false_dist in tuples:
                # normalize and sum
                fitness += true_dist / (1 + true_dist)
    
    return (fitness,)



def deap_test_exec(path,iter):

    creator.create('FitnessNew',base.Fitness,weights = (-1.0,))
    creator.create('IntIndividual',list,fitness = creator.FitnessNew)
    creator.create('StrIndividual',list,fitness = creator.FitnessNew)
    creator.create('PairIndividual',list,fitness = creator.FitnessNew)

    toolbox = base.Toolbox()
    toolbox.register('attr_int',random.randint,INT_MIN,INT_MAX)
    toolbox.register('attr_str',random_string)
    toolbox.register('attr_pair',random_pair)

    toolbox.register('int_indv_1',tools.initRepeat,creator.IntIndividual,toolbox.attr_int, n = 1)
    toolbox.register('int_indv_2',tools.initRepeat,creator.IntIndividual,toolbox.attr_int, n = 2)
    toolbox.register('int_indv_3',tools.initRepeat,creator.IntIndividual,toolbox.attr_int, n = 3)
    toolbox.register('int_population_1',tools.initRepeat,list,toolbox.int_indv_1)
    toolbox.register('int_population_2',tools.initRepeat,list,toolbox.int_indv_2)
    toolbox.register('int_population_3',tools.initRepeat,list,toolbox.int_indv_3)

    toolbox.register('str_indv_1',tools.initRepeat,creator.StrIndividual,toolbox.attr_str, n = 1)
    toolbox.register('str_indv_2',tools.initRepeat,creator.StrIndividual,toolbox.attr_str, n = 2)
    toolbox.register('str_indv_3',tools.initRepeat,creator.StrIndividual,toolbox.attr_str, n = 3)
    toolbox.register('str_population_1',tools.initRepeat,list,toolbox.str_indv_1)
    toolbox.register('str_population_2',tools.initRepeat,list,toolbox.str_indv_2)
    toolbox.register('str_population_3',tools.initRepeat,list,toolbox.str_indv_3)

    toolbox.register('pair_indv',tools.initRepeat,creator.PairIndividual,toolbox.attr_pair,n = 1)
    toolbox.register('pair_population',tools.initRepeat,list,toolbox.pair_indv)

    toolbox.register('mate',crossover)
    toolbox.register('mutate',mutate)
    toolbox.register('evaluate',deap_fitness)
    toolbox.register("select", tools.selTournament, tournsize=3)

    for file in os.listdir(path) :
        full_path = os.path.join(path,file)
        source_code = open(full_path).read()
        exec(source_code,globals())
        visitor = Functions()
        visitor.visit(ast.parse(source_code))
        total_testcases = []
        total_funcs = []
        total_testcases  = []
        #branches = visitor.branches
        for func,parameters in visitor.funcs.items() :
            total_funcs.append(func)
            testcases = TestCases(func)
            iterations = 0
            pool = None
            skips = 0
            total = 0
            if len(parameters) == 1 :
                if parameters[0] == 'str' :
                    pool = toolbox.str_population_1(POOL_SIZE)
                else :
                    pool = toolbox.int_population_1(POOL_SIZE)

            elif len(parameters) == 2 :
                if parameters[0] == 'int' :
                    pool = toolbox.int_population_2(POOL_SIZE)
                elif parameters[0] == 'str':
                    if parameters[1] == 'str':
                        pool = toolbox.str_population_2(POOL_SIZE)
                    else :
                        pool = toolbox.pair_population(POOL_SIZE)
            else :
                if parameters[0] == 'int' :
                    pool = toolbox.int_population_3(POOL_SIZE)
                else :
                    pool = toolbox.str_population_3(POOL_SIZE)
            print(f'Function {func}')
            print(f'Parameters {parameters}')
            #print(pool[0])
            
            while len(testcases.current_cov) < visitor.branches[func] and iterations < 100 :
                iterations += 1
                output = {}
                for entry in pool :
                    #print(*entry)
                    try : 
                        input = ''
                        for i in range(len(entry)) :
                            input = input + str(entry[i]) + ', ' if i <= len(entry) - 2 else input + str(entry[i])
                        if parameters == ['str','int'] :
                            output = globals()[func](*entry[0])
                        else :
                            output = globals()[func](*entry)
                        if type(output) == str :
                            output.replace('\\','\\\\').replace('"','\\"').replace("'","\\'")
                        #print(output)
                        dist_map = instrumentor.distance_map
                        instrumentor.distance_map = {}
                        if parameters == ['str','int'] :
                            testcases.updater(dist_map,entry[0],output)
                        else :
                            testcases.updater(dist_map,entry,output)
                    except Exception as e :
                        skips += 1
                        #print(e)
                hof = tools.HallOfFame(1)

                algorithms.eaSimple(
                    pool,
                    toolbox,
                    cxpb=0.5,  
                    mutpb=0.5,  
                    ngen=40,    
                    halloffame=hof,
                    verbose=False
                )
                total += len(pool)
                #print(testcases.current_cov)

            total_testcases.append(testcases)
        test_code_tree = test_class_gen(file.replace('_instrumented.py',''),total_funcs,total_testcases)
        test_file = file.replace('instrumented','test')
        os.makedirs(f'test/GA_{iter}',exist_ok = True)

        with open(f'test/GA_{iter}/{test_file}','w') as file :
            file.write(ast.unparse(test_code_tree))

    with open(f'test/GA_{iter}/__init__.py','w') as file :
        file.write('')
        
        #print(f'Skipped {skips} out of {total}')
    
    

