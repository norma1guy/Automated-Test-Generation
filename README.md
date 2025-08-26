# Project 02 - Python test generator

### About the Project

This project has the goal of writing a search based automated test generator for Python.
It is part of the Knowledge Search & Extraction - 2023 course from the Università della Svizzera italiana.

In this repository, you can find the following files:
- benchmark folder: which contains the benchmark of functions under test to be instrumented

Note: Feel free to modify this file according to the project's necessities.


### Execution

First step is to produce the instrumented files by running the instrumentor.py script.
```
python instrumentor.py
```


### Comparison

Running the comparison.py script makes use of test_gen_deap and test_gen_random scripts to produces tests using fuzzer and GA then runs mut.py on them to produce mutants and calculate the mutation score.

```
python comparison.py
```


 
