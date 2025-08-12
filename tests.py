from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


def main():
    test_get_files_info()
    # test_get_file_content()
    # test_write_file()
    # test_execute_python()


def test_get_files_info():
    print("Result for current directory:")
    results = get_files_info("calculator", ".")
    print(results)

    print("Result for 'pkg' directory:")
    results = get_files_info("calculator", "pkg")
    print(results)

    print("Result for '/bin' directory:")
    results = get_files_info("calculator", "/bin")
    print(results)

    print("Result for '../' directory:")
    results = get_files_info("calculator", "../")
    print(results)

def test_get_file_content():
    print("Result for 'lorem.txt':")
    results = get_file_content('calculator', 'lorem.txt')
    print(results)

    print("Result for 'main.py':")
    results = get_file_content('calculator', 'main.py')
    print(results)

    print("Result for 'pkg/calculator.py':")
    results = get_file_content("calculator", "pkg/calculator.py")
    print(results)

    print("Result for '/bin/cat':")
    results = get_file_content("calculator", "/bin/cat")
    print(results)

    print("Result for 'pkg/does_not_exist.py':")
    results = get_file_content("calculator", "pkg/does_not_exist.py")
    print(results)

def test_write_file():
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result)

    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result)

    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result)

def test_execute_python():
    result = run_python_file("calculator", "main.py")
    print(result)

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)

    result = run_python_file("calculator", "../main.py")
    print(result)

    result = run_python_file("calculator", "nonexistent.py")
    print(result)


if __name__ == "__main__":
    main()
