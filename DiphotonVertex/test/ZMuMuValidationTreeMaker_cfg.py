import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils

process = cms.Process("ZMuMuValidationTreeMaker")

# geometry and global tag:
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v35')
#process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mc2017_realistic_v7')
#process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2018_realistic_v11_L1v1')
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mcRun2_asymptotic_preVFP_v11')
#process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mcRun2_asymptotic_v17')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 1000 )
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.source = cms.Source ("PoolSource",
        fileNames = cms.untracked.vstring(
#'root://cms-xrd-global.cern.ch//store/user/youying/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/ReMiniAOD_VTX_v1_DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/180116_143131/0000/miniAOD-prod_PAT_MC_1.root'
#'/store/user/youying/Vtx_UL/UL2017/DoubleMuon/DiphoVtxUL2017_DoubleMuon_Run2017B-09Aug2019_UL2017-v1/200810_162202/0000/miniAOD-prod_PAT_99.root'
'file:/afs/cern.ch/work/y/youying/UL_flashgg/vertex/zmumu/CMSSW_10_6_27/src/miniAOD-prod_PAT.root'
#'/store/user/youying/DoubleMuon/ReMiniAOD_VTX_DoubleMuon_Run2017B-17Nov2017-v1/180112_155329/0000/miniAOD-prod_PAT_101.root'
        )
)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("ZMuMuTree.root")
)

#Sequence builder
#**************************************************************
process.load("flashggLegacyDiphoVtx.DiphotonVertex.flashggZMuMuValidationSequence_cff")

#from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
#process.hltHighLevel= hltHighLevel.clone(HLTPaths = cms.vstring("HLT_IsoMu27_v*"))

process.commissioning = cms.EDAnalyzer('ZMuMuValidationTreeMaker',
                                       MuonTag =  cms.InputTag('slimmedMuons'),
                                       VertexTagWithMu=cms.InputTag('offlinePrimaryVerticesWithMu'),
                                       VertexTagNoMu=cms.InputTag('offlinePrimaryVerticesNoMu'),
                                       VertexSelectorName=cms.string("FlashggLegacyVertexSelector"),
                                       VertexCandidateMapTag=cms.InputTag('flashggVertexMapUniqueZMuMu'),
                                       VertexCandidateMapTagNoMu=cms.InputTag('flashggVertexMapUniqueZMuMuNoMu'),
                                       GenParticleTag=cms.InputTag('prunedGenParticles'),
                                       genEventInfoProduct=cms.InputTag('generator'),
                                       BeamSpotTag=cms.InputTag('offlineBeamSpot'),
                                       PileUpTag=cms.InputTag('slimmedAddPileupInfo'),

                                       #vtxId and vtxProb 2016 with single leg

                                       vertexIdMVAweightfile = cms.FileInPath("flashgg/MicroAOD/data/TMVAClassification_BDTVtxId_SL_2016.xml"),
                                       vertexProbMVAweightfile = cms.FileInPath("flashgg/MicroAOD/data/TMVAClassification_BDTVtxProb_SL_2016.xml"),

                                       useSingleLeg            = cms.bool(True),
                                       useZerothVertexFromMicro = cms.bool(False),

                                       nVtxSaveInfo            = cms.untracked.uint32(999),
                                       trackHighPurity         = cms.bool(False),
                                       pureGeomConvMatching    = cms.bool(True),
                                       dRexclude               = cms.double(0.05),

                                       #Reso 2016
                                       sigma1Pix               = cms.double(0.0125255),
                                       sigma1Tib               = cms.double(0.716301),
                                       sigma1Tob               = cms.double(3.17615),
                                       sigma1PixFwd            = cms.double(0.0581667),
                                       sigma1Tid               = cms.double(0.38521),
                                       sigma1Tec               = cms.double(1.67937),
                                       sigma2Pix               = cms.double(0.0298574),
                                       sigma2Tib               = cms.double(0.414393),
                                       sigma2Tob               = cms.double(1.06805),
                                       sigma2PixFwd            = cms.double(0.180419),
                                       sigma2Tid               = cms.double(0.494722),
                                       sigma2Tec               = cms.double(1.21941),
                                       singlelegsigma1Pix      = cms.double(0.0178107),
                                       singlelegsigma1Tib      = cms.double(1.3188),
                                       singlelegsigma1Tob      = cms.double(2.23662),
                                       singlelegsigma1PixFwd   = cms.double(0.152157),
                                       singlelegsigma1Tid      = cms.double(0.702755),
                                       singlelegsigma1Tec      = cms.double(2.46599),
                                       singlelegsigma2Pix      = cms.double(0.0935307),
                                       singlelegsigma2Tib      = cms.double(0.756568),
                                       singlelegsigma2Tob      = cms.double(0.62143),
                                       singlelegsigma2PixFwd   = cms.double(0.577081),
                                       singlelegsigma2Tid      = cms.double(0.892751),
                                       singlelegsigma2Tec      = cms.double(1.56638) 
)

process.p = cms.Path(process.flashggZMuMuValidationSequence
                    #*process.hltHighLevel
                    *process.commissioning
                    )
