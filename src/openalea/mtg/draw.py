# -*- python -*-
#
#       OpenAlea.mtg
#
#       Copyright 2014-2016 CIRAD - Inria
#
#       File author(s): Christophe Pradal <christophe.pradal.at.cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
"""
**********
Matplotlib
**********

Draw MTG with matplotlib.

See Also
--------

matplotlib: http://matplotlib.sourceforge.net/

"""

from openalea.mtg import layout

def draw(g, pos=None, ax=None, hold=None, ax_size=(0,0,1,1), **kwds):
    """Draw the graph g with Matplotlib.

    Draw the graph as a simple representation with no node
    labels or edge labels and using the full Matplotlib figure area
    and no axis labels by default.  See draw_mtg() for more
    full-featured drawing that allows title, axis labels etc.

    Parameters
    ----------
    g : graph
       A MTG graph

    pos : dictionary, optional
       A dictionary with nodes as keys and positions as values.
       If not specified a spring layout positioning will be computed.
       See mtg.layout for functions that compute node positions.

    ax : Matplotlib Axes object, optional
       Draw the graph in specified Matplotlib axes.

    hold : bool, optional
       Set the Matplotlib hold state.  If True subsequent draw
       commands will be added to the current axes.

    **kwds : optional keywords
       See draw.draw_mtg() for a description of optional keywords.

    Examples
    --------
    >>> g = om.random_mtg()
    >>> draw.draw(g)
    >>> draw.draw(g,pos=om.spring_layout(G)) # use spring layout

    See Also
    --------
    draw_mtg()
    draw_mtg_vertices()
    draw_mtg_edges()
    draw_mtg_labels()
    draw_mtg_edge_labels()

    Notes
    -----
    This function has the same name as pylab.draw and pyplot.draw
    so beware when using

    >>> from openalea.mtg.draw import *

    since you might overwrite the pylab.draw function.

    With pyplot use

    >>> import matplotlib.pyplot as plt
    >>> import openalea.mtg as om
    >>> g=om.random_mtg()
    >>> om.draw(g)  # mtg draw()
    >>> plt.draw()  # pyplot draw()

    Also see the openalea.mtg drawing examples at
    openalea gallery.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("Matplotlib required for draw()")
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    if ax is None:
        cf = plt.gcf()
    else:
        cf = ax.get_figure()
    cf.set_facecolor('w')
    if ax is None:
        if cf._axstack() is None:
            ax=cf.add_axes(ax_size)
        else:
            ax=cf.gca()

 # allow callers to override the hold state by passing hold=True|False
    b = plt.ishold()
    h = kwds.pop('hold', None)
    if h is not None:
        plt.hold(h)
    try:
        draw_mtg(g, pos=pos,ax=ax,**kwds)
        ax.set_axis_off()
        plt.draw_if_interactive()
    except:
        plt.hold(b)
        raise
    plt.hold(b)
    return

def draw_mtg(G, pos=None, with_labels=True, with_edge_labels=False, **kwds):
    """Draw the graph G using Matplotlib.

    Draw the graph with Matplotlib with options for node positions,
    labeling, titles, and many other drawing features.
    See draw() for simple drawing without labels or axes.

    Parameters
    ----------
    G : graph
       A MTG graph

    pos : dictionary, optional
       A dictionary with nodes as keys and positions as values.
       If not specified a spring layout positioning will be computed.
       See MTG.layout for functions that compute vertex positions.

    with_labels :  bool, optional (default=True)
       Set to True to draw labels on the nodes.

    ax : Matplotlib Axes object, optional
       Draw the graph in the specified Matplotlib axes.

    nodelist : list, optional (default G.nodes())
       Draw only specified nodes

    edgelist : list, optional (default=G.edges())
       Draw only specified edges

    node_size : scalar or array, optional (default=300)
       Size of nodes.  If an array is specified it must be the
       same length as nodelist.

    node_color : color string, or array of floats, (default='r')
       Node color. Can be a single color format string,
       or a  sequence of colors with the same length as nodelist.
       If numeric values are specified they will be mapped to
       colors using the cmap and vmin,vmax parameters.  See
       matplotlib.scatter for more details.

    node_shape :  string, optional (default='o')
       The shape of the node.  Specification is as matplotlib.scatter
       marker, one of 'so^>v<dph8'.

    alpha : float, optional (default=1.0)
       The node transparency

    cmap : Matplotlib colormap, optional (default=None)
       Colormap for mapping intensities of nodes

    vmin,vmax : float, optional (default=None)
       Minimum and maximum for node colormap scaling

    linewidths : [None | scalar | sequence]
       Line width of symbol border (default =1.0)

    width : float, optional (default=1.0)
       Line width of edges

    edge_color : color string, or array of floats (default='r')
       Edge color. Can be a single color format string,
       or a sequence of colors with the same length as edgelist.
       If numeric values are specified they will be mapped to
       colors using the edge_cmap and edge_vmin,edge_vmax parameters.

    edge_ cmap : Matplotlib colormap, optional (default=None)
       Colormap for mapping intensities of edges

    edge_vmin,edge_vmax : floats, optional (default=None)
       Minimum and maximum for edge colormap scaling

    style : string, optional (default='solid')
       Edge line style (solid|dashed|dotted,dashdot)

    labels : dictionary, optional (default=None)
       Node labels in a dictionary keyed by node of text labels

    font_size : int, optional (default=12)
       Font size for text labels

    font_color : string, optional (default='k' black)
       Font color string

    font_weight : string, optional (default='normal')
       Font weight

    font_family : string, optional (default='sans-serif')
       Font family

    label : string, optional
        Label for graph legend

    Examples
    --------
    >>> g = om.random_mtg()
    >>> om.draw(g)
    >>> om.draw(g, pos=om.spring_layout(g)) # use spring layout

    >>> import matplotlib.pyplot as plt
    >>> limits=plt.axis('off') # turn of axis



    See Also
    --------
    draw()
    draw_mtg_vertices()
    draw_mtg_edges()
    draw_mtg_labels()
    draw_mtg_edge_labels()
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("Matplotlib required for draw()")
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    if pos is None:
        g=layout.simple_layout(G)
        pos = g.property('position')

    node_collection=draw_mtg_vertices(G, pos, **kwds)
    edge_collection=draw_mtg_edges(G, pos, **kwds)

    if with_labels:
        draw_mtg_labels(G, pos, **kwds)

    if with_edge_labels:
        draw_mtg_edge_labels(G, pos, **kwds)

    plt.draw_if_interactive()

def draw_mtg_vertices(g, pos,
					nodelist=None,
					node_size=300,
					node_color='r',
					node_shape='o',
					alpha=1.0,
					cmap=None,
					vmin=None,
					vmax=None,
					ax=None,
					linewidths=None,
					label=None,
					**kwds):
    """Draw the nodes of the graph G.

	This draws only the nodes of the graph G.

	Parameters
	----------
	G : graph
		A MTG graph

	pos : dictionary
		A dictionary with nodes as keys and positions as values.
		Positions should be sequences of length 2.

	ax : Matplotlib Axes object, optional
		Draw the graph in the specified Matplotlib axes.

	nodelist : list, optional
		Draw only specified nodes (default G.nodes())

	node_size : scalar or array
		Size of nodes (default=300). If an array is specified it must be the
		same length as nodelist.

	node_color : color string, or array of floats
		Node color. Can be a single color format string (default='r'),
		or a sequence of colors with the same length as nodelist.
		If numeric values are specified they will be mapped to
		colors using the cmap and vmin,vmax parameters. See
		matplotlib.scatter for more details.

	node_shape : string
		The shape of the node. Specification is as matplotlib.scatter
		marker, one of 'so^>v<dph8' (default='o').

	alpha : float
		The node transparency (default=1.0)

	cmap : Matplotlib colormap
		Colormap for mapping intensities of nodes (default=None)

	vmin,vmax : floats
		Minimum and maximum for node colormap scaling (default=None)

	linewidths : [None | scalar | sequence]
		Line width of symbol border (default =1.0)

	label : [None| string]
		Label for legend

	Returns
	-------
	matplotlib.collections.PathCollection
		`PathCollection` of the nodes.

	Examples
	--------
	>>> g = MTG()
	>>> vid = g.add_component(g.root)
	>>> random_tree(g, vid)
	>>> nodes=om.draw_mtg_vertices(G,pos=om.spring_layout(G))


	See Also
	--------
	draw()
	draw_mtg_vertices()
	draw_mtg_edges()
	draw_mtg_labels()
	draw_mtg_edge_labels()
	"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.cbook as cb
        import numpy
    except ImportError:
        raise ImportError("Matplotlib required for draw()")
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    if ax is None:
        ax = plt.gca()

    if nodelist is None:
        nodelist = g.vertices(scale=g.max_scale())

    if not nodelist or len(nodelist) == 0: # empty nodelist, no drawing
        return None

    if not cb.is_string_like(node_shape) and cb.iterable(node_shape):
        shapes = list(set(node_shape))
        for sh in shapes:
            sh_index = [i for i, nsh in enumerate(node_shape) if nsh == sh]
            sh_nodelist = [ nodelist[i] for i in sh_index ]
            sh_node_color = node_color
            if not cb.is_string_like(sh_node_color) and cb.iterable(sh_node_color):
                sh_node_color = [ sh_node_color[i] for i in sh_index ]
            sh_node_size = node_size
            if not cb.is_string_like(sh_node_size) and cb.iterable(sh_node_size):
                sh_node_size = [ sh_node_size[i] for i in sh_index ]

            xy = numpy.asarray([pos[v] for v in sh_nodelist])

            node_collection = ax.scatter(xy[:, 0], xy[:, 1],
                                         s=sh_node_size,
                                         c=sh_node_color,
                                         marker=sh,
                                         cmap=cmap,
                                         vmin=vmin,
                                         vmax=vmax,
                                         alpha=alpha,
                                         linewidths=linewidths,
                                         label=label)

            node_collection.set_zorder(2)
        return node_collection

    # else

    try:
        xy = numpy.asarray([pos[v] for v in nodelist])
    except KeyError as e:
        raise Exception('Node %s has no position.'%e)
    except ValueError:
        raise Exception('Bad value in node positions.')

    node_collection = ax.scatter(xy[:, 0], xy[:, 1],
                                 s=node_size,
                                 c=node_color,
                                 marker=node_shape,
                                 cmap=cmap,
                                 vmin=vmin,
                                 vmax=vmax,
                                 alpha=alpha,
                                 linewidths=linewidths,
                                 label=label)

    node_collection.set_zorder(2)
    return node_collection

def draw_mtg_edges(g, pos,
                        edgelist=None,
                        width=1.0,
                        edge_color='k',
                        style='solid',
                        alpha=None,
                        edge_cmap=None,
                        edge_vmin=None,
                        edge_vmax=None,
                        ax=None,
                        arrows=True,
                        label=None,
                        **kwds):
    """Draw the edges of the graph g.

    This draws only the edges of the graph g.

    Parameters
    ----------
    g : graph
       A MTG graph

    pos : dictionary
       A dictionary with nodes as keys and positions as values.
       If not specified a spring layout positioning will be computed.
       See mtg.layout for functions that compute node positions.

    edgelist : collection of edge tuples
       Draw only specified edges(default=G.edges())

    width : float
       Line width of edges (default =1.0)

    edge_color : color string, or array of floats
       Edge color. Can be a single color format string (default='r'),
       or a sequence of colors with the same length as edgelist.
       If numeric values are specified they will be mapped to
       colors using the edge_cmap and edge_vmin,edge_vmax parameters.

    style : string
       Edge line style (default='solid') (solid|dashed|dotted,dashdot)

    alpha : float
       The edge transparency (default=1.0)

    edge_ cmap : Matplotlib colormap
       Colormap for mapping intensities of edges (default=None)

    edge_vmin,edge_vmax : floats
       Minimum and maximum for edge colormap scaling (default=None)

    ax : Matplotlib Axes object, optional
       Draw the graph in the specified Matplotlib axes.

    arrows : bool, optional (default=True)
       For directed graphs, if True draw arrowheads.

    label : [None| string]
       Label for legend

    Notes
    -----
    For directed graphs, "arrows" (actually just thicker stubs) are drawn
    at the head end.  Arrows can be turned off with keyword arrows=False.
    Yes, it is ugly but drawing proper arrows with Matplotlib this
    way is tricky.

    Examples
    --------
    >>> g = om.random_mtg()
    >>> edges = om.draw_mtg_edges(g, pos=om.simple_layout(G))


    See Also
    --------
    draw()
    draw_mtg()
    draw_mtg_vertices()
    draw_mtg_labels()
    draw_mtg_edge_labels()

    """
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        import matplotlib.cbook as cb
        from matplotlib.colors import colorConverter,Colormap
        from matplotlib.collections import LineCollection
        import numpy
    except ImportError:
        raise ImportError("Matplotlib required for draw()")
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    if ax is None:
        ax=plt.gca()

    if edgelist is None:
        edgelist=g.edges(scale=g.max_scale())

    if not edgelist or len(edgelist)==0: # no edges!
        return None

    # set edge positions
    edge_pos=numpy.asarray([(pos[e[0]],pos[e[1]]) for e in edgelist])

    if not cb.iterable(width):
        lw = (width,)
    else:
        lw = width

    if not cb.is_string_like(edge_color) \
           and cb.iterable(edge_color) \
           and len(edge_color)==len(edge_pos):
        if numpy.alltrue([cb.is_string_like(c)
                         for c in edge_color]):
            # (should check ALL elements)
            # list of color letters such as ['k','r','k',...]
            edge_colors = tuple([colorConverter.to_rgba(c,alpha)
                                 for c in edge_color])
        elif numpy.alltrue([not cb.is_string_like(c)
                           for c in edge_color]):
            # If color specs are given as (rgb) or (rgba) tuples, we're OK
            if numpy.alltrue([cb.iterable(c) and len(c) in (3,4)
                             for c in edge_color]):
                edge_colors = tuple(edge_color)
            else:
                # numbers (which are going to be mapped with a colormap)
                edge_colors = None
        else:
            raise ValueError('edge_color must consist of either color names or numbers')
    else:
        if cb.is_string_like(edge_color) or len(edge_color)==1:
            edge_colors = ( colorConverter.to_rgba(edge_color, alpha), )
        else:
            raise ValueError('edge_color must be a single color or list of exactly m colors where m is the number or edges')

    edge_collection = LineCollection(edge_pos,
                                     colors       = edge_colors,
                                     linewidths   = lw,
                                     antialiaseds = (1,),
                                     linestyle    = style,
                                     transOffset = ax.transData,
                                     )


    edge_collection.set_zorder(1) # edges go behind nodes
    edge_collection.set_label(label)
    ax.add_collection(edge_collection)

    # Note: there was a bug in mpl regarding the handling of alpha values for
    # each line in a LineCollection.  It was fixed in matplotlib in r7184 and
    # r7189 (June 6 2009).  We should then not set the alpha value globally,
    # since the user can instead provide per-edge alphas now.  Only set it
    # globally if provided as a scalar.
    if cb.is_numlike(alpha):
        edge_collection.set_alpha(alpha)

    if edge_colors is None:
        if edge_cmap is not None:
            assert(isinstance(edge_cmap, Colormap))
        edge_collection.set_array(numpy.asarray(edge_color))
        edge_collection.set_cmap(edge_cmap)
        if edge_vmin is not None or edge_vmax is not None:
            edge_collection.set_clim(edge_vmin, edge_vmax)
        else:
            edge_collection.autoscale()

    arrow_collection=None

    if arrows:

        # a directed graph hack
        # draw thick line segments at head end of edge
        # waiting for someone else to implement arrows that will work
        arrow_colors = edge_colors
        a_pos=[]
        p=1.0-0.25 # make head segment 25 percent of edge length
        for src,dst in edge_pos:
            x1,y1=src
            x2,y2=dst
            dx=x2-x1 # x offset
            dy=y2-y1 # y offset
            d=numpy.sqrt(float(dx**2+dy**2)) # length of edge
            if d==0: # source and target at same position
                continue
            if dx==0: # vertical edge
                xa=x2
                ya=dy*p+y1
            if dy==0: # horizontal edge
                ya=y2
                xa=dx*p+x1
            else:
                theta=numpy.arctan2(dy,dx)
                xa=p*d*numpy.cos(theta)+x1
                ya=p*d*numpy.sin(theta)+y1

            a_pos.append(((xa,ya),(x2,y2)))

        arrow_collection = LineCollection(a_pos,
                                colors       = arrow_colors,
                                linewidths   = [4*ww for ww in lw],
                                antialiaseds = (1,),
                                transOffset = ax.transData,
                                )

        arrow_collection.set_zorder(1) # edges go behind nodes
        arrow_collection.set_label(label)
        ax.add_collection(arrow_collection)


    # update view
    miom = numpy.amin(numpy.ravel(edge_pos[:,:,0]))
    maxx = numpy.amax(numpy.ravel(edge_pos[:,:,0]))
    miny = numpy.amin(numpy.ravel(edge_pos[:,:,1]))
    maxy = numpy.amax(numpy.ravel(edge_pos[:,:,1]))

    w = maxx-miom
    h = maxy-miny
    padx, pady = 0.05*w, 0.05*h
    corners = (miom-padx, miny-pady), (maxx+padx, maxy+pady)
    ax.update_datalim( corners)
    ax.autoscale_view()

#    if arrow_collection:

    return edge_collection

def draw_mtg_labels(G, pos,
                         nodelist = None,
                         labels=None,
                         font_size=12,
                         font_color='k',
                         font_family='sans-serif',
                         font_weight='normal',
                         alpha=1.0,
                         ax=None,
                         **kwds):
    """Draw node labels on the graph G.

    Parameters
    ----------
    G : graph
       A MTG graph

    pos : dictionary, optional
       A dictionary with nodes as keys and positions as values.
       If not specified a spring layout positioning will be computed.
       See mtg.layout for functions that compute node positions.

    labels : dictionary, optional (default=None)
       Node labels in a dictionary keyed by node of text labels

    font_size : int
       Font size for text labels (default=12)

    font_color : string
       Font color string (default='k' black)

    font_family : string
       Font family (default='sans-serif')

    font_weight : string
       Font weight (default='normal')

    alpha : float
       The text transparency (default=1.0)

    ax : Matplotlib Axes object, optional
       Draw the graph in the specified Matplotlib axes.


    Examples
    --------
    >>> G=om.dodecahedral_graph()
    >>> labels=om.draw_mtg_labels(G,pos=om.spring_layout(G))

    Also see the MTG drawing examples at
    gallery.html


    See Also
    --------
    draw()
    draw_mtg()
    draw_mtg_vertices()
    draw_mtg_edges()
    draw_mtg_labels()
    draw_mtg_edge_labels()

    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.cbook as cb
    except ImportError:
        raise ImportError("Matplotlib required for draw()")
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    if ax is None:
        ax=plt.gca()

    if labels is None:
        if nodelist is None:
            nodelist = G.vertices(scale=G.max_scale())
        labels=dict( (n,n) for n in nodelist)

    # set optional alignment
    horizontalalignment=kwds.get('horizontalalignment','center')
    verticalalignment=kwds.get('verticalalignment','center')

    text_items={}  # there is no text collection so we'll fake one
    for n, label in labels.items():
        (x,y)=pos[n]
        if not cb.is_string_like(label):
            label=str(label) # this will cause "1" and 1 to be labeled the same
        t=ax.text(x, y,
                  label,
                  size=font_size,
                  color=font_color,
                  family=font_family,
                  weight=font_weight,
                  horizontalalignment=horizontalalignment,
                  verticalalignment=verticalalignment,
                  transform = ax.transData,
                  clip_on=True,
                  )
        text_items[n]=t

    return text_items

def draw_mtg_edge_labels(G, pos,
                              edge_labels=None,
                              label_pos=0.5,
                              font_size=10,
                              font_color='k',
                              font_family='sans-serif',
                              font_weight='normal',
                              alpha=.5,
                              bbox=None,
                              ax=None,
                              rotate=False,
                              **kwds):
    """Draw edge labels.

    Parameters
    ----------
    G : graph
       A MTG graph

    pos : dictionary, optional
       A dictionary with nodes as keys and positions as values.
       If not specified a spring layout positioning will be computed.
       See mtg.layout for functions that compute node positions.

    ax : Matplotlib Axes object, optional
       Draw the graph in the specified Matplotlib axes.

    alpha : float
       The text transparency (default=1.0)

    edge_labels : dictionary
       Edge labels in a dictionary keyed by edge two-tuple of text
       labels (default=None). Only labels for the keys in the dictionary
       are drawn.

    label_pos : float
       Position of edge label along edge (0=head, 0.5=center, 1=tail)

    font_size : int
       Font size for text labels (default=12)

    font_color : string
       Font color string (default='k' black)

    font_weight : string
       Font weight (default='normal')

    font_family : string
       Font family (default='sans-serif')

    bbox : Matplotlib bbox
       Specify text box shape and colors.

    clip_on : bool
       Turn on clipping at axis boundaries (default=True)

    Examples
    --------
    >>> G=om.random_graph()
    >>> edge_labels=om.draw_mtg_edge_labels(G,pos=om.layout.spring_layout(G))

    Also see the MTG drawing examples at
    gallery

    See Also
    --------
    draw()
    draw_mtg()
    draw_mtg_vertices()
    draw_mtg_edges()
    draw_mtg_labels()
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.cbook as cb
        import numpy
    except ImportError:
        raise ImportError("Matplotlib required for draw()")
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    if ax is None:
        ax=plt.gca()
    if edge_labels is None:
        labels=dict( ((u,v), G.edge_type(v)) for u,v in G.edges(scale=G.max_scale()) )
    else:
        labels = edge_labels
    text_items={}
    for (n1,n2), label in labels.items():
        (x1,y1)=pos[n1]
        (x2,y2)=pos[n2]
        (x,y) = (x1 * label_pos + x2 * (1.0 - label_pos),
                 y1 * label_pos + y2 * (1.0 - label_pos))

        if rotate:
            angle=numpy.arctan2(y2-y1,x2-x1)/(2.0*numpy.pi)*360 # degrees
            # make label orientation "right-side-up"
            if angle > 90:
                angle-=180
            if angle < - 90:
                angle+=180
            # transform data coordinate angle to screen coordinate angle
            xy=numpy.array((x,y))
            trans_angle=ax.transData.transform_angles(numpy.array((angle,)),
                                                      xy.reshape((1,2)))[0]
        else:
            trans_angle=0.0
        # use default box of white with white border
        if bbox is None:
            bbox = dict(boxstyle='round',
                        ec=(1.0, 1.0, 1.0),
                        fc=(1.0, 1.0, 1.0),
                        )
        if not cb.is_string_like(label):
            label=str(label) # this will cause "1" and 1 to be labeled the same

        # set optional alignment
        horizontalalignment=kwds.get('horizontalalignment','center')
        verticalalignment=kwds.get('verticalalignment','center')

        t=ax.text(x, y,
                  label,
                  size=font_size,
                  color=font_color,
                  family=font_family,
                  weight=font_weight,
                  horizontalalignment=horizontalalignment,
                  verticalalignment=verticalalignment,
                  rotation=trans_angle,
                  transform = ax.transData,
                  bbox = bbox,
                  zorder = 2,
                  clip_on=True,
                  alpha=alpha,
                  )
        text_items[(n1,n2)]=t

    return text_items
