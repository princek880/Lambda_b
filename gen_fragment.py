import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

_generator = cms.EDFilter("Pythia8GeneratorFilter",
                        pythiaPylistVerbosity = cms.untracked.int32(0),
                        pythiaHepMCVerbosity = cms.untracked.bool(False),
                        comEnergy = cms.double(5360.0),
                        maxEventsToPrint = cms.untracked.int32(0),
                        ExternalDecays = cms.PSet(
                            EvtGen130 = cms.untracked.PSet(
                                decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),  
                                particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'), 
                                list_forced_decays = cms.vstring('MyLambda_b0', "Myanti-Lambda_b0"),   
                                operates_on_particles = cms.vint32(),
                                convertPythiaCodes = cms.untracked.bool(False),
                                user_decay_file = cms.vstring('GeneratorInterface/ExternalDecays/data/LambdaB_JPsiLambda_ppi_noPol.dec')
                                
                             ),
                             parameterSets = cms.vstring('EvtGen130')
                         ),
                         PythiaParameters = cms.PSet(
                             pythia8CommonSettingsBlock,
                             pythia8CP5SettingsBlock,
                             processParameters = cms.vstring(
                                 'SoftQCD:nonDiffractive = on',
                                 'HardQCD:all = on',
			                    #  'MultipartonInteractions:processLevel = 3',
                                 'PhaseSpace:pTHatMin = 5', #min pthat
                             ),
                             parameterSets = cms.vstring(
                                 'pythia8CommonSettings',
                                 'pythia8CP5Settings',
                                 'processParameters',
                             )
                         )
                     )

from GeneratorInterface.Core.ExternalGeneratorFilter import ExternalGeneratorFilter
generator = ExternalGeneratorFilter(_generator)
generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)


lambdabfilter = cms.EDFilter("PythiaFilter", ParticleID = cms.untracked.int32(5122))
psifilter = cms.EDFilter("PythiaDauVFilter",
        verbose         = cms.untracked.int32(0),
        NumberDaughters = cms.untracked.int32(2),
        MotherID        = cms.untracked.int32(5122),
        ParticleID      = cms.untracked.int32(443),
        DaughterIDs     = cms.untracked.vint32(13, -13),
        MinPt           = cms.untracked.vdouble(1., 1.),
        MinEta          = cms.untracked.vdouble(-3, -3),
        MaxEta          = cms.untracked.vdouble(3, 3)
)
lb0filter = cms.EDFilter("PythiaDauVFilter",
        verbose         = cms.untracked.int32(0),
        NumberDaughters = cms.untracked.int32(2),
        MotherID        = cms.untracked.int32(5122),
        ParticleID      = cms.untracked.int32(3122),
        DaughterIDs     = cms.untracked.vint32(2212, -211),
        MinPt           = cms.untracked.vdouble(1., 1.),
        MinEta          = cms.untracked.vdouble(-2.4, -2.4),
        MaxEta          = cms.untracked.vdouble(2.4, 2.4)
)
decayfilter = cms.EDFilter("PythiaDauVFilter",
	    verbose         = cms.untracked.int32(0),
	    NumberDaughters = cms.untracked.int32(2),
	    MotherID        = cms.untracked.int32(0),
	    ParticleID      = cms.untracked.int32(5122),
        DaughterIDs     = cms.untracked.vint32(443, 3122),
	    MinPt           = cms.untracked.vdouble(1, 1),
	    MinEta          = cms.untracked.vdouble(-2.4, -2.4),
	    MaxEta          = cms.untracked.vdouble( 2.4,  2.4)
)

# Lbrapidityfilter = cms.EDFilter("PythiaFilter",
#                                 ParticleID = cms.untracked.int32(5122),
#                                 MinPt = cms.untracked.double(2.0),
#                                 MaxPt = cms.untracked.double(500.),
#                                 MinRapidity = cms.untracked.double(-2.4),
#                                 MaxRapidity = cms.untracked.double(2.4),
#                             )

ProductionFilterSequence = cms.Sequence(generator*lambdabfilter*decayfilter*lb0filter*psifilter)

''' driver command used
cmsDriver.py Configuration/GEN/python/gen_fragment.py --mc --eventcontent RAWSIM --pileup HiMixGEN --datatier GEN-SIM --conditions 130X_mcRun3_2023_realistic_HI_v18 --beamspot MatchHI --step GEN,SIM --scenario HeavyIons --geometry DB:Extended --era Run3_pp_on_PbPb  --fileout file:GS_out.root --pileup_input "dbs:/MinBias_Drum5F_5p36TeV_hydjet/HINPbPbSpring23GS-130X_mcRun3_2023_realistic_HI_v18-v2/GEN-SIM" --nThreads 8 -n 1000000
'''
