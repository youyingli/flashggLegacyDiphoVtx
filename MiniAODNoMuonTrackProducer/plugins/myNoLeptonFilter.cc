// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/Common/interface/Ref.h"
#include "DataFormats/TrackReco/interface/Track.h"

//for AOD: 
#include "DataFormats/RecoCandidate/interface/RecoCandidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

using namespace std;
using namespace edm;
//using namespace math;

class myNoLeptonFilter : public edm::EDFilter {
    public:
        explicit myNoLeptonFilter(const edm::ParameterSet&);
        ~myNoLeptonFilter();

    private:
        virtual bool filter(edm::Event&, const edm::EventSetup&) override;
      
        EDGetTokenT<View<reco::Track> > allTrackToken_;
        EDGetTokenT<View<reco::Track> > noLepTrackToken_;

      // ----------member data ---------------------------
};

myNoLeptonFilter::myNoLeptonFilter(const edm::ParameterSet& iConfig):
  allTrackToken_( consumes<View<reco::Track> >( iConfig.getParameter<InputTag> ( "allTrackTag" ) ) ),
  noLepTrackToken_( consumes<View<reco::Track> >( iConfig.getParameter<InputTag> ( "noLepTrackTag" ) ) )
{
}


myNoLeptonFilter::~myNoLeptonFilter()
{
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
}

// ------------ method called on each new Event  ------------
bool
myNoLeptonFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{

    Handle<View<reco::Track> > allTracks;
    iEvent.getByToken( allTrackToken_, allTracks );

    Handle<View<reco::Track> > noLepTracks;
    iEvent.getByToken( noLepTrackToken_, noLepTracks );

    if (allTracks->size() - noLepTracks->size() != 2) return false;
    //else cout<<" PASSING "<< endl;
    return true;
}

//define this as a plug-in
DEFINE_FWK_MODULE(myNoLeptonFilter);
