import json # to easily modify jsons
import os # to navigate through folders

# root folder of our humble mod file
CDDA_MOD_ROOT = os.path.abspath("./")

# given an object it iterates through all the pockets.
# modifies the max weight & length
# returns the object if it did anything, returns nothing if nothing was changed
used_ids = [] # can't have duplicate ids so we go first come first serve.
def cycle_object(obj):
    done_anything = False
    if 'pocket_data' in obj:
        for i in obj['pocket_data']:
            if 'max_contains_weight' in i:
                i['max_contains_weight'] = '1000 kg'
                done_anything = True
            if 'max_item_length' in i:
                i['max_item_length'] = '1 km'
                done_anything = True
    if 'snippet_category' in obj: # can't have duplicate snippet IDs apparently smh my head
        obj.pop('snippet_category')
    if done_anything:
        if 'id' in obj:
            if obj['id'] in used_ids:
                return None
            used_ids.append(obj['id'])
        return obj
    else:
        return None

# given a json, return potential file
def cycle_json(jon):
    new_jon = []
    did_anything = False
    for i in jon:
        tadd = cycle_object(i)
        if tadd is not None: # we made a change!
            did_anything = True
            new_jon.append(tadd)
    if did_anything:
        return new_jon
    else:
        return None

# write json, given json, path, and file name
def write_json(jon, path, name):
    if not os.path.exists(path): # path doesn't exist so we need to make one:
        os.makedirs(path)
    with open(os.path.join(path, name), 'w') as f:
        json.dump(jon, f, indent=4)

# given an absolute path + name to a file, run it down
def cycle_file(path, name, root):
    with open(os.path.join(path, name), 'r') as f: # open file
        new_json = cycle_json(json.load(f)) # cycle its json
        if new_json is not None:            # if anything happens then we write a new json file.
            rel_path = os.path.relpath(path, root) # gets path from root to file
            new_path = os.path.join(CDDA_MOD_ROOT, rel_path)
            write_json(new_json, new_path, name)
            #print("Printed {} to {}".format(name, new_path))

def cycle_root(root_dir):
    # iterate through all the files we could ever care about:
    for (path, dirs, file) in os.walk(root_dir):
        for i in file:
            if i.endswith('.json'): # if it's a json then we care.
                cycle_file(path, i, root_dir)

# next step is to read from a mod list.
with open("./mods.json", 'r') as f:
    # get working modlist to check
    modlist = []
    for i in json.load(f): # for each of the mod ids
        modlist.append(i)

    # look through the folder we're in (/cdda/mods/)
    for directory in os.listdir("../"): # for each folder in our current mod folder
        #print("testing mod: {}".format(directory))
        mod_path = os.path.join('../', directory)
        if mod_path == CDDA_MOD_ROOT:
            continue
        if os.path.isfile(mod_path):
            continue
        hit = False
        with open(os.path.join(mod_path, 'modinfo.json'), 'r') as g:
            mod_info = json.load(g)
            for i in mod_info:
                if i['type'] == 'MOD_INFO':
                    if i['id'] in modlist:
                        hit = True
        if hit:
            #print('\n\nCycling {}\n\n'.format(directory))
            cycle_root(os.path.abspath(mod_path))
    # look through the other mod folder: /cdda/data/mods/
    for directory in os.listdir("../../data/mods/"): # for each folder in our current mod folder
        #print("testing mod: {}".format(directory))
        mod_path = os.path.join('../../data/mods/', directory)
        if mod_path == CDDA_MOD_ROOT:
            continue
        if os.path.isfile(mod_path):
            continue
        hit = False
        with open(os.path.join(mod_path, 'modinfo.json'), 'r') as g:
            mod_info = json.load(g)
            for i in mod_info:
                if i['type'] == 'MOD_INFO':
                    if i['id'] in modlist:
                        hit = True
        if hit:
            #print('\n\nCycling {}\n\n'.format(directory))
            cycle_root(os.path.abspath(mod_path))
            
# cycle the cdda main data folder last, so the mods get to overwrite things properly.
cycle_root(os.path.abspath("../../data/json"))