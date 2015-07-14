# Copyright (c) 2015 Ultimaker B.V.
# Uranium is released under the terms of the AGPLv3 or higher.

from UM.Event import MouseEvent, KeyEvent
from UM.Tool import Tool
from UM.Application import Application
from UM.Scene.BoxRenderer import BoxRenderer
from UM.Scene.RayRenderer import RayRenderer
from UM.Scene.Selection import Selection
from UM.Scene.Iterator.BreadthFirstIterator import BreadthFirstIterator

from PyQt5.QtGui import qAlpha, qRed, qGreen, qBlue

class SelectionTool(Tool):
    PixelSelectionMode = 1
    BoundingBoxSelectionMode = 2

    def __init__(self):
        super().__init__()

        self._scene = Application.getInstance().getController().getScene()
        self._renderer = Application.getInstance().getRenderer()

        self._selection_mode = self.PixelSelectionMode
        self._ctrl_is_active = None
    
    def checkModifierKeys(self, event):
        #checks for the press and release events of the modifier keys (shift and control)
        #sets the accompanying variabel ( _[key]_is_active) on true or false
        if event.type is KeyEvent.KeyPressEvent:
            if event.key == KeyEvent.ControlKey:
                self._ctrl_is_active = True
        if event.type is KeyEvent.KeyReleaseEvent:
            if  event.key == KeyEvent.ControlKey:
                self._ctrl_is_active = False

    def setSelectionMode(self, mode):
        self._selection_mode = mode

    def event(self, event):
        self.checkModifierKeys(event)
        if event.type == MouseEvent.MousePressEvent and MouseEvent.LeftButton in event.buttons:
            if self._selection_mode == self.PixelSelectionMode:
                self._pixelSelection(event)
            else:
                self._boundingBoxSelection(event)

        return False

    def _boundingBoxSelection(self, event):
        root = self._scene.getRoot()

        ray = self._scene.getActiveCamera().getRay(event.x, event.y)

        intersections = []
        for node in BreadthFirstIterator(root):
            if node.getSelectionMask() == self._selectionMask and not node.isLocked():
                intersection = node.getBoundingBox().intersectsRay(ray)
                if intersection:
                    intersections.append((node, intersection[0], intersection[1]))

        if intersections:
            intersections.sort(key=lambda k: k[1])

            node = intersections[0][0]
            if not Selection.isSelected(node):
                if not self._ctrl_is_active:
                    Selection.clear()
                Selection.add(node)
        else:
            Selection.clear()

    def _pixelSelection(self, event):
        pixel_id = self._renderer.getIdAtCoordinate(event.x, event.y)

        if not pixel_id:
            Selection.clear()
            return
        for node in BreadthFirstIterator(self._scene.getRoot()):
            if id(node) == pixel_id:
                
                if self._ctrl_is_active:
                    if Selection.isSelected(node):
                        if node.getParent():
                            if node.getParent().callDecoration("isGroup"):
                                Selection.remove(node.getParent())
                            else:
                                Selection.remove(node)
                    else: 
                        Selection.add(node)
                        if node.getParent():
                            if node.getParent().callDecoration("isGroup"):
                                Selection.add(node.getParent())
                            else:
                                Selection.add(node)
                else:
                    if not Selection.isSelected(node) or Selection.getCount() > 1:
                        Selection.clear()
                        if node.getParent():
                            if node.getParent().callDecoration("isGroup"):
                                Selection.add(node.getParent())
                            else: 
                                Selection.add(node)
