import random

class Pool :

    def __init__(self,parameters):
        self.MAX_STRING = 10
        self.MIN_INT = -1000
        self.MAX_INT = 1000
        self.POOL_SIZE = 1000
        self.parameters = parameters

    def random_string(self):
        length = random.randint(0,self.MAX_STRING)
        rand_str = ''

        for i in range(length):
            rand_str += chr(random.randrange(97,122))

        return rand_str

    def initialize(self,flag):
        if flag == 'str' :
            return self.random_string()
        else :
            return random.randrange(self.MIN_INT,self.MAX_INT)
        

    def pool_init(self,size = 0):

        pool = []
        for i in range(size):
            if len(self.parameters) == 1 :
                pool.append(self.initialize(self.parameters[0]))
            else :
                entry = []
                for j in range(len(self.parameters)):
                    entry.append(self.initialize(self.parameters[j]))
                pool.append(entry)
        return pool

    def mutation_helper(self,entry):
        if type(entry) == str :
            if len(entry) == 0 :
                return entry
            rand_index = random.randrange(0,len(entry))
            entry = entry[:rand_index] + chr(random.randrange(97,122)) + entry[rand_index:]
            return entry
        else :
            return random.randrange(self.MIN_INT,self.MAX_INT)

    def mutation(self,value_list):
        n = len(value_list)
        for i in range(n) :

            if type(value_list[i]) == list :
                choice = random.randrange(0,len(value_list[i]))
                value_list[i][choice] = self.mutation_helper(value_list[i][choice])
            else :
                value_list[i] = self.mutation_helper(value_list[i])
        return value_list

    def crossover(self,list1,list2):
        if type(list1[0]) == int :
            list1[-1] = list2[-1]
        
        elif type(list1[0]) == str : 
            index1 = random.randrange(0,len(list1))
            index2 = random.randrange(0,len(list2))
            if list1[index1] != '' and list2[index2] != '' :
                list1[index1] = list1[index1][0] + list2[index2][1:]

        else :
            if type(list1[0][0]) == str :
                choice1 = random.randrange(0,len(list1))
                choice2 = random.randrange(0,len(list2))
                if list1[choice1][0] != '' and list2[choice2][0] != '' :
                    list1[choice1][0] = list1[choice1][0][0] + list2[choice2][0][1:]    
            else :
                list1[-1] = list2[-1]      
        return list1

    def fuzzer_test_gen(self,size) :
        #print('Initializing the Pool')
        pool = self.pool_init(self.POOL_SIZE)
        #print('Adding entries to the pool(Random/Mutation/Crossover)')
        for i in range(size):
            prob = random.randint(0,2)

            if prob == 0 :
                pool.append(self.pool_init(1)[0])

            elif prob == 1 :
                pool = self.mutation(pool)
        
            else :
                new_pool = self.pool_init(self.POOL_SIZE)
                pool = self.crossover(pool,new_pool)

        return pool