# Based on https://github.com/AllAlgorithms, python/algorithms/math/check_armstrong.py

def check_armstrong(n: int) -> bool:
	assert n >= 0
	if n == 0 or n == 1:
		return True
	if n <= 150:
		return False
	t = n
	sum = 0
	while t != 0:
		r = t % 10
		sum = sum + (r * r * r)
		t = t // 10
	if sum == n:
		return True
	else:
		return False
