import FWCore.ParameterSet.Config as cms

# Some miniAOD testfiles, about 1000 events copied to our eos storage
# (not running directly on datasets because they get moved around all the time and xrootd sucks)
filesMiniAOD_2018 = {
    'mc' :   cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/RunIIAutumn18MiniAOD-DYJetsToLL_M-50.root'),
    'data' : cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/Egamma-Run2018A-17Sep2018-v2.root'),
}

filesMiniAOD_2022 = {
    'mc' :   cms.untracked.vstring(''),
    'data' : cms.untracked.vstring('root://cmsxrootd.fnal.gov//store/data/Run2022B/EGamma/MINIAOD/PromptReco-v1/000/355/558/00000/92629520-53fb-4f1d-8465-a15b5504e149.root'),
}

filesMiniAOD_2023 = {
    'data' : cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/data/Run2023D/EGamma0/MINIAOD/22Sep2023_v2-v1/40000/01953bad-f7fc-496b-a729-e240bde2abc4.root'),
}

filesMiniAOD_2023preBPIX = {
    'mc' : cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/mc/Run3Summer23MiniAODv4/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v1/2550000/00070982-2c6a-4df6-9af7-530f9155c758.root')
    }

filesMiniAOD_2023postBPIX = {
    'mc' : cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/mc/Run3Summer23BPixMiniAODv4/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_postBPix_v2-v3/80000/0040c573-d7f9-47c0-bf8a-2c40619c8ffb.root')
    }

filesMiniAOD_2017 = {
    'mc' :   cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/RunIIFall17MiniAODv2-DYJetsToLL_M-50.root'),
    'data' : cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/SingleElectron-Run2017B-31Mar2018-v1.root'),
}

filesMiniAOD_2016 = {
    'mc' :   cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/RunIISummer16MiniAODv3-DYJetsToLL_M-50.root'),
    'data' : cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/SingleElectron-Run2016B-17Jul2018_ver2-v1.root'),
}

filesMiniAOD_2024 = {
    # /DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Winter24MiniAOD-133X_mcRun3_2024_realistic_v10-v2/MINIAODSIM
    'mc' : cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/mc/Run3Winter24MiniAOD/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/MINIAODSIM/133X_mcRun3_2024_realistic_v10-v2/70000/155d86af-6ef4-42bd-bf62-3740e41def71.root'),
    # /EGamma0/Run2024D-MINIv6NANOv15-v1/MINIAOD
    'data' : cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/data/Run2024D/EGamma0/MINIAOD/MINIv6NANOv15-v1/110002/aee7d8f5-d6ff-4e18-9bd2-56f014e5f7d7.root')
}

filesMiniAOD_2025 = {
    # /DYto2L-4Jets_Par-2J-MLL-50_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Winter25MiniAOD-142X_mcRun3_2025_realistic_v7-v2/MINIAODSIM
    'mc' : cms.untracked.vstring('root://cmsxrootd.fnal.gov//store/mc/Run3Winter25MiniAOD/DYto2L-4Jets_Par-2J-MLL-50_TuneCP5_13p6TeV_madgraphMLM-pythia8/MINIAODSIM/142X_mcRun3_2025_realistic_v7-v2/90000/80c85d6e-e844-47ec-9923-163d7378b948.root'),
    # 'mc' : cms.untracked.vstring('file:/eos/cms/store/group/phys_higgs/nonresonant_HH/PrivateProd/Yuxiang/TriggerSF/MiniAOD/2025/DYto2L-4Jets_Par-2J-MLL-50_file1.root'),
    # /EGamma0/Run2025D-PromptReco-v1/MINIAOD
    'data' : cms.untracked.vstring('root://cmsxrootd.fnal.gov//store/data/Run2025D/EGamma0/MINIAOD/PromptReco-v1/000/395/817/00000/990f0244-7184-48e1-814f-883f425398f7.root'),
    # 'data' : cms.untracked.vstring('file:/eos/cms/store/group/phys_higgs/nonresonant_HH/PrivateProd/Yuxiang/TriggerSF/MiniAOD/2025/Run2025D_EGamma0_file1.root')
}


# Some miniAOD UL testfiles, which are available now and hopefully don't get deleted too soon
filesMiniAOD_UL2016preVFP = {
    'mc':   cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/RunIISummer19UL16MiniAODAPV-DYJetsToLL_M-50.root'),
    'data': cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/SingleElectron-Run2016E-21Feb2020_UL2016_HIPM.root'),
}

filesMiniAOD_UL2016postVFP = {
    'mc':   cms.untracked.vstring(''),
    'data': cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/SingleElectron-Run2016F-21Feb2020_UL2016-postVFP.root'),
}

filesMiniAOD_UL2018 = {
    'mc' :   cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/RunIISummer19UL18MiniAOD-DYJetsToEE_M-50.root'),
    'data' : cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/Egamma-Run2018D-12Nov2019_UL2018.root'),
}

filesMiniAOD_UL2017 = {
    'mc' :   cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/RunIISummer19UL17MiniAOD-DYJetsToLL_M-50.root'),
    'data' : cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/SingleElectron-Run2017F-09Aug2019_UL2017.root'),
}


# AOD UL testfiles
filesAOD_UL2016preVFP = {
    'mc':   cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/RunIISummer19UL16RECOAPV-DYJetsToLL_M-50.root'),
    'data': cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/SingleElectron-Run2016E-21Feb2020_UL2016_HIPM-AOD.root'),
}

filesAOD_UL2016postVFP = {
    'mc':   cms.untracked.vstring(''),
    'data': cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/SingleElectron-Run2016F-21Feb2020_UL2016-postVFP-AOD.root'),
}

filesAOD_UL2018 = {
    'mc' :   cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/RunIISummer19UL18RECO-DYToEE_M-50.root'),
    'data' : cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/Egamma-Run2018D-12Nov2019_UL2018-AOD.root'),
}

filesAOD_UL2017 = {
    'mc' :   cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/RunIISummer19UL17RECO-DYToEE_M-50.root'),
    'data' : cms.untracked.vstring('file:/eos/cms/store/group/phys_egamma/tnpTuples/testFiles/SingleElectron-Run2017F-09Aug2019_UL2017-AOD.root'),
}

filesAOD_2022 = {
    'mc':   cms.untracked.vstring('file:../test/data/f10037a7-aa8b-4c35-9c7a-be28ecf22736.root'),
    'data': cms.untracked.vstring('file:../test/data/10037a7-aa8b-4c35-9c7a-be28ecf22736.root')
}

filesAOD_2023 = {
    'data' : cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/data/Run2023C/EGamma0/AOD/PromptReco-v1/000/367/094/00000/14a996e7-81c0-4c19-90e2-2571578bf2ad.root'),
    }

filesAOD_2023preBPIX = {
    'mc' : cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/mc/Run3Summer23DRPremix/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/AODSIM/130X_mcRun3_2023_realistic_v14-v1/2550000/002dfa75-be6d-469d-8098-a47e74158c99.root')
    }

filesAOD_2023postBPIX = {
    'mc' : cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/mc/Run3Summer23BPixDRPremix/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/AODSIM/130X_mcRun3_2023_realistic_postBPix_v2-v3/80000/00ebe845-8a8e-4ecd-a979-a74d292b87d6.root')
    }
