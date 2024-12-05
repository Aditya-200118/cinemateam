# from pathlib import Path
# from itertools import islice

# space =  '    '
# branch = '│   '
# tee =    '├── '
# last =   '└── '
# def tree(dir_path: Path, level: int=-1, limit_to_directories: bool=False,
#          length_limit: int=1000):
#     """Given a directory Path object print a visual tree structure"""
#     dir_path = Path(dir_path) # accept string coerceable to Path
#     files = 0
#     directories = 0
#     def inner(dir_path: Path, prefix: str='', level=-1):
#         nonlocal files, directories
#         if not level: 
#             return # 0, stop iterating
#         if limit_to_directories:
#             contents = [d for d in dir_path.iterdir() if d.is_dir()]
#         else: 
#             contents = list(dir_path.iterdir())
#         pointers = [tee] * (len(contents) - 1) + [last]
#         for pointer, path in zip(pointers, contents):
#             if path.is_dir():
#                 yield prefix + pointer + path.name
#                 directories += 1
#                 extension = branch if pointer == tee else space 
#                 yield from inner(path, prefix=prefix+extension, level=level-1)
#             elif not limit_to_directories:
#                 yield prefix + pointer + path.name
#                 files += 1
#     print(dir_path.name)
#     iterator = inner(dir_path, level=level)
#     for line in islice(iterator, length_limit):
#         print(line)
#     if next(iterator, None):
#         print(f'... length_limit, {length_limit}, reached, counted:')
#     print(f'\n{directories} directories' + (f', {files} files' if files else ''))

# tree(Path.home() / 'pyscratch', level=2)

# import os

# def list_files(startpath):
#     for root, dirs, files in os.walk(startpath):
#         level = root.replace(startpath, '').count(os.sep)
#         indent = ' ' * 4 * (level)
#         print('{}{}/'.format(indent, os.path.basename(root)))
#         subindent = ' ' * 4 * (level + 1)
#         for f in files:
#             print('{}{}'.format(subindent, f))
# print(list_files("C:\\Users\\bharg\\Desktop\\UGA\\Django\\cinema"))


import os

def list_files(startpath):
    ignore_dirs = {
        '__pycache__','objects','.git', 'hooks', 'profile', 'static' 'build', 'develop-eggs', 'dist', 'downloads', 'eggs', '.eggs', 'lib', 'lib64', 'parts', 'sdist', 'var', 'wheels', 'share/python-wheels', '*.egg-info', '.installed.cfg', '*.egg', 'MANIFEST', 'htmlcov', '.tox', '.nox', '.cache', '.hypothesis', '.pytest_cache', 'cover', 'instance', '.webassets-cache', '.scrapy', 'docs/_build', '.pybuilder', 'target', '.ipynb_checkpoints', 'profile_default', '.pyre', '.pytype', 'cython_debug', '.idea', 'migrations'
    }
    ignore_files = {
        '*.py[cod]', '*$py.class', '*.so', '.Python', '*.manifest', '*.spec', 'pip-log.txt', 'pip-delete-this-directory.txt', '.coverage', '.coverage.*', 'nosetests.xml', 'coverage.xml', '*.cover', '*.py,cover', '*.mo', '*.pot', '*.log', 'local_settings.py', 'ipython_config.py', '.python-version', 'Pipfile.lock', 'poetry.lock', 'pdm.lock', '.pdm.toml', '.pdm-python', '.pdm-build', '__pypackages__', 'celerybeat-schedule', 'celerybeat.pid', '*.sage.py', '.env', '.venv', 'env', 'venv', 'ENV', 'env.bak', 'venv.bak', '.spyderproject', '.spyproject', '.ropeproject', 'dmypy.json', '.css', '*.jpg', '*.jpeg', '*.png'
    }

    for root, dirs, files in os.walk(startpath):
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            # Filter out ignored files
            if not any(f.endswith(ext) for ext in ignore_files):
                print('{}{}'.format(subindent, f))

print(list_files("C:\\Users\\bharg\\Desktop\\UGA\\Django\\Team"))
