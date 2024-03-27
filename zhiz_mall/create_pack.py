import os

path = os.path.abspath(__file__)
print(path)
parrent_path = os.path.dirname(path)
print(parrent_path)

dir = os.path.join(parrent_path, 'templates')
try:

    os.makedirs(dir)
except FileExistsError:
    print("文件夹已存在")

file = os.path.join(dir, '__init__.py')

try:
    with open(file, 'w') as f:
        f.write('')
        print("创建成功")
except FileExistsError:
    print("文件已存在")