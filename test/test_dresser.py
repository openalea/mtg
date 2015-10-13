from openalea.mtg.plantframe.dresser import *

def test1():
    fn = r'data/wij10.drf'
    f = open(fn)

    dr = dressing_data(f)

    f.close()
    return dr
    
def create_dressing_data(fn):
    f = open(fn)

    dr = dressing_data(f)
    
    f.close()
    assert dr

def test():
    try:
        from path import path
    except:
        from openalea.core.path import path
    dir = path('data')
    files = dir.glob('*.drf')

    for f in files:
        yield create_dressing_data, f

