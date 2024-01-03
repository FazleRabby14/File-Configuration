import io

def convert_to_text(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def compare_text_files(text1, text2, file1, file2):
    lines1 = text1.split('\n')
    lines2 = text2.split('\n')

    mismatch_info = []

    # Compare lines
    for i, (line1, line2) in enumerate(zip(lines1, lines2), start=1):
        if line1 != line2:
            mismatch_info.append(f"Mismatch at line {i} in {file1} and {file2}:\n"
                                 f"    {line1}\n"
                                 f"!=  {line2}\n")

    return mismatch_info

if __name__ == "__main__":
    file1 = "CashInCustom.accfg"
    file2 = "CashInCustom1.accfg"

    text1 = convert_to_text(file1)
    text2 = convert_to_text(file2)

    mismatch_info = compare_text_files(text1, text2, file1, file2)

    # Print mismatch information with proper indentation and line breaks
    for info in mismatch_info:
        print(info)

    # Save mismatch information to a text file
    with open("accfg_mismatch_info.txt", "w") as file:
        for info in mismatch_info:
            file.write(info + "\n")
