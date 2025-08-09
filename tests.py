from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content


def main():
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

if __name__ == "__main__":
    main()
