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

    self.AugmentedRealityNavigationLogic = AugmentedRealityNavigationLogic()

    myModuleDataPath = slicer.modules.augmentedrealitynavigation.path.replace("AugmentedRealityNavigation.py","") + 'Resources/Data/Models/'
        
    # Load Patient Model
    self.patientModel = slicer.util.getNode('PatientModel')
    if not self.patientModel:
        slicer.util.loadModel(myModuleDataPath + 'PatientModel.stl')
        self.patientModel = slicer.util.getNode(pattern="PatientModel")
        self.patientModelDisplay=self.patientModel.GetModelDisplayNode()
        self.patientModelDisplay.SetColor([1,0.7,0.53])

    # Load Tablet Model
    self.tabletModel = slicer.util.getNode('TabletModel')
    if not self.tabletModel:
        slicer.util.loadModel(myModuleDataPath + 'TabletModel.stl')
        self.tabletModel = slicer.util.getNode(pattern="TabletModel")
        self.tabletModelDisplay=self.tabletModel.GetModelDisplayNode()
        self.tabletModelDisplay.SetColor([1,0.7,0.53])

    # Load Pointer Model
    self.pointerModel = slicer.util.getNode('PointerModel')
    if not self.pointerModel:
        slicer.util.loadModel(myModuleDataPath + 'PointerModel.stl')
        self.pointerModel = slicer.util.getNode(pattern="PointerModel")
        self.pointerModelDisplay=self.pointerModel.GetModelDisplayNode()
        self.pointerModelDisplay.SetColor([1,0.7,0.53])
          
    # Transform Definition Area
    transformsCollapsibleButton = ctk.ctkCollapsibleButton()
    transformsCollapsibleButton.text = "Transforms"
    self.layout.addWidget(transformsCollapsibleButton)   
    parametersFormLayout = qt.QFormLayout(transformsCollapsibleButton)
    
    # TabletToTracker transform 
    self.tabletToTrackerTransform = slicer.util.getNode('Tracker')
    if not self.tabletToTrackerTransform:
      print('ERROR: tabletToTracker transform node was not found')

    # referenceToTracker transform 
    self.referenceToTrackerTransform = slicer.util.getNode('referenceToTracker')
    if not self.referenceToTrackerTransform:
      print('ERROR: referenceToTracker transform node was not found')

    # PointerToTracker transform 
    self.pointerToTrackerTransform = slicer.util.getNode('pointerToTracker')
    if not self.pointerToTrackerTransform:
      print('ERROR: pointerToTracker transform node was not found')

    # PatientToReference transform selector    
    self.patientToReferenceSelector = slicer.qMRMLNodeComboBox()
    self.patientToReferenceSelector.nodeTypes = ( ("vtkMRMLLinearTransformNode"), "" )
    self.patientToReferenceSelector.selectNodeUponCreation = True
    self.patientToReferenceSelector.addEnabled = False
    self.patientToReferenceSelector.removeEnabled = False
    self.patientToReferenceSelector.noneEnabled = False
    self.patientToReferenceSelector.showHidden = False
    self.patientToReferenceSelector.showChildNodeTypes = False
    self.patientToReferenceSelector.setMRMLScene( slicer.mrmlScene )
    self.patientToReferenceSelector.setToolTip( "Pick the patientToReference transform (output of fiducial registration)." )
    parametersFormLayout.addRow("patientToReference transform: ", self.patientToReferenceSelector)

    # TabletModelToTablet transform selector    
    self.tabletModelToTabletSelector = slicer.qMRMLNodeComboBox()
    self.tabletModelToTabletSelector.nodeTypes = ( ("vtkMRMLLinearTransformNode"), "" )
    self.tabletModelToTabletSelector.selectNodeUponCreation = True
    self.tabletModelToTabletSelector.addEnabled = False
    self.tabletModelToTabletSelector.removeEnabled = False
    self.tabletModelToTabletSelector.noneEnabled = False
    self.tabletModelToTabletSelector.showHidden = False
    self.tabletModelToTabletSelector.showChildNodeTypes = False
    self.tabletModelToTabletSelector.setMRMLScene( slicer.mrmlScene )
    self.tabletModelToTabletSelector.setToolTip( "Pick the tabletModelToTablet transform (output of fiducial registration)." )
    parametersFormLayout.addRow("tabletModelToTablet transform: ", self.tabletModelToTabletSelector)

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
    self.tabletViewpointButton = qt.QPushButton()
    self.tabletViewpointButton.toolTip = "Apply Tablet viewpoint."
    self.tabletViewpointButton.enabled = True
    self.enableTabletViewpointButtonState = 0
    self.enableTabletViewpointButtonTextState0 = "Enable Tablet Viewpoint Mode"
    self.enableTabletViewpointButtonTextState1 = "Disable Tablet Viewpoint Mode"
    self.tabletViewpointButton.setText(self.enableTabletViewpointButtonTextState0)
    parametersFormLayout.addRow(self.tabletViewpointButton)

    # Patient Viewpoint Button
    self.patientViewpointButton = qt.QPushButton()
    self.patientViewpointButton.toolTip = "Apply Patient viewpoint."
    self.patientViewpointButton.enabled = True
    self.enablePatientViewpointButtonState = 0
    self.enablePatientViewpointButtonTextState0 = "Enable Patient Viewpoint Mode"
    self.enablePatientViewpointButtonTextState1 = "Disable Patient Viewpoint Mode"
    self.patientViewpointButton.setText(self.enablePatientViewpointButtonTextState0)
    parametersFormLayout.addRow(self.patientViewpointButton)

    # Pointer Viewpoint Button
    self.pointerViewpointButton = qt.QPushButton()
    self.pointerViewpointButton.toolTip = "Apply Pointer viewpoint."
    self.pointerViewpointButton.enabled = True
    self.enablePointerViewpointButtonState = 0
    self.enablePointerViewpointButtonTextState0 = "Enable Pointer Viewpoint Mode"
    self.enablePointerViewpointButtonTextState1 = "Disable Pointer Viewpoint Mode"
    self.pointerViewpointButton.setText(self.enablePointerViewpointButtonTextState0)
    parametersFormLayout.addRow(self.pointerViewpointButton)

    # connections    
    self.patientToReferenceSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.tabletModelToTabletSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.applyTransformsButton.connect('clicked(bool)', self.onApplyTransformsClicked)
    self.tabletViewpointButton.connect('clicked(bool)', self.onTabletViewpointButtonClicked)
    self.patientViewpointButton.connect('clicked(bool)', self.onPatientViewpointButtonClicked)
    self.pointerViewpointButton.connect('clicked(bool)', self.onPointerViewpointButtonClicked)
        
    # Add vertical spacer
    self.layout.addStretch(1)
    
    # Refresh scene (you only need one function for this)
    self.onSelect()
    
  def cleanup(self):
    pass

  def onSelect(self):    
    self.applyTransformsButton.enabled = self.patientToReferenceSelector.currentNode() and self.tabletModelToTabletSelector.currentNode() 

  def onApplyTransformsClicked(self):
    self.applyTransformsButton.enabled = False
    self.patientToReferenceSelector.enabled = False
    self.tabletModelToTabletSelector.enabled = False
    self.AugmentedRealityNavigationLogic.buildTransformTree(self.pointerModel, self.tabletModel, self.patientModel, self.pointerToTrackerTransform, self.tabletToTrackerTransform, self.referenceToTrackerTransform, self.patientToReferenceSelector.currentNode(), self.tabletModelToTabletSelector.currentNode())
  
  def onTabletViewpointButtonClicked(self):
    logging.debug('SetTabletViewpoint')
    
    if self.enableTabletViewpointButtonState == 0:
          self.AugmentedRealityNavigationLogic.SetTabletViewpoint(self.tabletModel, self.tabletModelToTabletSelector.currentNode())
          self.AugmentedRealityNavigationLogic.StartViewpoint()
          self.enableTabletViewpointButtonState = 1
          self.tabletViewpointButton.setText(self.enableTabletViewpointButtonTextState1)
    else: 
          self.AugmentedRealityNavigationLogic.StopViewpoint()
          self.enableTabletViewpointButtonState = 0
          self.tabletViewpointButton.setText(self.enableTabletViewpointButtonTextState0)
     
  def onPatientViewpointButtonClicked(self):
    logging.debug('SetPatientViewpoint')
    
    if self.enablePatientViewpointButtonState == 0:
          self.AugmentedRealityNavigationLogic.SetPatientViewpoint(self.patientModel, self.patientToReferenceSelector.currentNode())
          self.AugmentedRealityNavigationLogic.StartViewpoint()
          self.enablePatientViewpointButtonState = 1
          self.patientViewpointButton.setText(self.enablePatientViewpointButtonTextState1)
    else: 
          self.AugmentedRealityNavigationLogic.StopViewpoint()
          self.enablePatientViewpointButtonState = 0
          self.patientViewpointButton.setText(self.enablePatientViewpointButtonTextState0)
    
  def onPointerViewpointButtonClicked(self):
    logging.debug('SetPointerViewpoint')
    
    if self.enablePointerViewpointButtonState == 0:
          self.AugmentedRealityNavigationLogic.SetPointerViewpoint(self.pointerModel, self.pointerToTrackerTransform)
          self.AugmentedRealityNavigationLogic.StartViewpoint()
          self.enablePointerViewpointButtonState = 1
          self.pointerViewpointButton.setText(self.enablePointerViewpointButtonTextState1)
    else: 
          self.AugmentedRealityNavigationLogic.StopViewpoint()
          self.enablePointerViewpointButtonState = 0
          self.pointerViewpointButton.setText(self.enablePointerViewpointButtonTextState0)

  
### AugmentedRealityNavigationLogic
class AugmentedRealityNavigationLogic(ScriptedLoadableModuleLogic):

  def __init__(self):
    import Viewpoint # Viewpoint Module must have been added to Slicer 
    self.viewpointLogic = Viewpoint.ViewpointLogic()

    # Camera transformations
    self.pointerCameraToPointer = slicer.util.getNode('pointerCameraToPointer')
    if not self.pointerCameraToPointer:
      self.pointerCameraToPointer=slicer.vtkMRMLLinearTransformNode()
      self.pointerCameraToPointer.SetName("pointerCameraToPointer")
      m = vtk.vtkMatrix4x4()
      m.SetElement( 0, 0, 1 ) # Row 1
      m.SetElement( 0, 1, 0 )
      m.SetElement( 0, 2, 0 )
      m.SetElement( 0, 3, 0 )      
      m.SetElement( 1, 0, 0 )  # Row 2
      m.SetElement( 1, 1, 1 )
      m.SetElement( 1, 2, 0 )
      m.SetElement( 1, 3, 0 )       
      m.SetElement( 2, 0, 0 )  # Row 3
      m.SetElement( 2, 1, 0 )
      m.SetElement( 2, 2, 1 )
      m.SetElement( 2, 3, 0 )
      self.pointerCameraToPointer.SetMatrixTransformToParent(m)
      slicer.mrmlScene.AddNode(self.pointerCameraToPointer)

    self.tabletCameraToTablet = slicer.util.getNode('tabletCameraToTablet')
    if not self.tabletCameraToTablet:
      self.tabletCameraToTablet=slicer.vtkMRMLLinearTransformNode()
      self.tabletCameraToTablet.SetName("tabletCameraToTablet")
      m = vtk.vtkMatrix4x4()
      m.SetElement( 0, 0, 1 ) # Row 1
      m.SetElement( 0, 1, 0 )
      m.SetElement( 0, 2, 0 )
      m.SetElement( 0, 3, 0 )      
      m.SetElement( 1, 0, 0 )  # Row 2
      m.SetElement( 1, 1, 1 )
      m.SetElement( 1, 2, 0 )
      m.SetElement( 1, 3, 0 )       
      m.SetElement( 2, 0, 0 )  # Row 3
      m.SetElement( 2, 1, 0 )
      m.SetElement( 2, 2, 1 )
      m.SetElement( 2, 3, 0 )
      self.tabletCameraToTablet.SetMatrixTransformToParent(m)
      slicer.mrmlScene.AddNode(self.tabletCameraToTablet)

    self.patientCameraToPatient = slicer.util.getNode('patientCameraToPatient')
    if not self.patientCameraToPatient:
      self.patientCameraToPatient=slicer.vtkMRMLLinearTransformNode()
      self.patientCameraToPatient.SetName("patientCameraToPatient")
      m = vtk.vtkMatrix4x4()
      m.SetElement( 0, 0, 1 ) # Row 1
      m.SetElement( 0, 1, 0 )
      m.SetElement( 0, 2, 0 )
      m.SetElement( 0, 3, 0 )      
      m.SetElement( 1, 0, 0 )  # Row 2
      m.SetElement( 1, 1, 1 )
      m.SetElement( 1, 2, 0 )
      m.SetElement( 1, 3, 0 )       
      m.SetElement( 2, 0, 0 )  # Row 3
      m.SetElement( 2, 1, 0 )
      m.SetElement( 2, 2, 1 )
      m.SetElement( 2, 3, 0 )
      self.patientCameraToPatient.SetMatrixTransformToParent(m)
      slicer.mrmlScene.AddNode(self.patientCameraToPatient)
     
  def __del__(self):
    self.viewpointLogic.stopViewpoint()

  def buildTransformTree(self, pointerModelNode, tabletModelNode, patientModelNode, PointerToTrackerTransformNode, TabletToTrackerTransformNode, ReferenceToTrackerTransformNode, PatientToReferenceTransformNode, TabletModelToTableTransformNode):
    # Build transform tree
    pointerModelNode.SetAndObserveTransformNodeID(PointerToTrackerTransformNode.GetID())
    tabletModelNode.SetAndObserveTransformNodeID(TabletModelToTableTransformNode.GetID())
    TabletModelToTableTransformNode.SetAndObserveTransformNodeID(TabletToTrackerTransformNode.GetID())
    patientModelNode.SetAndObserveTransformNodeID(PatientToReferenceTransformNode.GetID())
    PatientToReferenceTransformNode.SetAndObserveTransformNodeID(ReferenceToTrackerTransformNode.GetID())
  
  
  def SetTabletViewpoint(self, tabletModelNode, TabletToTrackerTransformNode):
    if TabletToTrackerTransformNode:
      self.tabletCameraToTablet.SetAndObserveTransformNodeID(TabletToTrackerTransformNode.GetID())  
      tabletModelNode.GetDisplayNode().SetOpacity(1)
      SceneCameraNode=slicer.util.getNode('Default Scene Camera')  
      
      # Viewpoint
      self.viewpointLogic.setCameraNode(SceneCameraNode)
      self.viewpointLogic.setTransformNode(self.tabletCameraToTablet)
      self.viewpointLogic.startViewpoint()

  def SetPatientViewpoint(self, patientModelNode, patientToTrackerTransformNode):
    if patientToTrackerTransformNode:
      self.patientCameraToPatient.SetAndObserveTransformNodeID(patientToTrackerTransformNode.GetID())  
      patientModelNode.GetDisplayNode().SetOpacity(1)
      SceneCameraNode=slicer.util.getNode('Default Scene Camera')  
      
      # Viewpoint
      self.viewpointLogic.setCameraNode(SceneCameraNode)
      self.viewpointLogic.setTransformNode(self.patientCameraToPatient)
      self.viewpointLogic.startViewpoint()

  def SetPointerViewpoint(self, pointerModelNode, PointerToTrackerTransformNode):
    if PointerToTrackerTransformNode:
      self.pointerCameraToPointer.SetAndObserveTransformNodeID(PointerToTrackerTransformNode.GetID())  
      pointerModelNode.GetDisplayNode().SetOpacity(1)
      SceneCameraNode=slicer.util.getNode('Default Scene Camera')  
      
      # Viewpoint
      self.viewpointLogic.setCameraNode(SceneCameraNode)
      self.viewpointLogic.setTransformNode(self.pointerCameraToPointer)
      self.viewpointLogic.startViewpoint()

  def StartViewpoint(self):
    self.viewpointLogic.startViewpoint()

  def StopViewpoint(self):
    self.viewpointLogic.stopViewpoint()



 



