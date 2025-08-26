from pool import Pool
from pprint import pprint

pool = Pool(['str','str'])

pprint(pool.pool_init(100))