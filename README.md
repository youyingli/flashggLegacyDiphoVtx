# flashggLegacyDiphoVtx

## Installation
Since the lxplus7 was closed, if you want to install CMSSW_10_6_X, please use the singularity of ```cmssw-el7```.
The package needs to use some dependencies from the flashgg framework. If you want to use your flashgg, please replace the following flashgg link with your flashgg GitHub.

```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_47_patch1
cd CMSSW_10_6_47_patch1/src
cmsenv
git cms-init

#flashgg framework
git clone -b dev_legacy_runII https://github.com/cms-analysis/flashgg 
source flashgg/setup_flashgg.sh

#flashgg vertex framework
git clone https://github.com/youyingli/flashggLegacyDiphoVtx.git
source flashggLegacyDiphoVtx/setup.sh

scram b -j 8
```

## Usage

### Production of the MiniAOD-like files without two muon tracks 

In order to produce an EDM file with the MiniAOD-like format and vertex collection from general tracks without two muon tracks, please use the following Python scripts for data and MC:

```
cmsRun flashggLegacyDiphoVtx/MiniAODNoMuonTrackProducer/test/miniAOD-skim_PAT_MC.py    # MC
cmsRun flashggLegacyDiphoVtx/MiniAODNoMuonTrackProducer/test/miniAOD-skim_PAT_Data.py  # Data
```
Note that you should change some configurations, such as the global tag, trigger path, and event contents for different situations (Here only keeps the muon-related, tracks, and vertex contents in the output file). 

### Diphoton vertex algorithm validation through Z to dimuon
After producing an EDM file with the MiniAOD-like format and vertex collection from general tracks without two muon tracks, the validation can start from this file as input, run the following Python script, and produce the designed ntuple:
```
cmsRun flashggLegacyDiphoVtx/DiphotonVertex/test/ZMuMuValidationTreeMaker_cfg.py
```
