""" Build index from directory listing

make_index.py </path/to/directory>
"""

INDEX_TEMPLATE = r"""
<html>
<head><title>${header}</title></head>
<body bgcolor="white">
<h1>${header}</h1>
<hr>
<pre>

<table><tbody>
<tr><td valign="top"><a href="../">../</a></td></tr>

% for file in files:
<tr>
    <td valign="top"> <a href="${file.name}">${file.name}</a> </td>
    <td style="padding-left: 100px">${file.date}</td>
    <td style="padding-left: 40px" >${file.size}</td>
</tr>
% endfor

</tbody></table>

</pre>
<hr>
</body>
</html>
"""




EXCLUDED = ['index.html']

import os
import argparse
import time
from collections import namedtuple

# May need to do "pip install mako"
from mako.template import Template

suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def generate(directory, header):
    fnames = [fname for fname in sorted(os.listdir(directory))
                          if fname not in EXCLUDED]
    File = namedtuple("File", "name date size")

    files = []
    for name in fnames:
        full_path = directory + "/" + name
        file_name = name
        file_time = time.ctime(os.path.getmtime(full_path))
        file_size = humansize(os.path.getsize(full_path))
        if os.path.isdir(full_path):
            file_name = name + "/"
            file_size = "-"

        files.append(File(file_name, file_time, file_size))

    header = (header if header else os.path.basename(directory))
    index_file = directory + "/index.html"
    with open(index_file, "w") as f:
        f.write(Template(INDEX_TEMPLATE).render(files=files, header=header))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    args = parser.parse_args()

    dir_list = [args.directory]
    for root, directories, filenames in os.walk(args.directory):
        for directory in directories:
            dir_list.append(os.path.join(root, directory))

    for directory in dir_list:
        generate(directory, "Index of " + directory)

if __name__ == '__main__':
        main()
