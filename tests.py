from functions.get_files_info import get_files_info


def main():
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

if __name__ == "__main__":
    main()
