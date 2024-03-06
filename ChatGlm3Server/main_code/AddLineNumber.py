import os

# 指定文件夹路径
root_folder_path = "D4j-modelans"

# 指定要处理的文件名
target_filename = "slicecode.txt"

# 递归函数，遍历文件夹并处理文件
def process_code(file_path,file_name):
    file_code = os.path.join(file_path, file_name)
    with open(file_code, 'r', encoding='utf-8') as input_file:
        # 初始化行号计数器
        line_number = 1
        # 创建新文件并打开用于写入
        output_filename = f"{file_name}_indexed.txt"
        output_path = os.path.join(file_path, output_filename)

        with open(output_path, 'w', encoding='utf-8') as output_file:
            # 读取代码文件的每一行并添加行号后写入新文件
            for line in input_file:
                output_file.write(f"{line_number} {line}")
                line_number += 1

        # print(f"已将行号添加到新文件 '{output_path}' 中。")

def process_files_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 检查文件是否与目标文件名相同
            if file == target_filename:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as input_file:
                    # 初始化行号计数器
                    line_number = 1
                    # 创建新文件并打开用于写入
                    output_filename = f"{file}_with_line_numbers.txt"
                    output_path = os.path.join(root, output_filename)
                    
                    with open(output_path, 'w', encoding='utf-8') as output_file:
                        # 读取代码文件的每一行并添加行号后写入新文件
                        for line in input_file:
                            output_file.write(f"{line_number} {line}")
                            line_number += 1

                    print(f"已将行号添加到新文件 '{output_path}' 中。")

        for dir in dirs:
            # 递归调用处理子文件夹
            subfolder_path = os.path.join(root, dir)
            process_files_in_folder(subfolder_path)

# 开始遍历处理
process_files_in_folder(root_folder_path)
