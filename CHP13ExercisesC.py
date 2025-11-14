#!/usr/bin/env python3
import os.path
import shelve
import hashlib

def same_contents(path1, path2):
    data1 = open(path1, 'rb').read()
    data2 = open(path2, 'rb').read()
    return data1 == data2

def walk_images(directory, extensions, db, max_depth=-1):
    for root, dirs, files in os.walk(directory, topdown=True):
        if max_depth != -1:  # We only care about depth update if the parameter is set.
            depth = root.count(os.sep) - directory.count(os.sep)
            if depth >= max_depth:
                del dirs[:]

        for file in files:
            file = os.path.join(root, file)
            if is_image(file, extensions):
                add_path(file, db)

def md5_digest(filename):
    data = open(filename, 'rb').read()
    md5_hash = hashlib.md5()
    md5_hash.update(data)
    digest = md5_hash.hexdigest()
    return digest

def add_path(file_path: str, db: shelve.Shelf):
    key = md5_digest(file_path)
    if key in db:
        if file_path not in db[key]:
            path_list = db[key]
            path_list.append(file_path)
            db[key] = path_list
    else:
        db[key] = [file_path]
    db.sync()  # This is likely redundant, but whatever.
    return db  # No real need to return this, but whatever.


def is_image(file_path: str, extensions: list):
    if not os.path.isfile(file_path): return False

    base_name, extension = os.path.splitext(file_path)
    if extension in extensions:
        return True
    return False

def main():
    extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.tiff']
    # print(is_image('photos/notes.txt', extensions))
    # print(is_image('photos/feb-2023/photo1.jpg', extensions))
    db = shelve.open( 'output/digests', 'n' )
    walk_images('photos', extensions, db)

    for digest, paths in db.items():
        if len( paths ) > 1:
            print( paths )
            print("Are they the same?", same_contents(*paths))

if __name__ == '__main__':
    main()