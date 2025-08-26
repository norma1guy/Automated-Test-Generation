from collections import namedtuple,defaultdict

TestCaseEntry = namedtuple('TestCaseEntry', ['input', 'output'])

class TestCases:
    def __init__(self, func):
        self.func_name = func
        self.testcases = []
        self.current_cov = set()
        self._best_false_by_branch = {}
        self._branch_to_index = {}

    def updater(self, cov_data, test, output):
        for branch, distances in cov_data.items():
            for true_dist, false_dist in distances:
                if true_dist == 0:
                    if branch not in self.current_cov:
                        self.current_cov.add(branch)
                        self._best_false_by_branch[branch] = false_dist
                        self._branch_to_index[branch] = len(self.testcases)
                        self.testcases.append(TestCaseEntry(test, output))
                    else:
                        if false_dist < self._best_false_by_branch.get(branch, float('inf')):
                            self._best_false_by_branch[branch] = false_dist
                            idx = self._branch_to_index[branch]
                            self.testcases[idx] = TestCaseEntry(test, output)

    





    