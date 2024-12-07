import os

def load_replacement_rules(file_path):
    rules = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or '=' not in line:
                continue
            old, new = line.split('=', 1)
            rules[old.strip()] = new.strip()
    return rules

def replace_in_file(file_path, rules):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    for old, new in rules.items():
        content = content.replace(old, new)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def process_project_files(project_path, rules):
    for root, _, files in os.walk(project_path):
        for file in files:
            # 可根據需求調整匹配的文件類型
            if file.endswith(('.txt', '.md', '.py', '.js', '.ipynb')):
                file_path = os.path.join(root, file)
                replace_in_file(file_path, rules)

if __name__ == '__main__':
    project_root = os.getcwd()
    replace_file = os.path.join(project_root, '.replace')
    if not os.path.exists(replace_file):
        print("在根目錄中未找到匹配文件。")
        exit(1)
    rules = load_replacement_rules(replace_file)
    process_project_files(project_root, rules)
    print("更改作業完成。")