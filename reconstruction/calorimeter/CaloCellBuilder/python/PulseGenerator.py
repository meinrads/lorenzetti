
__all__ = ["PulseGenerator"]

from GaugiKernel import Logger
from GaugiKernel.macros import *
from G4Kernel import treatPropertyValue


class PulseGenerator( Logger ):

  __allow_keys = ["OutputLevel", 
                  "NSamples", 
                  "ShaperFile",
                  "Pedestal",
                  "DeformationMean",
                  "DeformationStd",
                  "NoiseMean",
                  "NoiseStd",
                  "SamplingRate",
                  "StartSamplingBC",
                  ]

  def __init__( self, name, **kw ):

    Logger.__init__(self)
    import ROOT
    ROOT.gSystem.Load('liblorenzetti')
    from ROOT import RunManager, PulseGenerator
    self.__core = PulseGenerator(name)
    for key, value in kw.items():
      self.__core.setProperty( key, value )


  def core(self):
    return self.__core


  def setProperty( self, key, value ):
    if key in self.core().hasProperty(key):
      setattr( self, key , value )
      self.core().setProperty( key, treatPropertyValue(value) )
    else:
      MSG_FATAL( self, "Property with name %s is not allow for %s object", key, self.__class__.__name__)

 
  def getProperty( self, key ):
    if hasattr(self, key):
      return getattr( self, key )
    else:
      MSG_FATAL( self, "Property with name %s is not allow for %s object", key, self.__class__.__name__)


     

