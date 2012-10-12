# -*- python -*-
#
#       Template grapheditor definitions for MTG Edition.
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from random import randint as rint
from math import sin, cos, radians

from openalea.grapheditor import *
from openalea.grapheditor.all import *
from openalea.grapheditor import qt
from openalea.core.observer import Observed

from openalea.mtg import MTG
from openalea.mtg import algo

###############################################################
###############################################################
# -- A wrapper around mtg.MTG that implements notification -- #
###############################################################

class ObservableMTG(GraphAdapterBase, Observed):
    """An adapter to vplants.newmtg.mtg.MTG. It has the role to
    add notifications to actions performed on the underlying graph"""
    def __init__(self, graph=None):
        GraphAdapterBase.__init__(self)
        Observed.__init__(self)
        self.set_graph(MTG() if graph is None else graph)

    def new_vertex(self, **kwargs):
        self.graph._id += 1
        id_ = self.graph._id
        self.add_vertex(id_, **kwargs)
        return id_

    def add_vertex(self, vid, **kwargs):
        vertex_added = [vid]
        edge_added=[]
        pid = kwargs.pop("parent", None)
        edge_type = kwargs.pop("edge_type", "<")
        g = self.graph
        if pid is None:
            vid = g.add_component(g.root, component_id=vid, **kwargs)
            edge_added.append((g.root, vid))
        else:
            if edge_type in ["<", "+"]:
                vid = g.add_child(pid, child=vid,edge_type=edge_type, **kwargs)
                edge_added.append((pid, vid))
            elif edge_type == "/":
                vid = g.add_component(pid, component_id=vid, **kwargs)
                edge_added.append((pid, vid))
            else: # add a complex
                cpx_id = g.complex(pid)
                if pid in g.component_roots(cpx_id):
                    g._id -= 1
                    return
                # TODO : What is the type of the edge?
                g.add_child(cpx_id, child=vid, **kwargs)
                g.add_component(vid, component_id=pid)
                edge_added.append((cpx_id, vid))
                edge_added.append((vid, pid))


        self.notify_listeners(("vertex_added", ("vertex",vid)))

        self.notify_edge_additions(edge_added)

    def remove_vertex(self, vertex):
        g = self.graph
        pid = g.parent(vertex)
        children = g.children(vertex)
        nchildren = len(children)

        # -- refresh the graphical edges to --
        # -- reparent children to parent of vertex --
        edges_to_remove = [(pid,vertex)]+ [None]*nchildren
        edges_to_add    = [None]*nchildren
        for n, cid in enumerate(children):
            edges_to_remove[n+1] = vertex, cid
            edges_to_add[n] = pid, cid
        self.notify_edge_removals(edges_to_remove)
        self.notify_edge_additions(edges_to_add)

        g.remove_vertex(vertex, reparent_child=True)
        self.notify_listeners(("vertex_removed", ("vertex",vertex)))

    def add_edge(self, src_vertex, tgt_vertex, **kwargs):
        """ This method should really do add edge operations on graph
        and do notifications. It acts as the translator for the view to the model
        If it only does notifications, better put those in another method."""
        pass

    def remove_edge(self, src_vertex, tgt_vertex):
        """ This method should really do remove edge operations on graph
        and do notifications. It acts as the translator for the view to the model
        If it only does notifications, better put those in another method."""
        pass

    def notify_edge_additions(self, edges):
        for edge in edges:
            src, tgt = edge
            self.notify_listeners(("edge_added", ("default", edge, src, tgt)))

    def notify_edge_removals(self, edges):
        for edge in edges:
            self.notify_listeners(("edge_removed", ("default",edge)))


    # def remove_edges(self, edges):
    #     GraphAdapterBase.remove_edges(self, (e for e in edges))






##############################################
##############################################
# -- The graphical part of the MTG editor -- #
##############################################
from PyQt4 import QtGui, QtCore

class Vertex( qt.DefaultGraphicalVertex ):
    max_scale = 6

    def __init__(self, *args, **kwargs):
        qt.DefaultGraphicalVertex.__init__(self, *args, **kwargs)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, True)
        self._label = QtGui.QGraphicsSimpleTextItem(self)

    def _mtg(self):
        return self.graph().graph
    mtg = property(_mtg)

    def initialise_from_model(self):
        """Responsible for building the vertex' appearance
        from the vertex model"""
        g = self.mtg

        # -- set the color based on the scale of this vertex and the HSV wheel--
        scale = g.scale(self.vertex())
        s = (scale%self.max_scale)/float(self.max_scale)
        color = QtGui.QColor.fromHsvF(s, 1,1)
        brush = QtGui.QBrush(color)
        self.setBrush(brush)
        self._label.setText(str(self.vertex()))
        self._label.setPos(self.boundingRect().center()- \
                           self._label.boundingRect().bottomRight()/2)

        # -- call to parent handles the position --
        qt.DefaultGraphicalVertex.initialise_from_model(self)
        self.select()

    def store_view_data(self, **kwargs):
        vid = self.vertex()
        self.mtg._add_vertex_properties(vid,kwargs)

    def get_view_data(self, key):
        vid = self.vertex()
        return self.mtg.property(key).get(vid)

    def default_position(self):
        """If there is no position obtained by get_view_data("position"),
        use the return value from this one"""
        return [rint(0,200)]*2

    def select(self):
        self.setFocus()
        self.scene().clearSelection()
        self.setSelected(True)

    ########################################################
    # The following methods are meant to modify the model! #
    ########################################################
    def add_child(self, *args, **kwargs):
        """ This methods modifies the mtg by adding a child to this vertex.
        The view will be updated through the graph's notifications.
        """
        gm = self.graph()
        x, y = self.get_view_data("position")
        edge_type =  kwargs.get("edge_type", "<")
        if edge_type in ["+","<"]:
            y -= 40
        elif edge_type in ["\\","/"]:
            pass #y==y

        if edge_type == "<":
            n = len(algo.sons(self.mtg, self.vertex(), EdgeType="<"))
            if n > 0: #there can only be one successor
                return
        elif edge_type == "+":
            children = algo.sons(self.mtg, self.vertex(), EdgeType="+")
            n = len(children)
            n = n if n < 60/30 else n+1
            angle = -60 + n*30
            x += sin(radians(angle))*80
        elif edge_type == "/":
            x += 200
        elif edge_type == "\\":
            x -= 200

        gm.new_vertex(parent=self.vertex(), position=[x,y], edge_type=edge_type )


    #######################################
    # Handle notifications from the model #
    #######################################
    def notify(self, sender, event):
        if event=="select":
            self.select()
        else:
            qt.DefaultGraphicalVertex.notify(self, sender, event)

    ##########################
    # Some Qt Event handling #
    ##########################
    def keyPressEvent(self, event):
        k = event.key()
        if k in [QtCore.Qt.Key_Up, QtCore.Qt.Key_Down,
                 QtCore.Qt.Key_Left, QtCore.Qt.Key_Right]:
            g = self.mtg
            vid = self.vertex()
            if k == QtCore.Qt.Key_Up:
                cpx_id = g.complex(vid)
                if cpx_id is not None:
                    self.graph().notify_listeners(("vertex_event", (cpx_id, "select")))
            elif k == QtCore.Qt.Key_Down:
                cids = g.components(vid)
                if len(cids) > 0:
                    self.graph().notify_listeners(("vertex_event", (cids[0], "select")))
            elif k == QtCore.Qt.Key_Left:
                pid = g.parent(vid)
                if pid is not None:
                    self.graph().notify_listeners(("vertex_event", (pid, "select")))
            else:
                chids = g.children(vid)
                for chid in chids:
                    if g.edge_type(chid) == "<":
                        self.graph().notify_listeners(("vertex_event", (chid, "select")))
                        break
                else:
                    if chids:
                        chid = chids[0]
                        self.graph().notify_listeners(("vertex_event", (chid, "select")))
        else:
            edge_type = "<"
            to_add = True
            if k == QtCore.Qt.Key_Less:
                edge_type="<"
            elif k == QtCore.Qt.Key_Plus :
                edge_type="+"
            elif k == QtCore.Qt.Key_Slash :
                edge_type="/"
            elif k == QtCore.Qt.Key_Backslash :
                edge_type="\\"
            elif k == QtCore.Qt.Key_Delete :
                to_add=False
            else:
                return
            event.accept()
            if to_add:
                self.add_child(edge_type=edge_type)
            else:
                self.graph().remove_vertex(self.vertex())




class MtgView( qt.View ):

    #########################
    # Handling mouse events #
    #########################
    def mouseDoubleClickEvent(self, event):
        qt.View.mouseDoubleClickEvent(self, event)
        self.dropHandler(event)

    def dropHandler(self, event):
        position = self.mapToScene(event.pos())
        position = [position.x(), position.y()]
        # -- the new_vertex call is forwarded to the graph or to the
        # -- graph_adapter if available with *args and **kwargs
        if self.scene().get_graph():
            self.scene().new_vertex(position=position)

    # -- implement this to customize mouse motion handler.
    # -- !!! Be sure to call the parent's implementation somewhere inside! --
    # def mouseMoveEvent(self, e):
    #     qt.View.mouseMoveEvent(self, e)

    # -- implement this to customize mouse button right click.
    # -- !!! Be sure to call the parent's implementation somewhere inside! --
    # def contextMenuEvent(self, event):
    #     QtGui.QGraphicsView.contextMenuEvent(self, event)


def initialise_graph_view_from_model(graphView, graphModel):
    """ This method must be implemented to correctly display
    the graphModel in the graphView. This basically means
    browsing the graph structure and issuing the notifications
    that allow to build the visual representation of the graph

    If you wonder why this is not a member of MtgView:
    1) It serves to initialise the scene, not the view. The view holds the scene.
       One scene can be viewed by many views.
    2) As a consequence, it should be a method of a qtgraphview.Scene subclass
       which is not meant to be used directly but rather through the strategy business.
       It is not meant to be subclassed either, although that is possible.
    3) If one would subclass qtgraphview.Scene, that person would need to subclass
       qtgraphview.QtGraphStrategyMaker.
    In the end it's just way easier to simply implement this function and declare it
    to the QtGraphStrategyMaker contructor.
    """
    g = graphModel.graph
    gm = graphModel
    print g, gm
    for v in g:
        gm.notify_listeners(("vertex_added", ("vertex", v)))






# -- This creates a GraphicalMtg factory, a class that creates views for MTGS --
GraphicalMtgFactory = qt.QtGraphStrategyMaker( 
    graphView = MtgView,
    vertexWidgetMap = {"vertex":Vertex},
    edgeWidgetMap = {
        "default":qt.DefaultGraphicalEdge,
        "floating-default":qt.DefaultGraphicalFloatingEdge },
    graphViewInitialiser = initialise_graph_view_from_model,
    )



if __name__ == "__main__":
    from random import randint as rint

    #THE APPLICATION'S MAIN WINDOW
    class MainWindow(QtGui.QMainWindow):
        def __init__(self, parent=None):
            """                """
            QtGui.QMainWindow.__init__(self, parent)

            self.setMinimumSize(800,600)
            self.__graph = ObservableMTG()
            self.__graphView = GraphicalMtgFactory.create_view(self.__graph, parent=self)

            self.setCentralWidget(self.__graphView)


    app = QtGui.QApplication(["GraphEditor and Mtg test"])
    QtGui.QApplication.processEvents()
    w = MainWindow()
    w.show()
    app.exec_()

