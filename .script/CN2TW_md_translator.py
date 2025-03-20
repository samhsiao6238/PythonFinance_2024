import sys
import zhconv
import re

def simplify_to_traditional(text):
    """將簡體中文轉換為繁體中文"""
    return zhconv.convert(text, 'zh-tw')

def is_chinese(text):
    """檢查字串是否包含中文"""
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def translate_md_file(input_file, output_file):
    """讀取 .md 文件，轉換簡體為繁體，保持英文與程式碼不變"""
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.readlines()

    translated_lines = []
    # 用於標記是否在程式碼區塊內
    code_block = False

    for line in content:
        # 檢查是否進入或退出程式碼區塊 (```)
        if line.strip().startswith("```"):
            code_block = not code_block
            translated_lines.append(line)
            continue

        if code_block:
            # 在程式碼區塊內，但仍然轉換包含中文的部分
            translated_line = re.sub(r'([\u4e00-\u9fff]+)', lambda m: simplify_to_traditional(m.group(0)), line)
        else:
            # 非程式碼區塊，完全轉換
            translated_line = simplify_to_traditional(line)

        translated_lines.append(translated_line)

    # 寫入新的繁體中文 .md 文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(translated_lines)

    print(f"翻譯完成，結果已儲存至 {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方式: python ex01.py <輸入文件.md> <輸出文件.md>")
        sys.exit(1)

    input_md = sys.argv[1]
    output_md = sys.argv[2]

    translate_md_file(input_md, output_md)
