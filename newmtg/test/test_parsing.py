from openalea.mtg.io import *



def test0():
    # simple set of two successives axes
    s = '/I1<I2<I3<I4+I5<I6'
    g = multiscale_edit(s)
    assert len(g) == 7
    assert g.nb_vertices(scale=1)==6

def test1():
    # idem + branching point at I4
    s='/I1<I2<I3<I4[+I5<I6]+I7<I8<I9'
    g = multiscale_edit(s)
    assert len(g) ==10 
    assert g.nb_vertices(scale=1)==9

def test2():
    # idem + other notation (should give the same result)
    s='/I1<I2<I3<I4[+I7<I8<I9][+I5<I6]'
    g = multiscale_edit(s)
    assert len(g) ==10 
    assert g.nb_vertices(scale=1)==9

def test3():
    # idem + another branch on I2
    s = '/I1<I2[+I10<I11]<I3<I4[+I7<I8<I9][+I5<I6]'
    g = multiscale_edit(s)
    assert len(g) == 12 
    assert g.nb_vertices(scale=1) == 11
    

def test4():
    # remove the indexes in labels (except those that cannot be distinguished)
    s = '/I<I[+I<I]<I<I[+I7<I<I][+I5<I]'
    g = multiscale_edit(s)
    assert len(g) == 12 
    assert g.nb_vertices(scale=1) == 11

def test5():
    # if not distinguished should return an error ? 
    s = '/I<I[+I<I]<I<I[+I<I<I][+I<I]'
    g = multiscale_edit(s)
    assert len(g) == 12 
    assert g.nb_vertices(scale=1) == 11

def test6():
    # omission of '<' should be possible to map L-system strings
    # Not yet implemented
    s = "/II[+II]II[+I7II][+I5I]"

def test_properties():
    # Attributes
    s = '/I1(10,65.3,Alive,0)<I2(8,60.1,Alive,0)[+I10<I11]<I3(7,62.7,Alive,3)<I4(5,58.8,Dead,0)[+I7<I8<I9][+I5<I6]'
    g = multiscale_edit(s)
    assert len(g) == 12 
    assert g.nb_vertices(scale=1) == 11

def test_properties():
    # this should also be possible
    s1='/I1(10,65.3,,)<I2(8,60.1,,)[+I10<I11]<I3(7,62.7,,3)<I4(5,58.8,Dead,)[+I7<I8<I9][+I5<I6]'
    s2='/I1(10,65.3)<I2(8,60.1)[+I10<I11]<I3(7,62.7,,3)<I4(5,58.8,Dead)[+I7<I8<I9][+I5<I6]'
    class_type = {'diameter':'INT', 'length':'REAL', 'status':'STRING', 'type':'INT' }
    for s in [s1, s2]:
        g = multiscale_edit(s)
        assert len(g) == 12 
        assert g.nb_vertices(scale=1) == 11

def test_dynamic():
    # addition of dates:
    s = '/I1(date=10/01/92,x=10,y=65.3)*(date=20/01/92,x=12,y=69.3)*(date=02/02/92,x=15,y=70.1)<I2(date=10/01/92,x=8,y=60.1)*(date=20/01/92,x=9,y=61.3)*(date=02/02/92,x=10,y=66.3)[+I<I]<I3(date=20/01/92,x=7,y=62.7,z=3)*(date=02/02/92,x=9,y=65.5,z=1)<I4(date=02/02/92,x=5,y=58.8,status=Dead)[+I7<I<I][+I5<I]'
    class_type = {'date':'DD/MM/YY', 'x':'REAL', 'y': 'REAL', 'z':'REAL' ,'status':'STRING' }
    g = multiscale_edit(s, class_type=class_type, has_date=True)

def test_tree():
    # Tree from Godin et al. 2005
    s = '/I1[+I19[+I24[+I25]]<I20[+I21[+I26]<I22[+I23]]]<I2[+I27[+I32[+I33]]<I28[+I29[+I34]<I30[+I31]]]<I3[+I11[+I12[+I13]]]<I4[+I5[+I14[+I15]]<I6[+I16[+I17]]<I7[+I8[+I18]<I9<I10]]'
    g = multiscale_edit(s)
    assert len(g) == 35 
    assert g.nb_vertices(scale=1) == 34

def test_tree_property():
    # Same tree with attributes from Godin et al. 2005
    s = '/I1(10.5,18)[+I19[+I24[+I25]]<I20[+I21[+I26]<I22[+I23]]]<I2(9.2,20)[+I27[+I32[+I33]]<I28[+I29[+I34]<I30[+I31]]]<I3(8,18)[+I11[+I12[+I13]]]<I4(6,15)[+I5[+I14[+I15]]<I6[+I16[+I17]]<I7[+I8[+I18]<I9<I10]]'
    g = multiscale_edit(s)
    assert len(g) == 35 
    assert g.nb_vertices(scale=1) == 34
    
def test_mtg1():
    s = '/P1/S1/M1/I1\\\\[+S2/M13/I19\\\\[+S9/M16/I24\\[+M17/I25]]<I20\\[+M14/I21\\\\[+S8/M18/I26]<I22\\[+M15/I23]]]<I2\\\\[+S3/M19/I27\\\\[+S10/M22/I32\\[+M23/I33]]<I28\\[+M20/I29\\\\[+S11/M24/I34]<I30\\[+M21/I31]]]<I3\\\\[+S4/M5/I11\\[+M6/I12\\[+M7/I13]]]<I4\\[+M2/I5\\\\[+S5/M8/I14\\[+M9/I15]]<I6\\\\[+S6/M10/I16\\[+M11/I17]]<I7\\[+M3/I8\\\\[+S7/M12/I18]<I9\\<M4/I10]]\\\\\\'
    g = multiscale_edit(s)
    assert len(g) == 71 
    assert g.nb_scales() == 5
    assert g.nb_vertices(scale=1) ==1 
    assert g.nb_vertices(scale=2) == 11
    assert g.nb_vertices(scale=3) == 24
    assert g.nb_vertices(scale=4) == 34

def test_mtg2():
    s = '/P1\\/P2'
    g = multiscale_edit(s)
    assert len(g) == 3 
    assert g.nb_scales() == 2
    assert g.nb_vertices(scale=1) ==2 

def test_mtg3():
    s = '/P1/S1/M1/I1'
    g = multiscale_edit(s)
    assert len(g) == 5 
    assert g.nb_scales() == 5
    assert g.nb_vertices(scale=1) ==1 

