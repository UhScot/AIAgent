from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

result = run_python_file("calculator", "main.py")
print(result)

result = run_python_file("calculator", "main.py", ["3 + 5"])
print(result)

result = run_python_file("calculator", "tests.py")
print(result)

try:
    result = run_python_file("calculator", "../main.py")
    print(result)
except Exception as e:
    print(f"Error: {e}")

try:
    result = run_python_file("calculator", "nonexistent.py")
    print(result)
except Exception as e:
    print(f"Error: {e}")