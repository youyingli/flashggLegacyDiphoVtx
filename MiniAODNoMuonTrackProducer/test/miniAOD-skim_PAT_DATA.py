# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: miniAOD-prod -s PAT --runUnscheduled --nThreads 8 --data --era Run2_2017 --scenario pp --conditions 106X_dataRun2_v20 --eventcontent MINIAOD --datatier MINIAOD --filein /store/data/Run2017E/DoubleMuon/RAW/v1/000/303/824/00000/FECD0C22-0CA1-E711-A7E0-02163E01279A.root -n 1000 --python_filename=recoskim_Run2017E_DoubleMuon.py --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.ProcessModifiers.run2_miniAOD_UL_preSummer20_cff import run2_miniAOD_UL_preSummer20
#from Configuration.Eras.Era_Run2_2017_cff import Run2_2017
#from Configuration.Eras.Era_Run2_2018_cff import Run2_2018
#from Configuration.Eras.Era_Run2_2016_HIPM_cff import Run2_2016_HIPM
from Configuration.Eras.Era_Run2_2016_cff import Run2_2016

#process = cms.Process('PAT',Run2_2017)
#process = cms.Process('PAT',Run2_2018)
#process = cms.Process('PAT',Run2_2016_HIPM,run2_miniAOD_UL_preSummer20)
process = cms.Process('PAT',Run2_2016,run2_miniAOD_UL_preSummer20)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
#process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')
process.load('Configuration.StandardSequences.PAT_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100

# Input source
process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
#        '/store/data/Run2017D/DoubleMuon/AOD/09Aug2019_UL2017-v1/270000/FEECC77B-8207-2947-B3E2-B8A7A53EFA64.root'
#        '/store/data/Run2017E/DoubleMuon/AOD/09Aug2019_UL2017-v1/50000/FB73AED3-2215-6E41-9FA1-1FBDE3BB9899.root'
        '/store/data/Run2016H/DoubleMuon/AOD/21Feb2020_UL2016-v1/230000/040052EC-41E0-754B-B3AE-EC8125C938BE.root'
#        '/store/data/Run2018A/DoubleMuon/AOD/12Nov2019_UL2018-v2/100000/9870C1AF-1531-5F4D-BD77-25AEC7FF1F10.root'
#        '/store/data/Run2017D/DoubleMuon/AOD/09Aug2019_UL2017-v1/270000/FFB8524C-5148-F748-9AD5-B5BD3F342883.root'
#         '/store/data/Run2016G/DoubleMuon/AOD/21Feb2020_UL2016-v1/230000/001CDE8D-364D-5541-BA6E-2F6C2016F811.root'
    )
)

#For muon track manager(New branch for diphoton vertex id)
from flashggLegacyDiphoVtx.MiniAODNoMuonTrackProducer.myNoMuonTrackProducer_cfi import *
process.myNoMuonTrackProducerNoMu                 = myNoMuonTrackProducer.clone()
process.myNoMuonTrackProducerNoMu.doRemoveMuons   = cms.untracked.bool(True)
process.myNoMuonTrackProducerNoMu.isData          = cms.untracked.bool(True)

from RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi import *
process.offlinePrimaryVerticesNoMu                = offlinePrimaryVertices.clone()
process.offlinePrimaryVerticesNoMu.TrackLabel     = cms.InputTag('myNoMuonTrackProducerNoMu')


from flashggLegacyDiphoVtx.MiniAODNoMuonTrackProducer.myNoMuonTrackProducer_cfi import *
process.myNoMuonTrackProducerWithMu               = myNoMuonTrackProducer.clone()
process.myNoMuonTrackProducerWithMu.doRemoveMuons = cms.untracked.bool(False)
process.myNoMuonTrackProducerWithMu.isData        = cms.untracked.bool(True)

from RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi import *
process.offlinePrimaryVerticesWithMu              = offlinePrimaryVertices.clone()
process.offlinePrimaryVerticesWithMu.TrackLabel   = cms.InputTag('myNoMuonTrackProducerWithMu')

process.myFilter = cms.EDFilter('myNoLeptonFilter',
                                allTrackTag    = cms.InputTag('myNoMuonTrackProducerWithMu'),
                                noLepTrackTag  = cms.InputTag('myNoMuonTrackProducerNoMu')
)

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
#process.hltHighLevel = hltHighLevel.clone(HLTPaths = cms.vstring("HLT_IsoMu27_v*")) #2017
#process.hltHighLevel = hltHighLevel.clone(HLTPaths = cms.vstring("HLT_IsoMu24_v*")) #2018
process.hltHighLevel = hltHighLevel.clone(HLTPaths = cms.vstring("HLT_IsoMu24_v*", "HLT_IsoTkMu24_v*")) #2016

#process.selectionNoLeptonFilter = cms.Path( ( process.myNoMuonTrackProducerNoMu + process.myNoMuonTrackProducerWithMu) * process.myFilter)
process.selectionNoLeptonFilter = cms.Path( ( process.myNoMuonTrackProducerNoMu + process.myNoMuonTrackProducerWithMu) * process.myFilter * process.hltHighLevel )
process.vtxRefit = cms.Path( process.offlinePrimaryVerticesNoMu + process.offlinePrimaryVerticesWithMu )

# Output definition
MiniAODOutputContent = cms.untracked.vstring(
                'drop *',
                #'keep *_TriggerResults*_*_HLT',
                'keep *_offlinePrimaryVertices*_*_*',
                'drop *_offlinePrimaryVerticesWithBS_*_*',
                'keep *_offlineSlimmedPrimaryVertices*_*_*',
                'keep *_offlineBeamSpot*_*_*',
                'keep *_packedPFCandidates*_*_*',
                'keep *_slimmedMuons*_*_*'
                )


process.MINIAODoutput = cms.OutputModule('PoolOutputModule',
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

#process.MINIAODoutput.outputCommands.append('keep *_offlinePrimaryVertices*_*_*')
#process.MINIAODoutput.outputCommands.append('keep *_myNoMuonTrackProducer*_*_*')


# Additional output definition
#process.myNoMuonTrackProducerWithMu.verbose       = cms.untracked.bool(False)

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v35', '')

process.load('RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi')
process.offlinePrimaryVertices.verbose = cms.untracked.bool(False)

# Path and EndPath definitions
process.endjob_step = cms.EndPath(process.endOfProcess)
process.MINIAODoutput_step = cms.EndPath(process.MINIAODoutput)

# Schedule definition
process.schedule = cms.Schedule(process.selectionNoLeptonFilter,process.vtxRefit,process.endjob_step,process.MINIAODoutput_step)
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
from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllData 

#call to customisation function miniAOD_customizeAllData imported from PhysicsTools.PatAlgos.slimming.miniAOD_tools
process = miniAOD_customizeAllData(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
