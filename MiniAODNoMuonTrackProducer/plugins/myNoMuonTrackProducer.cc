// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/Common/interface/Ref.h"
#include "DataFormats/TrackReco/interface/Track.h"

//for AOD: 
#include "DataFormats/MuonReco/interface/Muon.h"

#include "DataFormats/RecoCandidate/interface/RecoCandidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

//for miniAOD:
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/Math/interface/LorentzVector.h"


using namespace std;
using namespace edm;
using namespace reco;
using namespace math;

class myNoMuonTrackProducer : public edm::EDProducer 
{
public:
    explicit myNoMuonTrackProducer(const edm::ParameterSet&);
    ~myNoMuonTrackProducer();
  
private:
    virtual void produce(edm::Event&, const edm::EventSetup&);

    EDGetTokenT<View<reco::Candidate> > recoCandidateToken_;
    EDGetTokenT<View<reco::Muon> > muonToken_;
    EDGetTokenT<View<reco::Track> > generalTrackToken_;

    // ----------member data ---------------------------
  
    //double ptMin_;

    bool doRemoveMuons;
    bool isData;
    bool muonEventMC;
    int  nMuonInAccMC;
    int  nZInAccMC;

    int nPatMuonReco;
    int nZReco;

    int muonCount;
    int notMuonCount;
    int notMuonBestTrackCount;

};

myNoMuonTrackProducer::myNoMuonTrackProducer(const ParameterSet& iConfig):
    recoCandidateToken_( consumes<View<reco::Candidate> >( iConfig.getParameter<InputTag> ( "recoCandidatesTag" ) ) ),
    muonToken_( consumes<View<reco::Muon> >( iConfig.getParameter<InputTag>( "muonTag" ) ) ),
    generalTrackToken_( consumes<View<reco::Track> >( iConfig.getParameter<InputTag> ( "generalTrackTag" ) ) )
{
    doRemoveMuons = iConfig.getUntrackedParameter<bool>( "doRemoveMuons", true );
    isData = iConfig.getUntrackedParameter<bool>( "isData", false );
    produces< reco::TrackCollection >();
}


myNoMuonTrackProducer::~myNoMuonTrackProducer()
{
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)
}

// ------------ method called on each new Event  ------------
void
myNoMuonTrackProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{

    //muonCount = 0;
    //notMuonCount = 0;
    //notMuonBestTrackCount = 0;

    Handle<View<reco::Candidate> > recoCandidates;
    iEvent.getByToken( recoCandidateToken_, recoCandidates );

    Handle<View<reco::Muon> > muons;
    iEvent.getByToken( muonToken_, muons );

    Handle<View<reco::Track> > generalTracks;
    iEvent.getByToken( generalTrackToken_, generalTracks );
      
    std::unique_ptr<reco::TrackCollection> MuonLessTracks(new reco::TrackCollection);

    //muonEventMC = false;
    //nMuonInAccMC=0;
      
    int nMuonReco = 0;
    for(unsigned int j = 0 ; j < muons->size(); j++){
        Ptr<reco::Muon> the_muon = muons->ptrAt(j);
        if (muon::isLooseMuon(*the_muon) && the_muon->pt() > 10) nMuonReco++;
    }

    Ptr<reco::Muon> pat_muon1;
    Ptr<reco::Muon> pat_muon2;
    double dimuon_mass = 0;

    if (nMuonReco >= 2) {

        float min_dm = 9999.;
        const float Zmass = 91.19;
        Ptr<reco::Muon> pat_muontmp1;
        Ptr<reco::Muon> pat_muontmp2;
    
        for (unsigned int j = 0 ; j < muons->size(); j++) {
            pat_muontmp1= muons->ptrAt(j);
            if ( !(muon::isLooseMuon(*pat_muontmp1) && pat_muontmp1->pt() > 10) ) continue;

            for (unsigned int i = j+1 ; i < muons->size(); i++) {
                pat_muontmp2= muons->ptrAt(i);
                if ( !(muon::isLooseMuon(*pat_muontmp2) && pat_muontmp2->pt() > 10) ) continue;
        
                XYZTLorentzVector dimuon_p4;
                dimuon_p4 += pat_muontmp1->p4();
                dimuon_p4 += pat_muontmp2->p4();

                double dimuon_mass_tmp = dimuon_p4.M();
                double dm = fabs(dimuon_mass_tmp - Zmass);
                if (dm < min_dm){
                    pat_muon1 = pat_muontmp1;
                    pat_muon2 = pat_muontmp2;
                    dimuon_mass = dimuon_mass_tmp;
                    min_dm = dm;
                }
            }
        }    
    }

    bool pass = false;
    //if( mass>50 && mass<130 && nMuonReco>=2 ){
    if (dimuon_mass > 50 && dimuon_mass < 130 && nMuonReco >= 2) pass = true;
 
    for (unsigned int j = 0 ; j < generalTracks->size(); j++) {
        
        Ptr<reco::Track> the_track = generalTracks->ptrAt(j);
      
        bool doMatch = false;
        if(pass){
            if (the_track->pt() > 10){
                float dPt1 = fabs(the_track->pt() - pat_muon1->pt());
                float dPt2 = fabs(the_track->pt() - pat_muon2->pt());
                float dR1 = deltaR(the_track->eta(), the_track->phi(), pat_muon1->eta(), pat_muon1->phi());
                float dR2 = deltaR(the_track->eta(), the_track->phi(), pat_muon2->eta(), pat_muon2->phi()); 
                if (doRemoveMuons && ((dPt1 < 0.01 && dR1 < 0.005) || (dPt2 < 0.01 && dR2 < 0.005))) {
                    doMatch = true;
                    //cout << "Match one of two muons come from Z boson" << endl;
                }	
            }
        }
        if(!doMatch) MuonLessTracks->push_back(*the_track);            
    }
      
    iEvent.put(std::move(MuonLessTracks));  
}

//define this as a plug-in
DEFINE_FWK_MODULE(myNoMuonTrackProducer);
