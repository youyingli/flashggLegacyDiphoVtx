import FWCore.ParameterSet.Config as cms


myNoMuonFilter = cms.EDFilter( 'myNoLeptonFilter',
                                allTrackTag   = cms.InputTag('myNoMuonTrackProducerWithMu'),
                                noLepTrackTag = cms.InputTag('myNoMuonTrackProducerNoMu')
)

