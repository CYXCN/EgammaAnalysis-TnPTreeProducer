#ifndef _PHOTONVARIABLEHELPER_H
#define _PHOTONVARIABLEHELPER_H

#include "FWCore/Framework/interface/one/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/L1Trigger/interface/L1EmParticle.h"
#include "DataFormats/L1Trigger/interface/L1EmParticleFwd.h"
#include "DataFormats/L1Trigger/interface/EGamma.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/EgammaCandidates/interface/Photon.h"

#include "EgammaAnalysis/TnPTreeProducer/plugins/WriteValueMap.h"

template <class T>
class PhotonVariableHelper : public edm::one::EDProducer<>{
 public:
  explicit PhotonVariableHelper(const edm::ParameterSet & iConfig);
  virtual ~PhotonVariableHelper() ;

  virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup) override;

private:
  edm::EDGetTokenT<std::vector<T> > probesToken_;
  // 光子不需要 vertex 计算 dz/dxy，但如果做 L1 匹配等可能需要 beamspot
  edm::EDGetTokenT<BXVector<l1t::EGamma> > l1EGToken_;
  edm::EDGetTokenT<EcalRecHitCollection> recHitsEBToken_;
  edm::EDGetTokenT<EcalRecHitCollection> recHitsEEToken_;
};

template<class T>
PhotonVariableHelper<T>::PhotonVariableHelper(const edm::ParameterSet & iConfig) :
  probesToken_(consumes<std::vector<T> >(iConfig.getParameter<edm::InputTag>("probes"))),
  l1EGToken_(consumes<BXVector<l1t::EGamma> >(iConfig.getParameter<edm::InputTag>("l1EGColl"))),
  recHitsEBToken_(consumes<EcalRecHitCollection>(iConfig.getParameter<edm::InputTag>("ebRecHits"))),
  recHitsEEToken_(consumes<EcalRecHitCollection>(iConfig.getParameter<edm::InputTag>("eeRecHits")))
{
  // 移除径迹相关变量 (dz, dxy, sip, gsfhits, missinghits, kf*)
  produces<edm::ValueMap<float>>("l1e");
  produces<edm::ValueMap<float>>("l1et");
  produces<edm::ValueMap<float>>("l1eta");
  produces<edm::ValueMap<float>>("l1phi");
  
  // [关键] 保留 Seed Gain
  produces<edm::ValueMap<float>>("seedGain");
}

template<class T>
PhotonVariableHelper<T>::~PhotonVariableHelper()
{}

template<class T>
void PhotonVariableHelper<T>::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {

  edm::Handle<std::vector<T>> probes;
  iEvent.getByToken(probesToken_, probes);

  edm::Handle<BXVector<l1t::EGamma>> l1Cands;
  iEvent.getByToken(l1EGToken_, l1Cands);

  // Output vectors
  std::vector<float> l1EVals;
  std::vector<float> l1EtVals;
  std::vector<float> l1EtaVals;
  std::vector<float> l1PhiVals;
  std::vector<float> seedGains; // seed gain for scales

  // RecHits retrieval
  edm::Handle<EcalRecHitCollection> recHitsEBH, recHitsEEH;
  bool hasRecHitsEB = iEvent.getByToken(recHitsEBToken_, recHitsEBH);
  bool hasRecHitsEE = iEvent.getByToken(recHitsEEToken_, recHitsEEH);
  const EcalRecHitCollection* recHitsEBProd = hasRecHitsEB ? recHitsEBH.product() : nullptr;
  const EcalRecHitCollection* recHitsEEProd = hasRecHitsEE ? recHitsEEH.product() : nullptr;

  typename std::vector<T>::const_iterator probe, endprobes = probes->end();

  for (probe = probes->begin(); probe != endprobes; ++probe) {

    // --- L1 Matching Logic ---
    float l1e = 999999.;
    float l1et = 999999.;
    float l1eta = 999999.;
    float l1phi = 999999.;
    float dRmin = 0.3;

    for (std::vector<l1t::EGamma>::const_iterator l1Cand = l1Cands->begin(0); l1Cand != l1Cands->end(0); ++l1Cand) {
      // Photon 也有 superCluster()
      float dR = deltaR(l1Cand->eta(), l1Cand->phi() , probe->superCluster()->eta(), probe->superCluster()->phi());
      if (dR < dRmin) {
        dRmin = dR;
        l1e = l1Cand->energy();
        l1et = l1Cand->et();
        l1eta = l1Cand->eta();
        l1phi = l1Cand->phi();
      }
    }
    l1EVals.push_back(l1e);
    l1EtVals.push_back(l1et);
    l1EtaVals.push_back(l1eta);
    l1PhiVals.push_back(l1phi);

    // --- Seed Gain Logic (完全相同) ---
    // Photon 的 SuperCluster 结构与 Electron 相同
    auto detid = probe->superCluster()->seed()->seed();
    float tmpSeedVal = 12.0;
    
    // Check Barrel or Endcap logic
    // 注意: Photon 可能没有 isEB() 快捷方法，取决于版本。
    // 使用 DetId 判断更稳健，或者用 probe->isEB() 如果 pat::Photon 支持
    bool isEB = (detid.subdetId() == EcalBarrel);

    if (isEB) {
      if (recHitsEBProd) {
        auto it = recHitsEBProd->find(detid);
        if (it != recHitsEBProd->end()) {
          if (it->checkFlag(EcalRecHit::kHasSwitchToGain6)) tmpSeedVal = 6.0;
          if (it->checkFlag(EcalRecHit::kHasSwitchToGain1)) tmpSeedVal = 1.0;
        }
      }
    } else {
      if (recHitsEEProd) {
        auto it = recHitsEEProd->find(detid);
        if (it != recHitsEEProd->end()) {
          if (it->checkFlag(EcalRecHit::kHasSwitchToGain6)) tmpSeedVal = 6.0;
          if (it->checkFlag(EcalRecHit::kHasSwitchToGain1)) tmpSeedVal = 1.0;
        }
      }
    }
    seedGains.push_back(tmpSeedVal);
  }

  // Write ValueMaps
  writeValueMap(iEvent, probes, l1EVals, "l1e");
  writeValueMap(iEvent, probes, l1EtVals, "l1et");
  writeValueMap(iEvent, probes, l1EtaVals, "l1eta");
  writeValueMap(iEvent, probes, l1PhiVals, "l1phi");
  writeValueMap(iEvent, probes, seedGains, "seedGain");
}

#endif