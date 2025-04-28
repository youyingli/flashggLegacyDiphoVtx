import FWCore.ParameterSet.Config as cms


myNoMuonTrackProducer = cms.EDProducer('myNoMuonTrackProducer',
                                        recoCandidatesTag  = cms.InputTag('particleFlow','','RECO'),
                                        generalTrackTag    = cms.InputTag('generalTracks'),
                                        muonTag            = cms.InputTag('muons'),
                                        genEventInfo       = cms.InputTag('generator')
)

