import io
import os

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

def compare_files(file1, file2, processed_files):
    file_type1 = determine_file_type(file1)
    file_type2 = determine_file_type(file2)

    if file_type1 is None or file_type2 is None:
        print(f"Unsupported file type for {file1} or {file2}. Skipping comparison.")
        return

    if (file1, file2) in processed_files or (file2, file1) in processed_files:
        return  # Skip already processed files

    text1 = convert_to_text(file1)
    text2 = convert_to_text(file2)

    mismatch_info = compare_text_files(text1, text2, file1, file2)

    # Print mismatch information with proper indentation and line breaks
    for info in mismatch_info:
        print(info)

    # Save mismatch information to a text file
    result_file = "combined_mismatch_info.txt"

    # Check if the info is already present in the file to avoid duplicates
    with open(result_file, 'r') as file:
        existing_info = file.read()

    if any(info not in existing_info for info in mismatch_info):
       with open(result_file, 'a+') as file:
            for info in mismatch_info:
                file.write(info + "\n")

    processed_files.add((file1, file2))

def determine_file_type(file_path):
    if file_path.lower().endswith('.xml'):
        return 'xml'
    elif file_path.lower().endswith('.accfg'):
        return 'accfg'
    else:
        return None

if __name__ == "__main__":
    processed_files = set()

    # Compare XML files
    xml_file1 = "NCR_SR_UPDATE_IUI_11.00_VER_01.00_17052023.xml"
    xml_file2 = "NCR_SR_UPDATE_IUI_11.00_VER_01.00_17052023(1).xml"
    compare_files(xml_file1, xml_file2, processed_files)

    # Compare accfg files
    accfg_file1 = "CashInCustom.accfg"
    accfg_file2 = "CashInCustom1.accfg"
    compare_files(accfg_file1, accfg_file2, processed_files)
