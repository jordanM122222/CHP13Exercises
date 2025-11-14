#!/usr/bin/env python3
import os.path
import shelve

def add_word(my_str, anagram_shelf: shelve.Shelf):
    word, key = get_word_and_key(my_str)
    if key in anagram_shelf:
        if word not in anagram_shelf[key]:  # Can't treat shelf like a dictionary because it needs to be synced to fs.
            anagram_list = anagram_shelf[key]
            anagram_list.append(word)
            anagram_shelf[key] = anagram_list
    else:
        anagram_shelf[key] = [word]
    anagram_shelf.sync()  # This is likely redundant, but whatever.
    return anagram_shelf  # No real need to return this, but whatever.

def prepare(word):
    return word.strip().lower()

def get_word_and_key(word):
    word = prepare(word)
    return word, ''.join( sorted( word ) )

def load_anagram_map(db_file='files/anagram_map.db'):
    if not os.path.exists(db_file):
        word_list_to_anagram_map(db_file=db_file[:-3])  # This ensures it is loaded first, and removes .db extension.

    return shelve.open(db_file[:-3], 'c')

def shelf_to_dict(db_file):
    my_dict = {}
    with shelve.open(db_file) as db:
        for key in db:
            my_dict[key] = db[key]
    return my_dict

def dict_to_shelf(my_dict: dict, db_file):
    with shelve.open( db_file, 'c' ) as db:
        for key, value in my_dict.items():
            db[key] = value

def word_list_to_anagram_map(word_list='files/words.txt', db_file='files/anagram_map'):
    anagram_map = {}
    with open(word_list, 'r') as fp:
        for word in fp:
            word, key = get_word_and_key(word)
            anagram_map.setdefault(key, []).append(word)
    dict_to_shelf(anagram_map, db_file)

def main():
    db = load_anagram_map()
    print(db.get('eorrtv'))
    db = add_word("Trevor", db)
    db.close()  # Force the write back of the word!

    db = load_anagram_map()
    print(db.get('eorrtv'))

if __name__ == '__main__':
    main()