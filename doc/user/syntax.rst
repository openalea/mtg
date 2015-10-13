
.. _newmtg_syntax:

File syntax
###########


.. todo:: revise the entire document to check tabulation of the examples

.. contents::

General conventions
===================

In general, words can be separated by any combination of whitespace characters (SPACE, TAB, EOL). In certain files, TABs or EOL are meaningful (e.g. MTG coding files), and therefore are not considered as a whitespace character in these files.

Comments may be introduced anywhere in a file using the sharp sign #, meaning that the rest of the line is a comment. In some files, block comments can be introduced by bracketing the comment text with (# and #).

Files used by AML can be located anywhere in the UNIX hierachical file system, provided the user can access them. All references to files from within a file or from AML must be given explicitly. References to files must always be made relatively to the location where the reference is made.

In various files, user-defined names must be given to objects, attributes, etc. Unless specified otherwise, names always consist of strings of alphanumeric characters (including underscore '_') starting by a non-numeric character. A name may start by an underscore. Some names correspond to reserved keywords. Since reserved keywords always start in AMAPmod with uppercase letter, it is advised, though not mandatory, to define user-defined names starting with lowercase letter to avoid name collision. 


MTGs
====
Coding strategy
---------------

A plant multiscale topology is represented by a string of characters (see 3.2.2). The string is made up of a series of labels representing plant components (a label is made up of an alphabetic character in A-Z,a-z and a numeric index) and of symbols representing either the physical relationships between the components. Character '/' is used for decomposition relationship (see next paragraph), '+' is used for branching relationship and '<' for successor relationship. For example::

    /I1<I2<I3<I4+I5<I6

is a string representing 6 components with labels I1, I2, I3, I4, I5, I6. I1 to I4 are a sequence of components defining an axis which bears a second axis made up of the sequence of components I5 and I6. In this string every component is connected with at most one subsequent component (either by a '<' or by a '+')

As illustrated by this example, the name of an entity is built by concatenating the consecutive entity labels encountered while moving along the plant structure from the plant basis to the considered entity. For example, consider the decomposition of a plant in terms of axes. Assume this plant is made of 3 axes: axis A1 bears axis A2, which itself bears axis A3. Then, the respective names of the axes are::

    /A1
    /A1+A2
    /A1+A2+A3

Symbol '+' refers to the type of connection between A1 and A2, A2 and A3 respectively. Now, consider another plant considered at the scale of growth units. A growth unit U90 bears a growth unit U91 which is itself followed on the same axis by U92. The respective names of these growth units are ::

    /U90
    /U90+U91
    /U90+U91<U92

These two examples illustrate how to define the name of plant entities when only one scale of description is considered. When several scales are considered, this strategy can be extended as explained in section 3.2.2.

Assume for instance that axis A1 of the previous example is composed of 3 consecutive growth units and that axis A2 is borne by the second growth units of A1. Then the name of A2 is defined as ::

    /A1/U1<U2+A2

Relative names
--------------

Every name of an entity is thus the concatenation of a series of pairs (relation symbol,label) : name = relation label relation label relation label relation...label relation label

Let us consider any prefix p of a name n of an entity x of the plant, made of a series of pairs (relation label). According to the recursive construction of entity names, this prefix defines the name of an entity y on the path from the plant basis to the entity with name n. The name of x has thus the form::

    n = p m

where m is a series label relation ... label relation. Entity x has absolute name n. Alternatively we can say that x has relative name m with respect position p, i.e. relatively to entity y.

Examples ::

    /S1/A1/E1+A3 has relative name /A1/E1+A3 in position /S1
    /S1/A1/E3+A1/E4+S1/U2/E3+U1/E5+U4/E4 has relative name +U1/E5+U4/E4 in position /S1/A1/E3+A1/E4+S1/U2/E3

Coding files
------------------

The coding of a plant (or of a set of plants) is carried out in a so called "coding file". The code consists of a description of the MTG representing plant architectures. A coding file contains two parts:
    * a header which contains a description of the coding parameters,
    * the code of the plant architecture.

The header contains general informations related to all individuals:
    * the set of all entity classes used in the MTG description,
    * a detailed description of the topological properties of these classes,
    * and the set of all attributes used for any entity in the plant description.

In a MTG coding file, TABs are meaningful. They correspond to column separators. Consequently, a MTG coding file should be edited using a spreadsheet editor. If a sharp '#' is inserted on a line, every character until the next TAB on the same line is considered as a comment and is not interpreted.

Header
~~~~~~

**General parameter section**

For historical reasons, two forms of plant architecture coding have been developed, denoted FORM-A et FORM-B. FORM-A is the most general and should be employed. FORM-B is available for ascendant compatibility with former coding forms employed in the AMAP laboratory [Rey et al, 97]. Whatever the coding form used the plant built by AMAPmod is the same. The form of the coding language must be specified in the coding file by specifying either FORM-A or FORM-B following the keyword CODE, in the next column, for example :
CODE:   FORM-A
This definition is mandatory.

**Class definition section**

Classes must then be declared. This is done in a section beginning with keyword CLASSES. Then a line is defined for each class of the MTG. The first column, entitled SYMBOL, contains the symbolic character denoting a class used in the MTG. This symbol most be an alphabetic character (either upper or lower-case letter). Two classes either at identical or different scales must have different symbolic characters.
The second column, entitled SCALE, represents the scale at which this class appears in the MTG. There are no a priori limitation related to the number of classes, however, these must be consecutive integer greater or equal to 0. Scale i, i>1, can only appear if scale i-1 has appeared before.

::

    CLASSES
    SYMBOL  SCALE   DECOMPOSITION   INDEXATION  DEFINITION
    $   0   FREE    FREE    IMPLICIT
    P   1   CONNECTED   FREE    IMPLICIT
    U   2   <-LINEAR    FREE    EXPLICIT
    I   2   <-LINEAR    FREE    EXPLICIT
    E   3   NONE    FREE    IMPLICIT

Symbol $ represent the entire database and is defined by definition at scale 0.
Keyword DECOMPOSITION defines the types of decomposition that can have a vertex (i.e. a plant constituent) : CONNECTED, LINEAR, <-LINEAR, +-LINEAR, FREE, NONE. Key word CONNECTED means that the decomposition graph of a vertex at the next scale is connected. Keyword LINEAR means that the decomposition graph of a vertex at the next scale is a linear sequence of vertices. Besides, if this all the constituents of this sequence are connected using a single type of edge (respectively < or +), then keyword <-LINEAR et +-LINEAR can respectively be used. Keyword FREE allows any type of decomposition structure while keyword NONE, specifies that the components of a unit must not be decomposed.
Column INDEXATION is not used.
Column DEFINITION must be filled with value EXPLICIT if any entity of that class has feature values (i.e. attributes). IMPLICIT should be used otherwise.

This section is mandatory.

**Topological constraints section**

Topological constraints are described in the next section, beginning with keyword DESCRIPTION. Here, each line defines for a pair of classes at the same scale one allowed type of connection. It contains 4 columns, LEFT, RIGHT, RELTYPE, and MAX. For any class in column LEFT, the column RIGHT defines a list of class (appearing at the same scale) which can be connected to it using a connection of type RELTYPE. The maximum number of connections of type RELTYPE that can be made on an entity from column is defined in column MAX. If column MAX contains a question mark '?', the number of connections is not bounded. If a class does not appear in the column LEFT, then entities of this class cannot be connected to other entities in the MTG.

::

    DESCRIPTION:
    LEFT    RIGHT   RELTYPE MAX
    U   U,I +   ?
    U   U,I <   1
    I   I   +   ?
    E   E   <   1
    E   E   +   1

Let us resume on the example from the above CLASS section with its DESCRIPTION section. Since class P does not appear in the left column, a P cannot be connected to any other entity at scale 1, e.g. to any other P. Entities of type U can be connected to entities of either type I or U, for any of the connection types < et +. An entity of type U can be connected by relation + to any number of Us or Is. However, they can only be connected by relation < to at most one entity of either type U or I. Entities of type I cannot be connected by relation < to any type of entity, while they can be connected to other I's by relation +. At scale 3, any E can be connected to only one other E by either relation + or <.
This section is mandatory but can contain no topology description.

**Attribute section**

The third and last part of the header contains a list of names defining the features that can be attached to plant entities and their types. This part begins with keyword FEATURES. Thelist of names appears in column NAME and the corresponding types in column TYPE. The name of an attribute might be either a reserved keyword (see a list below) or a user-defined name. The types of attributes can be INT (integer), REAL (real number), STRING (string of characters from {A...Za...z-+. /} and which are bounded to 14 characters max), DD/MM, DD/MM/YY, MM/YY, DD/MM-TIME, DD/MM/YY-TIME (Dates), GEOMETRY (geometric objects defined in a .geom file), APPEARANCE (appearance objects defined in a .app file), OBJECT (general object defined in generic type of file).

::

    FEATURES:
    NAME    TYPE
     
    Alias   STRING
    Date    DD/MM
    NbEl    INT
    State   STRING
    flowerNb    INT
    len INT
    TopDiameter REAL
    geom    GEOMETRY    geom1.geom
    appear  APPEARANCE  material.app

Certain names of attributes are reserved keywords. They all start by an upper-case letter. If they appear in the feature list, they must be in the same order as in the following description. Alias, of type STRING (formerly ALPHA), must come first if used. It allows the user to define aliases for plant entities to simplify some code strings. Date, is used to define the observation date of an entity. NbEl (NumBer of ELements), defines the number of components on any entity at the next scale. Length is the length of an entity. BottomDiameter et TopDiameter respectively define the bottom and top stretching values of a tapered transformed that is applied to the geometric symbol representing this entity (for branch segments associated with cylinder as a basic geometrc model, this defines cone frustums). State of type STRING defines the state of an entity at the time of observation. This state can be D (Dead), A (Alive), B (Broken) , P (Pruned), G (Growing), V (Vegetative), R (Resting), C (Completed), M (Modified). These letters can be combined to form a string of characters, provided they consistent with one another. Such state descriptions are checked during the parsing of the MTG and possible inconsistencies are detected.

This section is mandatory but can contain no features.

Coding section
~~~~~~~~~~~~~~

The section containing the code of a MTG starts by keyword MTG.

The next line contains a list of column names. In the first column, the keyword TOPO indicates that this column and the next unlabelled column are reserved for the topological code. On the same line, all the names that appear in the FEATURE section of the header must appear, in the same order, one column after the other, starting with the first feature name in a column sufficiently far from the TOPO column to leave enough space for the topological code (see examples below).

The topological code must necessarily start by a '/' like in::

    /P1/A1...

It can spread on all the columns before the first feature column.

Since entity names have a nested definition, a plant description can be made on a single line. However, if one wants to declare feature values attached to some entity, the plant code must be interrupted after the label of this entity, attributes must be entered on the same line in corresponding columns, and the plant code must continue at the next line.

Note that in the current implementation of the parser, an entity which has no features uses obviously 0 bytes of memory for recording features, however, assuming that the total number of features is F, if an entity has at least one feature value defined, it uses a constant space F*14 bytes to record its feature (whatever the actual number of features defined for this entity).

**Example**

Here is an example of a coding file corresponding to plant illustrated on Figure 4-1::

    CODE:   FORM-A
    CLASSES:
    SYMBOL  SCALE   DECOMPOSITION   INDEXATION  DEFINITION
    $   0   FREE    FREE    IMPLICIT
    P   1   CONNECTED   FREE    IMPLICIT
    A   2   <-LINEAR    FREE    EXPLICIT
    S   2   CONNECTED   FREE    EXPLICIT
    U   3   NONE    FREE    IMPLICIT
    DESCRIPTION:
    LEFT    RIGHT   RELTYPE MAX
    A   A,S +   ?
    U   U   <   1
    U   U   +   ?
    FEATURES:
    NAME    TYPE
    MTG:
    TOPO
    /P1/A1
    /P1/A1/U1<U2+S1
    /P1/A1/U1<U2+S2
    /P1/A1/U1<U2+A1
    /P1/A1/U1<U2+A1/U1<U2+S1
    /P1/A1/U1<U2<U3+S1
    /P1/A1/U1<U2<U3+A2
    /P1/A1/U1<U2<U3+A2/U1<U2<U3+A3
    /P1/A1/U1<U2<U3+A2/U1<U2<U3+A3/U1+S1
    /P1/A1/U1<U2<U3+A2/U1<U2<U3<U4
    /P1/A1/U1<U2<U3<U4

In this example, certain names use frequently the same prefix which can be long (this bit of code contains 225 characters). We are going to introduce successively different strategies in order to simplify this first coding scheme.

The first simplification consists of giving a name (alias) to an entity name which is used frequently in the name of others.

::

    # before the header is identical to the previous one
    FEATURES:
    NAME    TYPE
    Alias   ALPHA
    MTG:
    TOPO    Alias
    /P1/A1  A1
    (A1)/U1<U2+S1   Branch1
    (A1)/U1<U2+S2
    (A1)/U1<U2+A1
    (A1)/U1<U2+A1/U1<U2+S1
    (A1)/U1<U2<U3+S1
    (A1)/U1<U2<U3+A2    A2
    (A2)/U1<U2<U3+A3
    (A2)/U1<U2<U3+A3/U1+S1  Branch2
    (A2)/U1<U2<U3<U4
    /P1/A1/U1<U2<U3<U4

An alias can be associated with a given entity by defining its name in column Alias. This name can then be reused in the topological section by enclosing it between parentheses. If an alias is used as a prefix of an entity, the code of this entity must be given relatively to this alias. For entity A2, for instance, we can see that its name is /U1<U2<U3+A2 relatively to position A1 which is an alias for /P1/A1. The absolute name of A2is thus, /P1/A1/U1<U2<U3+A2. The code part of this file has now a size of 173 characters, i.e. 78% of the initial code.

The code of the MTG can be further simplified. We can avoid completely the repetition of bit of codes. Assume that entity y has a code of the form XY where X represents the code of some entity x. For example X is /P1/A1 and Y is /U1<U2<U3+A2 in the previous example. If X already appears in column of the topological section, then we may consider that if subsequently Y appears at a different line, but shifted to the right by one column, then Y is actually follows X which is thus its prefix. Then Y is a relative name with respect to position X. In our example, this leads to ::

    /P1/A1  # code of x
    /P1/A1/U1<U2<U3+A2  # code of y

which becomes ::

    #column1    #column2
    /P1/A1      # code de x
        /U1<U2<U3+A2    # code de y

The fact that the code of y is shifted one column to the right, allows us to interpret /U1<U2<U3+A2 as the continuation of /P1/A1 leading to the absolute name /P1/A1/U1<U2<U3+A2 which is actually the code of y.

By applying this new rule on the complete previous example we obtain the following code ::

    MTG:
    TOPO
    #column1    #column2    #column3    #column4    #column5
    /P1/A1
        /U1<U2
            +S1
            +S2
            +A1/U1<U2+S1
            <U3
                +A2/U1<U2<U3
                    +A3/U1+S1
                    <U4
                <U4

Now the number of characters used in the code is now 63 and corresponds to 28% of the initial code. However, this compressed code raises two new problems. The first problem is that the number of columns necessary has greatly increased. The second is that it is difficult to recognise the structural organisation of the plant in the way the code displays it.

To address both problem, a new syntactic notation is introduced. Each time a relative code starts with character ^ in a given cell, the current relative code must be interpreted with respect to the position whose code is the latest code defined in the same column just above the current cell. Using the ^ notation::

    MTG:
    TOPO
    /P1/A1
    ^/U1<U2
        +S1
        +S2
        +A1/U1<U2+S1
    ^<U3
        +A2/U1<U2<U3
            +A3/U1+S1
        ^<U4
    ^<U4

Here the number of columns used is equal to the number of orders in the plant (i.e. 3), which bounds the total number of columns required and best reflects in the code the botanical structure of the plant. Entities of order i are defined in column i which greatly improves the code leagibility. Finaly, the number of characters used is 69, i.e. 31% of the initial extended code.

In some cases, a series of consecutive entities must be coded, which produces long lines of code just as this one::

    A1/U87<U88<U89<U90<U91<U92<U93+A2

Such a line can be abbreviated by using the << sign ::

    A1/U87<<U93+A2

U87<<U93 is a syntactic shorthand for U87<U89<U90<U91<U92<U93.

Symbol ++ is defined similarly: U87++U93 is a shorthand for U87+U89+U90+U91+U92+U93.

Note that in such cases, the entities implicitly defined cannot have attributes: for instance, the code::

    TOPO    diam    flowers
    /A1/U87<<U93    10.3    2

Means that an axis A1 is made of a series of 7 growth units, labelled from U87 to U93 and that U93 has a diameter of 10.3 and bears 2 flowers. In some cases, we want to express that the attributes are shared by all entities. This can be expressed as follows::

    TOPO    diam    flowers
    /A1/U87<.<U93       1

which means that every growth units from U87 to U93 has exactly 1 flower. Notation +.+ is defined similarly.

Here follows the complete code of plant of Figure 4-1::

    CODE:   FORM-A
    CLASSES:
    SYMBOL  SCALE   DECOMPOSITION   INDEXATION  DEFINITION
    $   0   FREE    FREE    IMPLICIT
    P   1   CONNECTED   FREE    IMPLICIT
    A   2   <-LINEAR    FREE    EXPLICIT
    S   2   CONNECTED   FREE    EXPLICIT
    U   3   NONE    FREE    IMPLICIT
    DESCRIPTION:
    LEFT    RIGHT   RELTYPE MAX
    A   A,S +   ?
    U   U   <   1
    U   U   +   ?
    FEATURES:
    NAME    TYPE
    MTG:
    TOPO
    /P1/A1
    ^/U1<U2
            +S1
        +S2
        +A1/U1<U2+S1
    ^<U3
        +A2/U1<<U3
            +A3/U1+S1
        <U4
    ^<U4

Examples of coding strategies in different classical situations
----------------------------------------------------------------------

Non linear growth units
~~~~~~~~~~~~~~~~~~~~~~~

Until now we have only used linear growth units, i.e. entities whose decomposition in a linear set of entities. It is possible to define branching growth-units, which are not a part of an axis. The plant illustrated in Figure 4-2 illustrates such non-linear entities.

::


    CODE:   FORM-A
    CLASSES:
    SYMBOL  SCALE   DECOMPOSITION   INDEXATION  DEFINITION
    $   0   FREE    FREE    IMPLICIT
    F   1   CONNECTED   FREE    IMPLICIT
    U   2   NONE    FREE    IMPLICIT
    DESCRIPTION:
    LEFT    RIGHT   RELTYPE MAX
    F   F   +   ?
    F   F   <   1
    U   U   +   ?
    U   U   <   1
    FEATURES:
    NAME    TYPE
    MTG:
    TOPO
    /F1/U1<U2
        +U3<U4<F2/U1
            +U2
            +U3
        +U5+F3/U1

Sympodial plants
~~~~~~~~~~~~~~~~

Sympodial plants often contain apparent axes made up of series of modules (or axes). At a macroscopic scale, the plant is described in terms of apparent axes connected to one another (Figure 4-3) depict a typical sympodial plant::

    CODE:   FORM-A
    CLASSES:
    SYMBOL  SCALE   DECOMPOSITION   INDEXATION  DEFINITION
    $   0   FREE    FREE    IMPLICIT
    S   1   +-LINEAR    FREE    IMPLICIT
    A   2   <-LINEAR    FREE    IMPLICIT
    A   2   <-LINEAR    FREE    IMPLICIT
    DESCRIPTION:
    LEFT    RIGHT   RELTYPE MAX
    S   S   +   ?
    A   A,a +   1
    A   A   +   ;1
    FEATURES:
    NAME    TYPE
    MTG:
    TOPO
    /S1
    ^/A1+A2
        +S1
        ^/a1+A2+A3
    ^+A3
        +S1
        ^/a1+A2
    ^+A4+A5

Note in this example the role of ^ which enables us to preserve the structure of the plant into the code itself. Indeed, apparent axes appear in columns corresponding to their apparent order.

Dominant axes
~~~~~~~~~~~~~

Similarly, dominant axes in a plant can be identified using macroscopic units Figure 4-4 illustrates how to code dominant axes::

    CODE:   FORM-A
    CLASSES:
    SYMBOL  SCALE   DECOMPOSITION   INDEXATION  DEFINITION
    $   0   FREE    FREE    IMPLICIT
    D   1   +-LINEAR    FREE    IMPLICIT
    A   2   NONE    FREE IMPLICIT
    DESCRIPTION:
    LEFT    RIGHT   RELTYPE MAX
    D   D   +   ?
    A   A   +   ?
    FEATURES:
    NAME    TYPE
    MTG:
    TOPO
    /D1
    ^/A1++A7
        +D1/A1
            +D3/A1+A2
        ^+A2++A6
        +D2/A1
            +D4/A1+A2
        ^+A2++A5

Whorls and supra-numerary buds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Whorls and supra-numerary buds can be encoded in several ways. One possible solution is to use the multiscale property a a MTG as illustrated in the following example.

::

    CODE:   FORM-A
    CLASSES:
    SYMBOL  SCALE   DECOMPOSITION   INDEXATION  DEFINITION
    $   0   FREE    FREE    IMPLICIT
    U   1   <-LINEAR    FREE    IMPLICIT
    E   2   <-LINEAR    FREE    EXPLICIT
    V   3   FREE    FREE    EXPLICIT
    N   4   NONE    FREE    IMPLICIT
    DESCRIPTION:
    LEFT    RIGHT   RELTYPE MAX
    U   U   +   ?
    U   U   <   1
    E   E   <   1
    E   E   +   ?
    FEATURES:
    NAME    TYPE
    MTG:
    TOPO
    /U90
    ^/E1
        /V1
            /N1+U91
            /N2+U91
        /V2
            /N1+U91
            /N2+U91
        /V3
            /N1+U91
    ^<E2
        /V1
            /N1+U91
        /V2
            /N1+U92
            /N2+U92
        /V3
            /N1+U92
            /N2+U92
    ^<E3 ...

Entities E denote internodes. Each internode contains a whorl, whose elements are denoted by class V. Each V can itself be decomposed into several supranumerary positions, denoted by class N. Then on each position, a growth unit (class U) can be described. Note that within a whorl E, V positions are not connected to one another. They are simply considered as one part of the whorl. This is also true for supra-numerary positions.

Plant growth observation
~~~~~~~~~~~~~~~~~~~~~~~~

Plant growth can be observed and described using MTGs. To this end, observation dates are recorded. If some entity is observed at several dates, the new values of its attributes at different dates are recorded on consecutive lines where the topological code of the entity is not repeated but rather replaced by a star symbol '*'.

::


    CODE:   FORM-A
    CLASSES:
    SYMBOL  SCALE   DECOMPOSITION   INDEXATION  DEFINITION
    $   0   FREE    FREE    IMPLICIT
    P   1   CONNECTED   FREE    IMPLICIT
    U   2   NONE    FREE    IMPLICIT
    DESCRIPTION:
    LEFT    RIGHT   RELTYPE MAX
    U   U   <   1
    U   U   +   ?
    FEATURES:
    NAME    TYPE
    Date    DD/MM/YY
    MTG:
    TOPO    Date
    /P1
    ^/U1<U2     08/06/00
    *   19/06/00
    *   30/06/00
    *   10/07/00
        +U1<U2  19/06/00
        *   30/06/00
        *   10/07/00
    ^<U3    19/06/00
    *   30/06/00
        +U1<<U3     19/06/00
        *       30/06/00
        *       10/07/00
        <U4     30/06/00
        *       10/07/00

Branching units located on the bearer according their height from the basis

In some cases, it is useful to use the index of an entity label to record information. Here, the index of the entity is used to denote the position of an element is used to record the height of this position with respect to the basis of the corresponding axis.

::

    CODE:   FORM-A
    CLASSES:
    SYMBOL  SCALE   DECOMPOSITION   INDEXATION  DEFINITION
    $   0   FREE    FREE    IMPLICIT
    X   1   FREE    FREE    IMPLICIT
    L   2   NONE    FREE    IMPLICIT
    DESCRIPTION:
    LEFT    RIGHT   RELTYPE MAX
    X   X   +   ?
    FEATURES:
    NAME    TYPE
    MTG:
    TOPO        Alias
    /X90
        /L50+X91
        /L100+X91   A91
        /L123+X92
    (A91)       # Back to axis borne at position L100
        /L10+X92
        /L25+X92
        ...

Description of a plant from the extremities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On some plants, it is easier to described branches starting from the bud of the stem on proceeding downward to the stem basis. This is the case for instance, for large trees where biological markers of growth, nodes, growth unit limits, sympodial module, etc., are more leagible near the branch extremities. Here follows a strategy to code the plant in such a case.

::


    CODE:   FORM-A
    CLASSES:
    SYMBOL  SCALE   DECOMPOSITION   INDEXATION  DEFINITION
    $   0   FREE    FREE    IMPLICIT
    P   1   CONNECTED   FREE    IMPLICIT
    U   2   <-LINEAR    FREE    EXPLICIT
    E   3   NONE    FREE    EXPLICIT
    DESCRIPTION:
    LEFT    RIGHT   RELTYPE MAX
    U   U   +   ?
    U   U   <   1
    E   E   <   1
    E   E   +   1
    FEATURES:
    NAME    TYPE
    MTG:
    TOPO
    /P1
    ^/U86
        /E2+U87
    ^<U87
    ^<U88
    ^<U89
        /E10+U89
        /E4+U90
        /E3+U90
        /E1+U90
    ^<U90
        /E6+U90
        /E3+U90
        /E2+U91
        /E1+U91
    ^<U91
        /E7+U91 # 7th internode from the apex U91
        /E3+U92 # 3th internode from the apex U91
        /E2+U92 # 2nd internode from the apex U91

The entities of the stem must be ordered in the file bottom-up (cf. the firt column where growth units U have increasing indexes). However, the positions within a given growth unit is given from top down to the basis of this growth unit. In addition, if the user wants to enter the stem entities (here growth units) from the top down to the basis of the stem, (s)he can use a laptop computer and insert new growth units (say U90) before the ones already observed at the top (say U91).

A second solution consists of using a FORM-B code. Using this more specific code allows you to enter the entities of the stem from top to basis (see first column).

::


    CODE:   FORM-B
    CLASSES:
    SYMBOL  SCALE   DECOMPOSITION   INDEXATION  DEFINITION
    $   0   FREE    FREE    IMPLICIT
    P   1   CONNECTED   FREE    IMPLICIT
    U   2   <-LINEAR    FREE    EXPLICIT
    E   3   NONE    FREE    EXPLICIT
    DESCRIPTION:
    LEFT    RIGHT   RELTYPE MAX
    U   U   +   ?
    U   U   <   1
    E   E   <   1
    E   E   +   1
    FEATURES:
    NAME    TYPE
    MTG:
    TOPO
    /P1
    ^/U91
        /E2+U92 # 2nd internode from the apex U91
        /E3+U92 # 3rd internode from the apex U91
        /E7+U91 # 7th internode from the apex U91
    ^/U90
        /E1+U91
        /E2+U91
        /E3+U90
        /E6+U90
    ^<U89
        /E1+U90
        /E3+U90
        /E4+U90
        /E10+U89
    ^<U88
    ^<U87
        /E7+U87

Reference Manual - STAT module 4.2 Dressing files 

Dressing Files (.drf)
=====================

The dressing data are the default data that are used to define the geometric models associated with geometric entities and to compute their geometric parameters when inference algorithms cannot be applied. These data are basically constant values (see the table below) and may be redefined in the dressing file. If no dressing file is defined, default (hard-coded) values are used (see table below). The dressing file .drf , if it exists in the current directory, is always used as a default dressing file.

The dressing data entries can be subdivided into 3 categories (any of these categories can be omitted).

Definition of basic geometric models associated with plant components
---------------------------------------------------------------------

A graphic model can be associated with a component in the following way (all keywords are in boldface characters):

   1. First, a set of all the basic geometric models of interest must be defined. This is done by specifying a file containing the geometric description of these models (for a definition of the syntax of geometric models, refer to the annexe section)::

          Geometry = file1.geom
          Geometry = ../../file2.geom

      The effect of these lines is to load the geometric models that are defined in files file1.geom and in file ../../file2.geom. Each geometric model defined is these files is associated with a symbolic name. If the same symbolic name is found twice during the loading operation, an error is generated and should be corrected.

   2. Any symbolic name (like internode) can then be associated with a component using the class of the component as follows::

          Class I = internode
 
      where I corresponds to a class name. This means that all the vertices of class I will have a geometry defined by the geometric model internode. Note that class I does not necessarily correspond to a valid class of a MTG (however, it should be a alphabetic letter in a-z,A-Z).

Alternatively, to allow for ascendant compatibility with previous versions of AMAPmod, it is possible to directly refer to geometric models defined in .smb files. In this case, the set of geometric models corresponds to the files contained in directory SMBPath and a geometric model can be loaded in AMAPmod by identifying a smb file in this directiry. This is done as follows in the dressing file::

    SMBPath = ../../databases/SMBFiles
    SMBModel internode2 = nentn105
    SMBModel leaf3 = oakleaf

Here, geometric models internode2 and are respectively associated with polygon files **nentn105.smb** and **oakleaf.smb** which are both located in directory **../../databases/SMBFiles**.

Like exposed above, SMB geometric models can then be associated with vertex classes::

    Class J = internode2
    Class F = leaf3

Then, global shapes can be defined for branches. This is done using the feature "category" defined for branches. The category of a branch is defined by the category of its first component. Note that the category may depend on the scale at which a branch is considered. For each category, the user can associate a 3 dimensional shape as a 3D bezier curve. The shape of the branch is then fit to the general shape associated with its category.

Assuming a set of Bezier curves are specified in a file beziershapes.crv (for example), we can associate branch categories with the Bezier curves using the following notation::

    BranchPattern = ../Curves/beziershapes.crv
    Form category = curve2

Note that the file beziershapes.crv is included, using a path relative to the directory where the .drf file itself is located. Alternatively, an absolute filename could be given. The structure of the file beziershapes.crv is discribed in section 4.4.

Definition of virtual elements
------------------------------

Components that don't appear in an MTG description can be added to a MTG (e.g. leaves, flowers or fruits). It is possible to define these new symbols as follows::

    Geometry = file1.geom

    SMBPath = SMBFiles
    SMBModel leaf = feui113

    Class L = leaf
    Class A = apple
    Class B = apricot_flower

    LeafClass = L
    FlowerClass = B
    FruitClass = A

A symbol L (a character) is defined and is associated with geometric model leaf. The two last lines associate respectively virtual leaf and fruit components with the geometric model associated with classes L and A.

Definition of defaults parameters
-----------------------------------------

The value of default parameters used to compute geometric models can be changed in the dressing file. Here follows the complete list of these parameters illustrated on an example::

    # Default geometric units (these quantities are used
    # to divide every value of the corresponding type before use)

    LengthUnit = 10
    DiameterUnit = 100
    AlphaUnit = 1

    DefaultAlpha = 30
    DefaultTeta = 0
    DefaultPhi = 90
    DefaultPsi = 180

    DefaultCategory = 3
    DefaultTrunkCategory = 0

    Alpha = Relative
    Phyllotaxy = 2/5

    DefaultEdge = PLUS # used for plantframe construction

    # Redefinition of default values of the geometric models of
    # components (here component S)

    MinLength S = 1000
    MinTopDiameter S = 20
    MinBottomDiameter S = 20

    # Redefinition of default values of the geometric models of
    # virtual components

    LeafLength = 1
    LeafTopDiameter = 2
    LeafBottomDiameter = 2
    LeafAlpha = 0
    LeafBeta = 0

    FruitLength = 1
    FruitTopDiameter = 1
    FruitBottomDiameter = 1
    FruitAlpha = 0
    FruitBeta = 0

    FlowerLength = 10
    FlowerTopDiameter = 5
    FlowerBottomDiameter = 5
    FlowerAlpha = 180
    FlowerBeta = 0

    DefaultTrunkCategory = 0
    DefaultDistance = 1000
    NbPlantsPerLine = 6

    # Colors for interpolation

    MediumThresholdGreen = 1
    MediumThresholdRed = 0
    MediumThresholdBlue = 0
    MinThresholdGreen = 0
    MinThresholdRed = 0
    MinThresholdBlue = 1
    MaxThresholdGreen = 0
    MaxThresholdRed = 1
    MaxThresholdBlue = 0

Any of these keywords can be omitted in the dressing file. If omitted, a parameter takes a default value, hard-coded into AMAPmod. The default values are defined in the following table:
i

.. tabularcolumns:: |l|l|l|l|

======================= =================================================================================== =============== ===================================
Name of the parameter   Description                                                                         Default value   Values
======================= =================================================================================== =============== ===================================
SMBPath                 Plant where SMB files are recorded                                                  .               STRING
LengthUnit              Unit used to divide all the length data                                             1               INT
AlphaUnit               Unit used to divide all the insertion angle                                         180/PI          INT
AzimutUnit              Unit used to divide all the angles                                                  180/PI          INT
DiametersUnit           Unit used to divide all the diameters                                               1               INT
DefaultEdge             Type of edge used to reconstruct a connected MTG                                    NONE            PLUS or LESS
DefaultAlpha            Default insertion angle (value in degrees with respect to the horizontal plane).    30              REAL
Phillotaxy              Phyllotaxic angle (given in degrees) or in number of turns over number of leaves 
                        for this number of turns.                                                           180             REAL or ratio e.g. 2/3
Alpha                   Nature of the insertion angle.                                                      Absolute        Absolute or Relative
DefaultTeta             Default first Euler angle                                                           0               REAL
DefaultPhi              Default second Euler angle                                                          0               REAL
DefaultPsi              Default third Euler angle                                                           0               REAL
MinLength S             Default length for elements whose class is S.                                       100             INT
MinTopDiameter S        Default top diameter for elements whose class is S.                                 10              INT
MinBotDiameter S        Default bottom diameter for elements whose class is S.                              10              INT
DefaultTrunkCategory    Default category for elements of the plant trunk. The default category of the 
                        other axes is their (botanical) order starting at 0 on the trunk.                   -1              INT
DefaultDistance         Distance between the trunk of two plants when several plants are vizualized 
                        at a time                                                                           100             REAL
NbPlantsPerLine         Number of plants per line when several plants are vizualized at a time              10              INT
MediumThresholdGreen    Green component of the color used for the values equal to the 
                        MediumThreshold (see command Plot on a PLANTFRAME) in the case of a 
                        color interpolation.                                                                0.05            REAL
MediumThresholdRed      Idem for the red component.                                                         0.07            REAL
MediumThresholdBlue     Idem for the blue component.                                                        0.01            REAL
MinThresholdGreen       Green component of the color used for the values equal to the 
                        MinThreshold (see command Plot on a PLANTFRAME) in the case of a color 
                        interpolation.                                                                      1               REAL
MinThresholdRed         Idem for the red component.                                                         0               REAL
MinThresholdBlue        Idem for the blue component.                                                        0               REAL
MaxThresholdGreen       Green component of the color used for the values equal to the MaxThreshold 
                        (see command Plot on a PLANTFRAME) in the case of a color interpolation.            0               REAL
MaxThresholdRed         Idem for the red component                                                          1               REAL
MaxThresholdBlue        Idem for the blue component.                                                        1               REAL
Whorl                   Number of virtual symbols per node                                                  2               INT
LeafClass               Class used for a leaf                                                               L               CHAR
LeafLength              Length of the leaf                                                                  50              REAL
LeafTopDiameter         Top diameter of the leaf                                                            5               REAL
LeafBottomDiameter      Bottom diameter of the leaf                                                         5               REAL
LeafAlpha               Insertion angle of a leaf                                                           30              REAL
LeafBeta                Azimuthal angle of a leaf (w.r.t its carrier)                                       180             REAL
FruitClass              Class used for a fruit                                                              F               CHAR
FruitLength             Length of the fruit                                                                 50              REAL
FruitTopDiamter         Top diameter of the fruit                                                           5               REAL
FruitBottomDiameter     Bottom diameter of the fruit                                                        5               REAL
FruitAlpha              Insertion angle of a fruit                                                          30              REAL
FruitBeta               Azimuthal angle of a fruit (w.r.t its carrier)                                      180             REAL
FlowerClass             Class used for a flower                                                             W               CHAR    
FlowerLength            Length of the flower                                                                50              REAL
FlowerTopDiameter       Top diameter of the flower                                                          5               REAL
FlowerBottomDiameter    Bottom diameter of the flower                                                       5               REAL
FlowerAlpha             Insertion angle of a flower                                                         30              REAL
FlowerBeta              Azimuthal angle of a flower (w.r.t its carrier)                                     180             REAL
======================= =================================================================================== =============== ===================================

Example of dressing file
-------------------------
see aml example

Curve Files (.crv)
==================

A curve file contains the specification of Bezier curves. It has the following general structure:

:math:`n`
curve1
:math:`k_1`
:math:`x_1\;y_1\;z_1`
...
:math:`xk1 yk1 zk1`
curve2
:math:`k2`
:math:`x1 y1 z1`
...
:math:`xk2 yk2 zk2`
...
curven
:math:`kn`
:math:`x1 y1 z1`
...
:math:`xkn ykn zkn`

where n, k1, kn, are integers and curve1, curve2, ..., curven are strings of characters. All coordinates are real numbers. 


.. topic:: documentation status:: in progress

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@inria.fr>, Dec 2009

    Documentation adapted from the AMAPmod user manual version 1.8.

