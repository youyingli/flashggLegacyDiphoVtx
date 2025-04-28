# flashggLegacyDiphoVtx

### Install the code
```
cmsrel CMSSW_10_6_47_patch1
cd CMSSW_10_6_47_patch1/src
cmsenv
git cms-init
git clone -b dev_legacy_runII https://github.com/cms-analysis/flashgg 
source flashgg/setup_flashgg.sh

git clone https://github.com/youyingli/flashggLegacyDiphoVtx.git
source flashggLegacyDiphoVtx/setup.sh

scram b -j 8
```
