# Automated Test Generation

## About the Project

This project has the goal of writing a search based automated test generator for Python.


In this repository, you can find the following files:
- benchmark folder: which contains the benchmark of functions under test to be instrumented

---

### Instrumentation 
---
> **Transform code for extracting relevant information.**

With the help of [Instrumentor](/instrumentor.py) class which is a subclass of **ast.NodeTransformer**,the code is instrumented for capturing branch information for conditional blocks.

A global map called **distances_map** is mainted to store the information regarding true and false distance of branches.

### Fuzzer Test Generator
---
[Function](/test_gen_random.py) class is used to get information regarding parameter types of each function definition in instrumented code.

--- 
The instrumented code is executed and the information is stored. Then using [Pool](/pool.py) a pool of test cases are generated according to the parameter type of function, mutation or crossover with equal probability.

New test cases are generated till each branch is covered or 100 iterations of generation have been reached.

### Test File Generation
---
Making use of all the information gathered so far test files are generated with test cases covering maximum branches possible.

### Genetic Algorithm Test Generator
---
> **Genetic algorithms defined with the help of **deap** module.**

A fitness function is defined by normalizing branch distance for branches not covered.

Again making use of crossover and mutate a pool of test cases is generated.

### Statistical Comparision
---
 With the help of **mut.py** faults are injected into benchmarks which helps evaluate whether our test cases catch the faults or not.





### Execution
---
First step is to produce the instrumented files by running the instrumentor.py script.
```
python instrumentor.py
```


### Comparison
---
Running the comparison.py script makes use of test_gen_deap and test_gen_random scripts to produces tests using fuzzer and GA then runs mut.py on them to produce mutants and calculate the mutation score.

```
python comparison.py
```


 
