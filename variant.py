from itertools import product

student_id = 19
print(list(product(
    ('python 3.8.*', 'python 3.7.*', 'python 3.6.*'),
    ('venv + requirements.txt', 'virtualenv + requirements.txt', 'poetry', 'pipenv')
))[(student_id - 1) % 12])
