from persistent.dict import PersistentDict
from persistent.list import PersistentList

def obj_to_pobj(o):
    """ Return an object to a persistent object.
    Only works on list and dictionaries for now.
    """
    
    if isinstance(o, list):
        return list_to_plist(o)

    if isinstance(o, dict):
        return dict_to_pdict(o)

    return o

def list_to_plist(l):
    pl = PersistentList()
    for val in l:
        pl.append(obj_to_pobj(val))

    return pl

def dict_to_pdict(d):
    pd = PersistentDict()

    for k, v in d.items():
        pd[obj_to_pobj(k)] = obj_to_pobj(v)

    return pd
