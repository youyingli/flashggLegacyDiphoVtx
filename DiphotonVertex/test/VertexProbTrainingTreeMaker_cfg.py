import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils
import FWCore.ParameterSet.VarParsing as opts
import os, json

options = opts.VarParsing ('analysis')
options.register('isZeroVertex',
                 False,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.bool,
                 'isZeroVertex'
                 )

options.register('year',
                 '2017',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'year'
                 )

options.parseArguments()

metaConditionVersion = ''

if options.year == '2016pre':
    metaConditionVersion = 'Era2016_legacyPreVFP_v1.json'
if options.year == '2016post':
    metaConditionVersion = 'Era2016_legacyPostVFP_v1.json'
elif options.year == '2017':
    metaConditionVersion = 'Era2017_legacy_v1.json'
elif options.year == '2018':
    metaConditionVersion = 'Era2018_legacy_v1.json'
else:
    print '[ERROR] : Please input 2016, 2017, 2018'

condition_dict = {}
with open( os.path.expandvars('$CMSSW_BASE/src/flashgg/MetaData/data/MetaConditions/' + metaConditionVersion) ) as json_condition:
    condition_dict = json.load(json_condition)


process = cms.Process("VertexProbTrainingTreeMaker")

# geometry and global tag:
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, condition_dict['globalTags']['MC'])

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 1000 )
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.source = cms.Source ("PoolSource",
        fileNames = cms.untracked.vstring(
#'/store/mc/RunIIFall17MiniAODv2/GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/90000/044F95FB-A342-E811-907F-5065F3816251.root'
#'/store/mc/RunIISummer19UL17MiniAOD/GluGluHToGG_M123_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/20000/8A70E23F-5672-9D4A-86F6-BDEF995BFD21.root'
#'/store/mc/RunIISummer19UL18MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8_storeWeights/MINIAODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/10000/06E2EC66-170E-9348-972F-291AE6C47865.root'
'/store/mc/RunIISummer19UL17MiniAODv2/GluGluHToGG_M-125_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/00000/45D3A883-AC2F-F847-84A0-806D1D55B28E.root'
#'/store/mc/RunIIAutumn18MiniAOD/GluGluHToGG_M-125_13TeV_powheg_pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/60000/FF3573F4-A9DA-7B4C-A1BE-E893C22B75E3.root'
#'/store/mc/RunIIFall17MiniAODv2/ttHJetToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/70000/307FE799-6B42-E811-8A34-0025905A48D6.root'
        )
)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("VertexProbTrainingTree.root")
)

#Sequence builder
#**************************************************************
from flashggLegacyDiphoVtx.DiphotonVertex.flashggDiphotonSequence_cff import getflashggDiphotonSequence, prepareflashggDiPhotonSystematicsTask
diphoSep = getflashggDiphotonSequence(process, condition_dict)
process.flashggDiPhotons.useZerothVertexFromMicro = cms.bool(options.isZeroVertex)

from flashgg.Taggers.flashggDifferentialPhoIdInputsCorrection_cfi import setup_flashggDifferentialPhoIdInputsCorrection
setup_flashggDifferentialPhoIdInputsCorrection(process, condition_dict)

process.RandomNumberGeneratorService.flashggRandomizedPhotons = cms.PSet(
                          initialSeed = cms.untracked.uint32(16253245)
                          )
process.load("flashgg.Taggers.flashggPreselectedDiPhotons_cfi")
diphoSystTask = prepareflashggDiPhotonSystematicsTask(process, condition_dict)

#from flashgg.Taggers.flashggPreselectedDiPhotons_cfi import flashggPreselectedDiPhotons
#setattr(process, 'flashggPreselectedDiPhotons', flashggPreselectedDiPhotons)

process.commissioning = cms.EDAnalyzer('VertexProbTrainingTreeMaker',
                                       DiPhotonTag             = cms.InputTag('flashggPreselectedDiPhotons'),
                                       #DiPhotonTag             = cms.InputTag('flashggDiPhotonSystematics'),
                                       VertexTag               = cms.InputTag('offlineSlimmedPrimaryVertices'),
                                       VertexCandidateMapTagDz = cms.InputTag('flashggVertexMapUnique'),
                                       BeamSpotTag             = cms.InputTag('offlineBeamSpot'),
                                       rhoTag                  = cms.InputTag('fixedGridRhoFastjetAll'),
                                       GenParticleTag          = cms.InputTag('prunedGenParticles'),
                                       GenEventInfoTag         = cms.InputTag('generator'),
                                       PileUpTag               = cms.InputTag('slimmedAddPileupInfo'),
                                       isZeroVertex            = cms.bool(options.isZeroVertex)
)

process.p = cms.Path(diphoSep
                    *process.flashggDifferentialPhoIdInputsCorrection
                    *process.flashggPreselectedDiPhotons
                    *process.commissioning, diphoSystTask)
