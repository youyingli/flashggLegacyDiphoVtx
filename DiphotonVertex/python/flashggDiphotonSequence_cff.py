import FWCore.ParameterSet.Config as cms
import importlib
#from MyFlashggPlugins.DiphotonVertex.flashggTkVtxMapValidation_cfi import flashggVertexMapUnique,flashggVertexMapNonUnique
#
#from flashgg.MicroAOD.flashggPhotons_cfi import flashggPhotons
#from flashgg.MicroAOD.flashggRandomizedPhotonProducer_cff import flashggRandomizedPhotons
#from flashgg.MicroAOD.flashggDiPhotons_cfi import flashggDiPhotons
#from flashgg.MicroAOD.flashggMicroAODGenSequence_cff import *
#
#RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService")
#RandomNumberGeneratorService.flashggRandomizedPhotons = cms.PSet(
#                          initialSeed = cms.untracked.uint32(16253245)
#                          )
def includeRunIIEGMPhoID(process):
    from PhysicsTools.SelectorUtils.tools.vid_id_tools import DataFormat,switchOnVIDPhotonIdProducer,setupAllVIDIdsInModule,setupVIDPhotonSelection
    dataFormat = DataFormat.MiniAOD
    switchOnVIDPhotonIdProducer(process, DataFormat.MiniAOD)
    my_id_modules = ['RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Fall17_94X_V2_cff']
    for idmod in my_id_modules:
        setupAllVIDIdsInModule(process,idmod,setupVIDPhotonSelection)
    process.flashggPhotons.effAreasConfigFile = cms.FileInPath("RecoEgamma/PhotonIdentification/data/Fall17/effAreaPhotons_cone03_pfPhotons_90percentBased_TrueVtx.txt")
    process.flashggPhotons.egmMvaValuesMap = cms.InputTag("photonMVAValueMapProducer:PhotonMVAEstimatorRunIIFall17v2Values")




def getflashggDiphotonSequence(process, condition_dict):
    from flashgg.MicroAOD.flashggTkVtxMap_cfi import flashggVertexMapUnique,flashggVertexMapNonUnique
    setattr(process, 'flashggVertexMapUnique', flashggVertexMapUnique)
    setattr(process, 'flashggVertexMapNonUnique', flashggVertexMapNonUnique)

    process.load("flashgg.MicroAOD.flashggMicroAODGenSequence_cff")
    process.load("flashgg.MicroAOD.flashggPhotons_cfi")
    process.load("flashgg.MicroAOD.flashggRandomizedPhotonProducer_cff")
    process.load("flashgg.MicroAOD.flashggDiPhotons_cfi")

    includeRunIIEGMPhoID(process)
#    process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService")
#    process.RandomNumberGeneratorService.flashggRandomizedPhotons = cms.PSet(
#                              initialSeed = cms.untracked.uint32(16253245)
#                              )

    process.flashggPhotons.photonIdMVAweightfile_EB = cms.FileInPath(str(condition_dict["flashggPhotons"]["photonIdMVAweightfile_EB"]))
    process.flashggPhotons.photonIdMVAweightfile_EE = cms.FileInPath(str(condition_dict["flashggPhotons"]["photonIdMVAweightfile_EE"]))
    process.flashggPhotons.effAreasConfigFile = cms.FileInPath(str(condition_dict["flashggPhotons"]["effAreasConfigFile"]))
    process.flashggPhotons.is2017 = cms.bool(condition_dict["flashggPhotons"]["is2017"])

    process.flashggDiPhotons.vertexIdMVAweightfile = cms.FileInPath(str(condition_dict["flashggDiPhotons"]["vertexIdMVAweightfile"]))
    process.flashggDiPhotons.vertexProbMVAweightfile = cms.FileInPath(str(condition_dict["flashggDiPhotons"]["vertexProbMVAweightfile"]))

    return cms.Sequence( process.flashggVertexMapUnique * process.flashggVertexMapNonUnique
                                                 *process.flashggMicroAODGenSequence
                                                 *process.flashggPhotons * process.egmPhotonIDSequence *
                                                 process.flashggRandomizedPhotons * process.flashggDiPhotons
                                                )


def customizeSystematicsForMC(process):
    photonSmearBins = getattr(process,'photonSmearBins',None)
    photonScaleUncertBins = getattr(process,'photonScaleUncertBins',None)
    for pset in process.flashggDiPhotonSystematics.SystMethods:
        if photonSmearBins and pset.Label.value().startswith("MCSmear"):
            pset.BinList = photonSmearBins
        elif photonScaleUncertBins and pset.Label.value().count("Scale"):
            pset.BinList = photonScaleUncertBins

def includeScale_Central(process):
    # Keep default MC central value behavior, remove all up/down shifts
    customizeSystematicsForMC(process)
    vpsetlist = [process.flashggDiPhotonSystematics.SystMethods]
    vpsetlist += [process.flashggDiPhotonSystematics.SystMethods2D]
    for vpset in vpsetlist:
        for pset in vpset:
            if type(pset.NSigmas) == type(cms.vint32()):
                pset.NSigmas = cms.vint32() # Do not perform shift
            else:
                pset.NSigmas = cms.PSet( firstVar = cms.vint32(), secondVar = cms.vint32() ) # Do not perform shift - 2D case

def prepareflashggDiPhotonSystematicsTask(process, condition_dict):

    from flashgg.Systematics.SystematicsCustomize import useEGMTools
    process.load("flashgg.Systematics.flashggDiPhotonSystematics_cfi")
    process.flashggPreselectedDiPhotons.src = cms.InputTag('flashggDiPhotonSystematics')

    process.load("flashgg.Systematics." + condition_dict['flashggDiPhotonSystematics'])
    sysmodule = importlib.import_module("flashgg.Systematics." + condition_dict['flashggDiPhotonSystematics'])

    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.MCScaleHighR9EB)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.MCScaleLowR9EB)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.MCScaleHighR9EE)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.MCScaleLowR9EE)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.MCScaleGain6EB_EGM)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.MCScaleGain1EB_EGM)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.MaterialCentralBarrel)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.MaterialOuterBarrel)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.MaterialForward)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.ShowerShapeHighR9EB)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.ShowerShapeHighR9EE)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.ShowerShapeLowR9EB)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.ShowerShapeLowR9EE)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.FNUFEB)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.FNUFEE)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.MCSmearHighR9EE)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.MCSmearLowR9EE)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.MCSmearHighR9EB)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.MCSmearLowR9EB)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.MvaShift)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.PreselSF)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.electronVetoSF)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.TriggerWeight)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.LooseMvaSF)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.SigmaEOverEShift)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.SigmaEOverESmearing)
    process.flashggDiPhotonSystematics.SystMethods.append(sysmodule.FracRVWeight)

    SystTask = cms.Task(process.flashggDiPhotonSystematics)

    useEGMTools(process)
    includeScale_Central(process)

    return SystTask
