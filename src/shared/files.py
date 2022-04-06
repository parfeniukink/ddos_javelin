def get_file_lines(filename: str) -> list:
    with open(filename) as file:
        return file.readlines()
