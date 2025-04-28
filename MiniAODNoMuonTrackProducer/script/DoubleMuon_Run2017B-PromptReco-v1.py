from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.section_('General')
config.General.requestName = 'DoubleMuon_Run2017B-PromptReco-v1'
config.General.workArea = 'youying_crab'
config.General.transferOutputs = True
config.General.transferLogs = True

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'MiniAODNoMuonTrackProducer/MiniAODProducer/test/miniAOD-prod_PAT_DATA_AllVerticesCollFiltered.py'
config.JobType.pyCfgParams = []
config.JobType.maxMemoryMB = 2000
config.JobType.maxJobRuntimeMin = 2000

config.section_('Data')
config.Data.inputDataset = '/DoubleMuon/Run2017B-PromptReco-v1/AOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 67
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/PromptReco/Cert_294927-303825_13TeV_PromptReco_Collisions17_JSON.txt'
config.Data.outLFNDirBase = '/store/user/youying'
config.Data.publication = True
config.Data.outputDatasetTag = 'ReMiniAOD_DoubleMuon_Run2017B-PromptReco-v1'

config.section_('Site')
config.Site.storageSite = 'T2_TW_NCHC'
