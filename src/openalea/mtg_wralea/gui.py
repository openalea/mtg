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


from openalea.visualea.node_widget import NodeWidget
from openalea.mtg.gui.mtg_editor import GraphicalMtgFactory, ObservableMTG

from qtpy import QtGui

class MTGEditor(QtGui.QWidget, NodeWidget):
    def __init__(self, node, parent):
        QtGui.QWidget.__init__(self, parent)
        NodeWidget.__init__(self, node)
        self.editor = GraphicalMtgFactory.create_view(None, parent=None)
        self.lay = QtGui.QVBoxLayout()
        self.lay.setSpacing(0)
        self.lay.setContentsMargins(0,0,0,0)
        self.lay.addWidget(self.editor)
        self.setLayout(self.lay)

    def notify(self, sender, event):
        """ Function called by observed objects """
        print(event)
        if event[0] == 'input_modified':
            if event[1] == 0:
                g = self.node.get_input(0)
                print(g)
                if self.editor.scene().get_graph() is None:
                    obsg = ObservableMTG(g)
                    self.editor.scene().set_graph(obsg)
                    self.editor.scene().initialise_from_model()
        else:
            NodeWidget.notify(self, sender, event)
