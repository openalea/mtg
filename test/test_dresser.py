from openalea.mtg.plantframe.dresser import *
import pytest

def test1():
    fn = r'data/wij10.drf'
    f = open(fn)

    dr = dressing_data(f)

    f.close()
    return dr

def files_to_check():
    try:
        from path import Path as path
    except:
        from openalea.core.path import path
    dir = path('data')
    files = dir.glob('*.drf')
    return files
    
@pytest.mark.parametrize('fn', list(files_to_check()))
def test_create_dressing_data(fn):
    f = open(fn)

    dr = dressing_data(f)
    
    f.close()
    assert dr



