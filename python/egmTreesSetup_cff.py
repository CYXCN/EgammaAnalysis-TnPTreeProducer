import FWCore.ParameterSet.Config as cms
from EgammaAnalysis.TnPTreeProducer.logger import getLogger
log = getLogger()

###################################################################################
################  --- TAG AND PROBE collections
###################################################################################
import EgammaAnalysis.TnPTreeProducer.egmGoodParticlesDef_cff as goodPartDef

def setTagsProbes(process, options):

    eleHLTProducer = 'PatElectronTriggerCandProducer'
    gamHLTProducer = 'PatPhotonTriggerCandProducer'
    hltObjects     = 'selectedPatTrigger' if options['use80X'] else 'slimmedPatTrigger'
    genParticles   = 'prunedGenParticles'
    SCEleMatcher   = 'PatElectronMatchedCandidateProducer'


    if (options['useAOD']):
        eleHLTProducer = 'GsfElectronTriggerCandProducer'
        gamHLTProducer = 'PhotonTriggerCandProducer'
        hltObjects     = 'hltTriggerSummaryAOD'
        genParticles   = 'genParticles'
        SCEleMatcher   = 'GsfElectronMatchedCandidateProducer'
        goodPartDef.setGoodParticlesAOD(     process, options )

    else:
        goodPartDef.setGoodParticlesMiniAOD( process, options )

    # dR settings
    dR_tagEle = 0.1
    dR_tagPho = 0.1
    dR_probePho = 0.1
    dR_probeSC = 0.1
    dR_matchL1 = 0.2
    dR_matchL1_EE = 0.2
    if options['DRSEETING'] != None:
        dR_settings = options['DRSEETING']
        dR_tagEle    = dR_settings.get('dR_tagEle',    dR_tagEle)
        dR_tagPho    = dR_settings.get('dR_tagPho',    dR_tagPho)
        dR_probePho  = dR_settings.get('dR_probePho',  dR_probePho)
        dR_probeSC   = dR_settings.get('dR_probeSC',   dR_probeSC)
        dR_matchL1   = dR_settings.get('dR_matchL1',   dR_matchL1)
        dR_matchL1_EE= dR_settings.get('dR_matchL1_EE',dR_matchL1_EE)


    def setupTag(process, options, label, inputCollection, producerType, dR_tag, orForSeeded=True):
        tagName = "tag" + label
        
        # 1. Tag Producer
        module = cms.EDProducer(producerType,
                                filterNames = cms.vstring(options['TnPHLTTagFilters']),
                                inputs      = cms.InputTag(inputCollection),
                                bits        = cms.InputTag('TriggerResults::' + options['HLTProcessName']),
                                objects     = cms.InputTag(hltObjects),
                                dR          = cms.double(dR_tag),
                                isAND       = cms.bool(True)
                                )
        setattr(process, tagName, module)

        # 2. Tagged leg seeded matching if required
        if options.get('DoTagSeededLegMatch', False):
            seeded_filters = options.get('TagSeededLegFilters', [])
            # Filter out L1 match filters if any, usually seeded filters are HLT
            filters_to_use = [f for f in seeded_filters if not f.endswith('L1match')]
            
            matchSeededLegName = tagName + "MatchSeededLeg"
            
            moduleSeeded = cms.EDProducer(producerType,
                                filterNames = cms.vstring(filters_to_use),
                                inputs      = cms.InputTag(tagName),
                                bits        = cms.InputTag('TriggerResults::' + options['HLTProcessName']),
                                objects     = cms.InputTag(hltObjects),
                                dR          = cms.double(dR_tag),
                                isAND       = cms.bool(False)  if orForSeeded else cms.bool(True)
                            )
            setattr(process, matchSeededLegName, moduleSeeded)

            do_seperate = True
            if do_seperate:
                for filter in filters_to_use:
                    singleFilterName = matchSeededLegName + filter.replace('::','_').replace('*','All').replace('.','_').replace('-','_')
                    moduleSingle = cms.EDProducer(producerType,
                                        filterNames = cms.vstring(filter),
                                        inputs      = cms.InputTag(tagName),
                                        bits        = cms.InputTag('TriggerResults::' + options['HLTProcessName']),
                                        objects     = cms.InputTag(hltObjects),
                                        dR          = cms.double(dR_tag),
                                        isAND       = cms.bool(False)  if orForSeeded else cms.bool(True)
                                    )
                    setattr(process, singleFilterName, moduleSingle)
    
    ##################### TAG ELECTRONs ###########################
    setupTag(process, options, "Ele", "tagEleCutBasedTight", eleHLTProducer, dR_tagEle)
    ##################### TAG PHOTONs #############################
    setupTag(process, options, "Pho", "tagPhoCutBasedTight", gamHLTProducer, dR_tagPho)

    def setupProbe(process, options, label, inputCollection, producerType, dR_probe, tag_is_photon = False, l1ProducerType=None):
        probeName = "probe" + label
        passHLTName = probeName + "PassHLT"
        
        # 1. Probe Producer (Reco matched to HLT)
        _module = cms.EDProducer(producerType,
                                filterNames = cms.vstring(options['TnPHLTProbeFilters']),
                                inputs      = cms.InputTag(inputCollection),
                                bits        = cms.InputTag('TriggerResults::' + options['HLTProcessName']),
                                objects     = cms.InputTag(hltObjects),
                                dR          = cms.double(dR_probe),
                                isAND       = cms.bool(True)
                                )
        setattr(process, probeName, _module)

        if (tag_is_photon and label == "Ele") or (not tag_is_photon and label == "Pho"):
            log.warning("The tag is a photon while the probe is an electron or vice versa. The dR matching may not work as intended.")
            return
        # 2. PassHLT Producer (Probe matched to specific filters)
        setattr(process, passHLTName, 
                _module.clone(
                    inputs = cms.InputTag(probeName),
                    isAND  = cms.bool(False)
                ))

        # 3. L1 Matching
        probeL1MatchedName = probeName + "L1matched"
        passHLTL1MatchedName = passHLTName + "L1matched"
        hasL1 = False

        if options['ApplyL1Matching'] and l1ProducerType:
            hasL1 = True
            l1ProbesName = "good" + label + "ProbesL1"
            setattr(process, l1ProbesName,
                    cms.EDProducer(l1ProducerType,
                                   inputs       = cms.InputTag(inputCollection),
                                   objects      = cms.InputTag("caloStage2Digis:EGamma"),
                                   minET        = cms.double(options['L1Threshold']),
                                   dRmatch      = cms.double(dR_matchL1),
                                   dRmatchEE    = cms.double(dR_matchL1_EE),
                                   isolatedOnly = cms.bool(False)
                    ))
            
            setattr(process, probeL1MatchedName,
                    getattr(process, probeName).clone(inputs = cms.InputTag(l1ProbesName)))
            setattr(process, passHLTL1MatchedName,
                    getattr(process, passHLTName).clone(inputs = cms.InputTag(probeL1MatchedName)))

        # 4. HLT Filters
        for flag, filterNames in options['HLTFILTERSTOMEASURE'].items():

            isL1 = 'L1match' in flag
            if isL1 and not hasL1: continue # Skip L1 flags if this probe doesn't support L1

            srcName = passHLTL1MatchedName if isL1 else passHLTName
            setattr(process, flag, getattr(process, srcName).clone(filterNames=filterNames))

    if options['ApplyL1Matching']:
        log.info("L1 matching will be applied for %s" % ', '.join([f.replace('L1match','') for f in options['HLTFILTERSTOMEASURE'].keys() if 'L1match' in f]))

    ##################### PROBE ELECTRONs ###########################
    setupProbe(process, options, "Ele", "goodElectrons", eleHLTProducer, dR_tagEle, options.get('isTagPho', False),"PatElectronL1Stage2CandProducer")

    ###################### PROBE PHOTONs ############################
    setupProbe(process, options, "Pho", "goodPhotons", gamHLTProducer, dR_probePho, options.get('isTagPho', False), "PatPhotonL1Stage2CandProducer")

    if options['useAOD'] : process.probePho = process.goodPhotons.clone()

    ######################### PROBE SCs #############################
    process.probeSC     = cms.EDProducer("RecoEcalCandidateTriggerCandProducer",
                                            filterNames  = cms.vstring(options['TnPHLTProbeFilters']),
                                             inputs       = cms.InputTag("goodSuperClusters"),
                                             bits         = cms.InputTag('TriggerResults::' + options['HLTProcessName']),
                                             objects      = cms.InputTag(hltObjects),
                                             dR           = cms.double(dR_probeSC),
                                             isAND        = cms.bool(True)
                                        )

    process.probeSCEle = cms.EDProducer( SCEleMatcher,
                                            src     = cms.InputTag("superClusterCands"),
                                            ReferenceElectronCollection = cms.untracked.InputTag("goodElectrons"),
                                            cut = cms.string(options['SUPERCLUSTER_CUTS'])
                                        )

    ########################## gen tag & probes ######################
    if options['isMC'] :
        cut_gen_standard = 'abs(pdgId) == 11 && pt > 3 && abs(eta) < 2.7 && isPromptFinalState'
        cut_gen_flashgg  = 'abs(pdgId) == 11 && pt > 3 && abs(eta) < 2.7 && ( isPromptFinalState || status == 23)'
        cut_gen_tau      = 'abs(pdgId) == 11 && pt > 3 && abs(eta) < 2.7 && ( isPromptFinalState || isDirectPromptTauDecayProductFinalState) '
        cut_gen_pho = 'abs(pdgId) == 22 && pt > 3 && abs(eta) < 2.7 && isPromptFinalState'

        process.genEle   = cms.EDFilter( "GenParticleSelector",
                                          src = cms.InputTag(genParticles),
                                          cut = cms.string(cut_gen_standard),
                                          )

        process.genTagEle = cms.EDProducer("MCMatcher",
                                            src      = cms.InputTag("tagEle"),
                                            matched  = cms.InputTag("genEle"),
                                            mcStatus = cms.vint32(),
                                            mcPdgId  = cms.vint32(),
                                            checkCharge = cms.bool(False),
                                            maxDeltaR   = cms.double(0.20),   # Minimum deltaR for the match
                                            maxDPtRel   = cms.double(50.0),    # Minimum deltaPt/Pt for the match
                                            resolveAmbiguities    = cms.bool(False), # Forbid two RECO objects to match to the same GEN objec
                                            resolveByMatchQuality = cms.bool(True),  # False = just match input in order; True = pick lowest deltaR pair first
                                            )

        process.genProbeEle  = process.genTagEle.clone( src = cms.InputTag("probeEle") )
        process.genProbePho  = process.genTagEle.clone( src = cms.InputTag("probePho") )
        process.genProbeSC   = process.genTagEle.clone( src = cms.InputTag("probeSC")  )

        if options['isTagPho']:
            process.genPho = cms.EDFilter("GenParticleSelector",
                                          src = cms.InputTag(genParticles),
                                          cut = cms.string(cut_gen_flashgg), # in photon collection, we indeeded want electron
                                          )
            process.genTagPho = cms.EDProducer("MCMatcher",
                                            src      = cms.InputTag("tagPho"),
                                            matched  = cms.InputTag("genPho"),
                                            mcStatus = cms.vint32(),
                                            mcPdgId  = cms.vint32(),
                                            checkCharge = cms.bool(False),
                                            maxDeltaR   = cms.double(0.20),   # Minimum deltaR for the match
                                            maxDPtRel   = cms.double(50.0),    # Minimum deltaPt/Pt for the match
                                            resolveAmbiguities    = cms.bool(False), # Forbid two RECO objects to match to the same GEN objec
                                            resolveByMatchQuality = cms.bool(True),  # False = just match input in order; True = pick lowest deltaR pair first
                                            )
            process.genProbePho = process.genTagPho.clone( src = cms.InputTag("probePho") )
            process.genProbeSC  = process.genTagPho.clone( src = cms.InputTag("probeSC")  )


    ########################### TnP pairs ############################
    masscut = cms.string("50<mass<130")
    process.tnpPairingEleHLT   = cms.EDProducer("CandViewShallowCloneCombiner",
                                        decay = cms.string("tagEle@+ probeEle@-"),
                                        checkCharge = cms.bool(True),
                                        cut = masscut,
                                        )

    process.tnpPairingEleRec             = process.tnpPairingEleHLT.clone()
    process.tnpPairingEleRec.decay       = cms.string("tagEle probeSC" )
    process.tnpPairingEleRec.checkCharge = cms.bool(False)

    process.tnpPairingEleIDs             = process.tnpPairingEleHLT.clone()
    process.tnpPairingEleIDs.decay       = cms.string("tagEle probeEle")
    process.tnpPairingEleIDs.checkCharge = cms.bool(False)

    process.tnpPairingPhoIDs             = process.tnpPairingEleHLT.clone()
    process.tnpPairingPhoIDs.decay       = cms.string("tagEle probePho")
    process.tnpPairingPhoIDs.checkCharge = cms.bool(False)

    if options['isTagPho']:
        process.tnpPairingEleHLT.decay       = cms.string("tagPho probePho")
        process.tnpPairingEleHLT.checkCharge = cms.bool(False)
        process.tnpPairingEleRec.decay       = cms.string("tagPho probeSC")
        process.tnpPairingEleIDs.decay       = cms.string("tagPho probeEle")
        process.tnpPairingPhoIDs.decay       = cms.string("tagPho probePho")


###################################################################################
################  --- SEQUENCES
###################################################################################
def setSequences(process, options):

    process.init_sequence = cms.Sequence()
    if options.get('isTagPho', False) and not options['useAOD']:
        process.init_sequence += process.patObjectCrossLinker
    if options['UseCalibEn']:
        process.enCalib_sequence = cms.Sequence(
            process.regressionApplication  *
            process.calibratedPatElectrons *
            process.calibratedPatPhotons   *
            process.selectElectronsBase    *
            process.selectPhotonsBase
            )
        process.init_sequence += process.enCalib_sequence


    process.sc_sequence  = cms.Sequence()
    if options['useAOD'] : process.sc_sequence += process.sc_sequenceAOD
    else :                 process.sc_sequence += process.sc_sequenceMiniAOD
    process.sc_sequence += process.probeSC
    process.sc_sequence += process.probeSCEle

    import EgammaAnalysis.TnPTreeProducer.egmElectronIDModules_cff as egmEleID
    process.ele_sequence  = egmEleID.setIDs(process, options)
    process.ele_sequence += cms.Sequence(process.probeEle)

    import EgammaAnalysis.TnPTreeProducer.egmPhotonIDModules_cff as egmPhoID
    process.pho_sequence  = cms.Sequence(process.goodPhotons)
    process.pho_sequence += egmPhoID.setIDs(process, options)
    process.pho_sequence += cms.Sequence(process.probePho)


    if options['ApplyL1Matching'] and not options['isTagPho']:
      process.ele_sequence += process.goodEleProbesL1
      process.ele_sequence += process.probeEleL1matched
    if options['ApplyL1Matching'] and options['isTagPho']:
      process.pho_sequence += process.goodPhoProbesL1
      process.pho_sequence += process.probePhoL1matched

    process.tag_sequence = cms.Sequence(
        process.goodElectrons             +
        process.tagEleCutBasedTight       + # note: this one also gets introduced by the egmEleID.setIDs function
        process.tagEle
        )
    
    if options['isTagPho']:
        process.tag_sequence = cms.Sequence(
            process.goodPhotons +
            process.tagPhoCutBasedTight +
            process.tagPho
        )

    # Add tagged leg seeded matching if required, to run seeded and unseeded in the same job
    if options.get('DoTagSeededLegMatch', False):
        tagName = "tagEle" if not options['isTagPho'] else "tagPho"
        matchSeededLegName = tagName + "MatchSeededLeg"
        
        # Add the combined seeded leg match module
        process.tag_sequence += getattr(process, matchSeededLegName)
        
        # Add individual filter match modules if they exist
        for attr in dir(process):
            if attr.startswith(matchSeededLegName) and attr != matchSeededLegName:
                process.tag_sequence += getattr(process, attr)

    process.hlt_sequence = cms.Sequence( process.hltFilter )
    for flag in options['HLTFILTERSTOMEASURE']:
        if hasattr(process, flag):
            process.hlt_sequence += getattr(process, flag)

    if options['isMC'] :
        if not options['isTagPho']:
            process.tag_sequence += process.genEle + process.genTagEle
        process.ele_sequence += process.genProbeEle
        process.pho_sequence += process.genProbePho
        process.sc_sequence  += process.genProbeSC
        if options['isTagPho']:
            process.tag_sequence += process.genPho + process.genTagPho

    process.init_sequence += process.egmGsfElectronIDSequence
    process.init_sequence += process.egmPhotonIDSequence
    process.init_sequence += process.eleVarHelper
    process.init_sequence += process.phoVarHelper
    process.init_sequence += process.isoForPho
    if options['addSUSY'] : process.init_sequence += process.susy_sequence
    if options['addSUSY'] : process.init_sequence += process.susy_sequence_requiresVID


###################################################################################
################  --- tree Maker setup
###################################################################################
def setupTreeMaker(process, options) :
    from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
    process.hltFilter = hltHighLevel.clone()
    process.hltFilter.throw = cms.bool(True)
    process.hltFilter.HLTPaths = options['TnPPATHS']
    process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","",options['HLTProcessName'])

    if options.get('isTagPho', False) and not options['useAOD']:
        process.patObjectCrossLinker = cms.EDProducer("PATObjectCrossLinker",
            electrons = cms.InputTag("slimmedElectrons"),
            photons = cms.InputTag("slimmedPhotons"),
            muons = cms.InputTag("slimmedMuons"),
            jets = cms.InputTag("slimmedJets"),
            taus = cms.InputTag("slimmedTaus"),
        )
        options['PHOTON_COLL'] = "patObjectCrossLinker:photons"

    setTagsProbes( process, options )
    setSequences(  process, options )


def customize( tnpTree, options ):
    tnpTree.arbitration = cms.string("HighestPt")
    if options['isMC'] :
        tnpTree.isMC = cms.bool( True )
        tnpTree.eventWeight = cms.InputTag("generator")
        tnpTree.PUWeightSrc = cms.InputTag("pileupReweightingProducer","pileupWeights")
    else:
        tnpTree.isMC = cms.bool( False )

