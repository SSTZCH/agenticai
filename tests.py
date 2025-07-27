# from subdirectory.filename import function_name
from functions.run_python_file import *

import os

res1 = run_python_file("calculator", "main.py")
print(f"1: {res1}")

res2 = run_python_file("calculator", "main.py", ["3 + 5"])
print(f"2: {res2}")

res3 = run_python_file("calculator", "tests.py")
print(f"3: {res3}")

res4 = run_python_file("calculator", "../main.py")
print(f"4: {res4}")

res5 = run_python_file("calculator", "nonexistent.py")
print(f"5: {res5}")
