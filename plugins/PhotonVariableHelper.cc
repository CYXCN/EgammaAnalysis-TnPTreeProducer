#include "PhotonVariableHelper.h"
#include "FWCore/Framework/interface/MakerMacros.h"

//PAT Photon for MiniAOD
typedef PhotonVariableHelper<pat::Photon> PatPhotonVariableHelper;
DEFINE_FWK_MODULE(PatPhotonVariableHelper);

//RECO Photon for AOD
typedef PhotonVariableHelper<reco::Photon> RecoPhotonVariableHelper;
DEFINE_FWK_MODULE(RecoPhotonVariableHelper);