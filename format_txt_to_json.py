import json
from langdetect import detect
import io
import contextlib

def read_and_clean_file(file_path):
    """Read a file and remove empty lines."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line.strip() for line in lines if line.strip()]

def detect_language(text):
    """Detect the language of a given text."""
    return detect(text)

def filter_invalid_characters(text):
    """Replace characters that cannot be displayed with English punctuation."""
    return ''.join(char if char.isprintable() else '.' for char in text)

def format_to_json(original_file, translation_file, output_file):
    """Format two text files into a JSON structure and return terminal output."""
    # 创建一个 StringIO 对象来捕获输出
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        try:
            # 读取并处理文件
            original_lines = read_and_clean_file(original_file)
            translation_lines = read_and_clean_file(translation_file)

            if len(original_lines) != len(translation_lines):
                raise ValueError("The number of lines in the original and translation files do not match.")

            translations = []
            for num, (original, translation) in enumerate(zip(original_lines, translation_lines), start=1):
                translations.append({
                    "num": num,
                    "original": filter_invalid_characters(original),
                    "translation": filter_invalid_characters(translation)
                })

            # Detect languages
            original_language = detect_language(" ".join(original_lines[:5]))
            translation_language = detect_language(" ".join(translation_lines[:5]))

            # Create the final JSON structure
            result = {
                "translations": translations,
                "language_detection": {
                    "original_language": original_language,
                    "translation_language": translation_language
                }
            }

            # Write to output file
            with open(output_file, 'w', encoding='utf-8') as json_file:
                json.dump(result, json_file, ensure_ascii=False, indent=4)
            
            print(f"JSON file has been created successfully: {output_file}")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    return buffer.getvalue()
    # original_lines = read_and_clean_file(original_file)
    # translation_lines = read_and_clean_file(translation_file)

    # if len(original_lines) != len(translation_lines):
    #     raise ValueError("The number of lines in the original and translation files do not match.")

    # def filter_invalid_characters(text):
    #     """Replace characters that cannot be displayed with English punctuation."""
    #     return ''.join(char if char.isprintable() else '.' for char in text)

    # translations = []
    # for num, (original, translation) in enumerate(zip(original_lines, translation_lines), start=1):
    #     translations.append({
    #         "num": num,
    #         "original": filter_invalid_characters(original),
    #         "translation": filter_invalid_characters(translation)
    #     })

    # # Detect languages
    # original_language = detect_language(" ".join(original_lines[:5]))
    # translation_language = detect_language(" ".join(translation_lines[:5]))

    # # Create the final JSON structure
    # result = {
    #     "translations": translations,
    #     "language_detection": {
    #         "original_language": original_language,
    #         "translation_language": translation_language
    #     }
    # }

    # # Write to output file
    # with open(output_file, 'w', encoding='utf-8') as json_file:
    #     json.dump(result, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # Input and output file paths
    original_file = "Origin.txt"
    translation_file = "Translation.txt"
    output_file = "formatted_translations.json"

    # 执行转换并获取输出
    output = format_to_json(original_file, translation_file, output_file)
    print(output)  # 在终端显示输出