# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step6 --filein file:RECO.root --fileout file:MiniAOD.root --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 106X_mc2017_realistic_v6 --step PAT --nThreads 8 --geometry DB:Extended --era Run2_2017 --python_filename MINIAOD_2017_cfg.py -n 10 --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.ProcessModifiers.run2_miniAOD_UL_preSummer20_cff import run2_miniAOD_UL_preSummer20
#from Configuration.Eras.Era_Run2_2017_cff import Run2_2017
#from Configuration.Eras.Era_Run2_2018_cff import Run2_2018
from Configuration.Eras.Era_Run2_2016_cff import Run2_2016
from Configuration.Eras.Era_Run2_2016_HIPM_cff import Run2_2016_HIPM

#process = cms.Process('PAT',Run2_2017)
#process = cms.Process('PAT',Run2_2018)
#process = cms.Process('PAT',Run2_2016)
process = cms.Process('PAT',Run2_2016_HIPM, run2_miniAOD_UL_preSummer20)
#process = cms.Process('PAT',Run2_2016,run2_miniAOD_UL_preSummer20)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')
process.load('Configuration.StandardSequences.PATMC_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/mc/RunIISummer19UL17RECO/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/AODSIM/106X_mc2017_realistic_v6-v2/100001/8E3DBA70-C5AF-784F-94B8-3D68AD1D23B2.root'
        )
)

#For muon track manager(New branch for diphoton vertex id)
from flashggLegacyDiphoVtx.MiniAODNoMuonTrackProducer.myNoMuonTrackProducer_cfi import *
process.myNoMuonTrackProducerNoMu                 = myNoMuonTrackProducer.clone()
process.myNoMuonTrackProducerNoMu.doRemoveMuons   = cms.untracked.bool(True)
process.myNoMuonTrackProducerNoMu.isData          = cms.untracked.bool(False)

from RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi import *
process.offlinePrimaryVerticesNoMu                = offlinePrimaryVertices.clone()
process.offlinePrimaryVerticesNoMu.TrackLabel     = cms.InputTag('myNoMuonTrackProducerNoMu')


from flashggLegacyDiphoVtx.MiniAODNoMuonTrackProducer.myNoMuonTrackProducer_cfi import *
process.myNoMuonTrackProducerWithMu               = myNoMuonTrackProducer.clone()
process.myNoMuonTrackProducerWithMu.doRemoveMuons = cms.untracked.bool(False)
process.myNoMuonTrackProducerWithMu.isData        = cms.untracked.bool(False)

from RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi import *
process.offlinePrimaryVerticesWithMu              = offlinePrimaryVertices.clone()
process.offlinePrimaryVerticesWithMu.TrackLabel   = cms.InputTag('myNoMuonTrackProducerWithMu')

process.myFilter = cms.EDFilter('myNoLeptonFilter',
                                allTrackTag    = cms.InputTag('myNoMuonTrackProducerWithMu'),
                                noLepTrackTag  = cms.InputTag('myNoMuonTrackProducerNoMu')
)

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
#process.hltHighLevel = hltHighLevel.clone(HLTPaths = cms.vstring("HLT_IsoMu27_v*"))#2017
#process.hltHighLevel = hltHighLevel.clone(HLTPaths = cms.vstring("HLT_IsoMu24_v*"))#2018
process.hltHighLevel = hltHighLevel.clone(HLTPaths = cms.vstring("HLT_IsoMu24_v*", "HLT_IsoTkMu24_v*")) #2016

#process.selectionNoLeptonFilter = cms.Path( ( process.myNoMuonTrackProducerNoMu + process.myNoMuonTrackProducerWithMu) * process.myFilter)
process.selectionNoLeptonFilter = cms.Path( ( process.myNoMuonTrackProducerNoMu + process.myNoMuonTrackProducerWithMu) * process.myFilter * process.hltHighLevel )
process.vtxRefit = cms.Path( process.offlinePrimaryVerticesNoMu + process.offlinePrimaryVerticesWithMu )

# Output definition
MiniAODOutputContent = cms.untracked.vstring(
                'drop *',
                #'keep *_TriggerResults*_*_HLT',
                'keep *_generator_*_*',
                'keep *_prunedGenParticles_*_*',
                'keep *_slimmedAddPileupInfo_*_*',
                'keep *_offlinePrimaryVertices*_*_*',
                'drop *_offlinePrimaryVerticesWithBS_*_*',
                'keep *_offlineSlimmedPrimaryVertices*_*_*',
                'keep *_offlineBeamSpot*_*_*',
                'keep *_packedPFCandidates*_*_*',
                'keep *_slimmedMuons*_*_*'
                )


process.MINIAODSIMoutput = cms.OutputModule('PoolOutputModule',
    compressionAlgorithm         = cms.untracked.string('LZMA'),
    compressionLevel             = cms.untracked.int32(4),
    eventAutoFlushCompressedSize = cms.untracked.int32(-900),
    #outputCommands               = process.MINIAODEventContent.outputCommands, 
    outputCommands               = MiniAODOutputContent,
    fileName                     = cms.untracked.string('miniAOD-prod_PAT.root'),
    dropMetaData                 = cms.untracked.string('ALL'),
    fastCloning                  = cms.untracked.bool(False),
    splitLevel                   = cms.untracked.int32(0),
    overrideInputFileSplitLevels = cms.untracked.bool(True),
    SelectEvents                 = cms.untracked.PSet( SelectEvents = cms.vstring('selectionNoLeptonFilter') )
)
# Additional output definition
#process.myNoMuonTrackProducerWithMu.verbose       = cms.untracked.bool(False)

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mc2017_realistic_v7', '') #2017
#process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2018_realistic_v11_L1v1', '')#2018
#process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mcRun2_asymptotic_v17', '')#2016
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mcRun2_asymptotic_preVFP_v11', '')#2016 pre

process.load('RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi')
process.offlinePrimaryVertices.verbose = cms.untracked.bool(False)

# Path and EndPath definitions
process.endjob_step = cms.EndPath(process.endOfProcess)
process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.selectionNoLeptonFilter,process.vtxRefit,process.endjob_step,process.MINIAODSIMoutput_step)
process.schedule.associate(process.patTask)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
#process.options.numberOfThreads=cms.untracked.uint32(1)
#process.options.numberOfStreams=cms.untracked.uint32(0)
#process.options.numberOfConcurrentLuminosityBlocks=cms.untracked.uint32(1)

#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.PatAlgos.slimming.miniAOD_tools
from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllMC

#call to customisation function miniAOD_customizeAllMC imported from PhysicsTools.PatAlgos.slimming.miniAOD_tools
process = miniAOD_customizeAllMC(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
