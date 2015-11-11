#
# AugmentedRealityNavigation
#
import os
import unittest
import logging
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *

### AugmentedRealityNavigation
class AugmentedRealityNavigation(ScriptedLoadableModule):

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "AugmentedRealityNavigation" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["David Garcia (Laboratorio de Imagen Medica (LIM))"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

### AugmentedRealityNavigationWidgety
class AugmentedRealityNavigationWidget(ScriptedLoadableModuleWidget):

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Loading models
    modelsCollapsibleButton = ctk.ctkCollapsibleButton()
    modelsCollapsibleButton.text = "Models"
    self.layout.addWidget(modelsCollapsibleButton)
    parametersFormLayout = qt.QFormLayout(modelsCollapsibleButton)

    # Load Models Button
    self.loadModelsButton = qt.QPushButton("Load models")
    self.loadModelsButton.toolTip = "Load saved models: Pointer, Applicator, and Tablet."
    self.loadModelsButton.enabled = True
    parametersFormLayout.addRow(self.loadModelsButton)
   
    # Skull model selector    
    self.tabletModelSelector = slicer.qMRMLNodeComboBox()
    self.tabletModelSelector.nodeTypes = ( ("vtkMRMLModelNode"), "" )
    self.tabletModelSelector.selectNodeUponCreation = True
    self.tabletModelSelector.addEnabled = False
    self.tabletModelSelector.removeEnabled = False
    self.tabletModelSelector.noneEnabled = False
    self.tabletModelSelector.showHidden = False
    self.tabletModelSelector.showChildNodeTypes = False
    self.tabletModelSelector.setMRMLScene( slicer.mrmlScene )
    self.tabletModelSelector.setToolTip( "Pick the tablet model." )
    parametersFormLayout.addRow("Tablet model: ", self.tabletModelSelector)
      
    # Skull Markers model selector
    self.applicatorModelSelector = slicer.qMRMLNodeComboBox()
    self.applicatorModelSelector.nodeTypes = ( ("vtkMRMLModelNode"), "" )
    self.applicatorModelSelector.selectNodeUponCreation = True
    self.applicatorModelSelector.addEnabled = False
    self.applicatorModelSelector.removeEnabled = False
    self.applicatorModelSelector.noneEnabled = False
    self.applicatorModelSelector.showHidden = False
    self.applicatorModelSelector.showChildNodeTypes = False
    self.applicatorModelSelector.setMRMLScene( slicer.mrmlScene )
    self.applicatorModelSelector.setToolTip( "Pick the applicator model." )
    parametersFormLayout.addRow("Applicator model: ", self.applicatorModelSelector)
    
    # Pointer model selector    
    self.pointerModelSelector = slicer.qMRMLNodeComboBox()
    self.pointerModelSelector.nodeTypes = ( ("vtkMRMLModelNode"), "" )
    self.pointerModelSelector.selectNodeUponCreation = True
    self.pointerModelSelector.addEnabled = False
    self.pointerModelSelector.removeEnabled = False
    self.pointerModelSelector.noneEnabled = False
    self.pointerModelSelector.showHidden = False
    self.pointerModelSelector.showChildNodeTypes = False
    self.pointerModelSelector.setMRMLScene( slicer.mrmlScene )
    self.pointerModelSelector.setToolTip( "Pick the pointer model." )
    parametersFormLayout.addRow("Pointer model: ", self.pointerModelSelector)
          
    # Transform Definition Area
    transformsCollapsibleButton = ctk.ctkCollapsibleButton()
    transformsCollapsibleButton.text = "Transforms"
    self.layout.addWidget(transformsCollapsibleButton)   
    parametersFormLayout = qt.QFormLayout(transformsCollapsibleButton)
    
    # TabletToTracker transform selector
    self.tabletToTrackerSelector = slicer.qMRMLNodeComboBox()
    self.tabletToTrackerSelector.nodeTypes = ( ("vtkMRMLLinearTransformNode"), "" )
    self.tabletToTrackerSelector.selectNodeUponCreation = True
    self.tabletToTrackerSelector.addEnabled = False
    self.tabletToTrackerSelector.removeEnabled = False
    self.tabletToTrackerSelector.noneEnabled = False
    self.tabletToTrackerSelector.showHidden = False
    self.tabletToTrackerSelector.showChildNodeTypes = False
    self.tabletToTrackerSelector.setMRMLScene( slicer.mrmlScene )
    self.tabletToTrackerSelector.setToolTip( "Pick the TabletToTracker transform." )
    parametersFormLayout.addRow("TabletToTracker transform: ", self.tabletToTrackerSelector)

    # ApplicatorToTracker transform selector
    self.applicatorToTrackerSelector = slicer.qMRMLNodeComboBox()
    self.applicatorToTrackerSelector.nodeTypes = ( ("vtkMRMLLinearTransformNode"), "" )
    self.applicatorToTrackerSelector.selectNodeUponCreation = True
    self.applicatorToTrackerSelector.addEnabled = False
    self.applicatorToTrackerSelector.removeEnabled = False
    self.applicatorToTrackerSelector.noneEnabled = False
    self.applicatorToTrackerSelector.showHidden = False
    self.applicatorToTrackerSelector.showChildNodeTypes = False
    self.applicatorToTrackerSelector.setMRMLScene( slicer.mrmlScene )
    self.applicatorToTrackerSelector.setToolTip( "Pick the ApplicatorToTracker transform." )
    parametersFormLayout.addRow("ApplicatorToTracker transform: ", self.applicatorToTrackerSelector)

    # PointerToTracker transform selector
    self.pointerToTrackerSelector = slicer.qMRMLNodeComboBox()
    self.pointerToTrackerSelector.nodeTypes = ( ("vtkMRMLLinearTransformNode"), "" )
    self.pointerToTrackerSelector.selectNodeUponCreation = True
    self.pointerToTrackerSelector.addEnabled = False
    self.pointerToTrackerSelector.removeEnabled = False
    self.pointerToTrackerSelector.noneEnabled = False
    self.pointerToTrackerSelector.showHidden = False
    self.pointerToTrackerSelector.showChildNodeTypes = False
    self.pointerToTrackerSelector.setMRMLScene( slicer.mrmlScene )
    self.pointerToTrackerSelector.setToolTip( "Pick the PointerToTracker transform." )
    parametersFormLayout.addRow("PointerToTracker transform: ", self.pointerToTrackerSelector)

    # Apply Transforms Button
    self.applyTransformsButton = qt.QPushButton("Apply Transforms")
    self.applyTransformsButton.toolTip = "Apply selected transforms."
    self.applyTransformsButton.enabled = False
    parametersFormLayout.addRow(self.applyTransformsButton)

    # Viewpoint Definition Area
    viewpointCollapsibleButton = ctk.ctkCollapsibleButton()
    viewpointCollapsibleButton.text = "Viewpoint"
    self.layout.addWidget(viewpointCollapsibleButton)   
    parametersFormLayout = qt.QFormLayout(viewpointCollapsibleButton)

    # Tablet Viewpoint Button
    self.tabletViewpointButton = qt.QPushButton("Tablet View")
    self.tabletViewpointButton.toolTip = "Apply tablet viewpoint."
    self.tabletViewpointButton.enabled = True
    parametersFormLayout.addRow(self.tabletViewpointButton)

    # Applicator Viewpoint Button
    self.applicatorViewpointButton = qt.QPushButton("Applicator View")
    self.applicatorViewpointButton.toolTip = "Apply applicator viewpoint."
    self.applicatorViewpointButton.enabled = True
    parametersFormLayout.addRow(self.applicatorViewpointButton)

     # Pointer Viewpoint Button
    self.pointerViewpointButton = qt.QPushButton("Pointer View")
    self.pointerViewpointButton.toolTip = "Apply pointer viewpoint."
    self.pointerViewpointButton.enabled = True
    parametersFormLayout.addRow(self.pointerViewpointButton)

     # connections    
    self.tabletToTrackerSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.applicatorToTrackerSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.pointerToTrackerSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.loadModelsButton.connect('clicked(bool)', self.onLoadModelsButtonClicked)
    self.applyTransformsButton.connect('clicked(bool)', self.onApplyTransformsClicked)
    self.tabletViewpointButton.connect('clicked(bool)', self.onTabletViewpointButtonClicked)
    self.applicatorViewpointButton.connect('clicked(bool)', self.onApplicatorViewpointButtonClicked)
    self.pointerViewpointButton.connect('clicked(bool)', self.onPointerViewpointButtonClicked)
        
    # Add vertical spacer
    self.layout.addStretch(1)
    
    # Refresh scene (you only need one function for this)
    self.onSelect()
    
  def cleanup(self):
    pass

  def onSelect(self):    
    self.applyTransformsButton.enabled = self.pointerToTrackerSelector.currentNode() and self.tabletToTrackerSelector.currentNode() and self.applicatorToTrackerSelector.currentNode()
    
  def onLoadModelsButtonClicked(self):
    logic = AugmentedRealityNavigationLogic()
    logic.LoadModels()    

  def onApplyTransformsClicked(self):
    self.applyTransformsButton.enabled = False
    self.pointerToTrackerSelector.enabled = False
    self.tabletToTrackerSelector.enabled = False
    self.applicatorToTrackerSelector.enabled = False
    logic = AugmentedRealityNavigationLogic()
    logic.buildTransformTree(self.pointerModelSelector.currentNode(), self.tabletModelSelector.currentNode(), self.applicatorModelSelector.currentNode(), self.pointerToTrackerSelector.currentNode(), self.tabletToTrackerSelector.currentNode(), self.applicatorToTrackerSelector.currentNode())

  def onTabletViewpointButtonClicked(self):
    logging.debug('SetTabletViewpoint')
    logic = AugmentedRealityNavigationLogic()
    logic.SetTabletViewpoint()
     
  def onApplicatorViewpointButtonClicked(self):
    logging.debug('SetApplicatorViewpoint')
    logic = AugmentedRealityNavigationLogic()
    logic.SetApplicatorViewpoint()
    
  def onPointerViewpointButtonClicked(self):
    logging.debug('SetPointerViewpoint')
    logic = AugmentedRealityNavigationLogic()
    logic.SetPointerViewpoint()

### AugmentedRealityNavigationLogic
class AugmentedRealityNavigationLogic(ScriptedLoadableModuleLogic):

  def __init__(self):
    import Viewpoint # Viewpoint Module must have been added to Slicer 
    self.viewpointLogic = Viewpoint.ViewpointLogic()

  def LoadModels(self):
    moduleDirectoryPath = slicer.modules.augmentedrealitynavigation.path.replace('AugmentedRealityNavigation.py', '')
    slicer.util.loadModel(qt.QDir.toNativeSeparators(moduleDirectoryPath + '../../Data/Models/TabletModel.stl'))
    slicer.util.loadModel(qt.QDir.toNativeSeparators(moduleDirectoryPath + '../../Data/Models/ApplicatorModel.stl'))
    slicer.util.loadModel(qt.QDir.toNativeSeparators(moduleDirectoryPath + '../../Data/Models/PointerModel.stl'))
    
  def buildTransformTree(self, pointerModelNode, tabletModelNode, applicatorModelNode, PointerToTrackerTransformNode, TabletToTrackerTransformNode, ApplicatorToTrackerTransformNode):
     
    # Build transform tree
    pointerModelNode.SetAndObserveTransformNodeID(PointerToTrackerTransformNode.GetID())
    tabletModelNode.SetAndObserveTransformNodeID(TabletToTrackerTransformNode.GetID())
    applicatorModelNode.SetAndObserveTransformNodeID(ApplicatorToTrackerTransformNode.GetID())
    

  def SetTabletViewpoint(self):
    pass

  def SetApplicatorViewpoint(self):
    pass

  def SetPointerViewpoint(self):
    pass

