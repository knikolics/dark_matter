from ROOT import TPie, TCanvas, TLegend, gROOT
import math

gROOT.SetStyle('Plain')

hList1 = []
hList2 = []
hList3 = []

# print total neutrons in ArDM for SS Vessel, SS top flange, PMT glass, PMT base, PMT electrode, resistors

totalFlux_U238_sf = [1.09e-10,1.09e-10,3.03767e-11,2.45196e-11,1.09e-10,5.38088e-11] # SS, HiPoly, PMT glass, PMT base, PMT electrode, PMT polyethylene, resistors, Borotron
totalFlux_U238_an = [3.864e-11,3.864e-11,1.45416e-10,5.36462e-11,3.864e-11,3.80755e-10]

totalFlux_Th232_an = [5.167e-11,5.167e-11,6.28144e-11,2.46847e-11,8.11115e-12,2.03839e-12]

totalFlux_U235_an = [0,0,1.23109e-09,0,0,0] # PMT Glass

material = ['SS Vessel','SS top flange','PMT glass','PMT base','PMT electrode','resistors']

activityU238 = [0.0472,0.0472,0.6793,11.1921,0.4175,1.8584]
activityTh232 = [0.017844,0.017844,0.12920,13.246,0.11722,1.91256]

activityU235 = [0.0134833,0.0134833,0.044251667,0.814896667,0.064974,0.166073333]

# grams of element producing 1 Bq
# U235_g = 1.287e-5
# U238_g = 8.040833e-05
# Th232_g = 2.464642e-04
# --> 1 ppb: SF = 1/1e-09
#U238ppb = 80.40833
#Th232ppb = 246.4642
U235ppb = 12.87
U238ppb = 81.9
Th232ppb = 246.464

contaminU235 = []
contaminTh232 = []
contaminU238 = []

contaminU235_err = []
contaminU238_err = []
contaminTh232_err = []

print 'contamination\n'
for iAct in range(len(activityU238)):
    contaminU235.append(activityU235[iAct]*U235ppb)
    contaminU238.append(activityU238[iAct]*U238ppb)
    contaminTh232.append(activityTh232[iAct]*Th232ppb)
    #contaminU235_err.append(activityU235_err[iAct]*U235ppb)
    #contaminU238_err.append(activityU238_err[iAct]*U238ppb)
    #contaminTh232_err.append(activityTh232_err[iAct]*Th232ppb)
    #print 'U238 contamination [ppb]',material[iAct],':',round(contaminU238[iAct],2),'+/-',round(contaminU238_err[iAct],2),'\n'
    #print 'U235 contamination [ppb]',material[iAct],':',round(contaminU235[iAct],2),'+/-',round(contaminU235_err[iAct],2),'\n'
#print 'Th232 contamination [ppb]',material[iAct],':',round(contaminTh232[iAct],2),'+/-',round(contaminTh232_err[iAct],2),'\n'


#---------------------------------------------------------------------
# fractions Borotron neutron shield - S1: E - [50,100], S2: 2keV, FV cuts: r = 345mm && -500mm < z < 450mm
fractionSS_238U_an = 0.00893
fractionSS_238U_sf = 0.00876
fractionSS_232Th_an = 0.00818

fractionTopFlange_238U_an = 0.00566
fractionTopFlange_238U_sf = 0.00554
fractionTopFlange_232Th_an = 0.00542

fractionHVr_238U_an = 0.03321
fractionHVr_238U_sf = 0.03428
fractionHVr_232Th_an = 0.03271

fractionPMTGlass_238U_an = 0.01059
fractionPMTGlass_238U_sf = 0.0108
fractionPMTGlass_232Th_an = 0.0114
fractionPMTGlass_235U_an = 0.01059
fractionPMTGlass_235U_sf = 0.0108

fractionPMTbase_238U_an = 0.00698
fractionPMTbase_238U_sf = 0.00709
fractionPMTbase_232Th_an = 0.00656


fractionPMTelectrode_238U_an = 0.053792 #unchanged!
fractionPMTelectrode_238U_sf = 0.049474 #unchanged!
fractionPMTelectrode_232Th_an = 0.049378 #unchanged!


fraction_U235_an = [0,0,fractionPMTGlass_235U_an,0,0,0]

fraction_U238_an = [fractionSS_238U_an,fractionTopFlange_238U_an,fractionPMTGlass_238U_an,fractionPMTbase_238U_an,fractionPMTelectrode_238U_an,fractionHVr_238U_an]
fraction_U238_sf = [fractionSS_238U_sf,fractionTopFlange_238U_sf,fractionPMTGlass_238U_sf,fractionPMTbase_238U_sf,fractionPMTelectrode_238U_sf,fractionHVr_238U_sf]
fraction_Th232_an = [fractionSS_232Th_an,fractionTopFlange_232Th_an,fractionPMTGlass_232Th_an,fractionPMTbase_232Th_an,fractionPMTelectrode_232Th_an,fractionHVr_232Th_an]

# vol dewar = 143375
# vol Top flange = 37946.9 cm3
# vol PMT electrode = 591 cm3
# vol PMT glass = 6090 cm3
# vol PMT base  = 217 cm3

volumes = [143375,37946.9,6117.48,217.14696,591,113.7532] # SS Vessel, SS top flange, PMT glass, PMT base, PMT electrode, resistors

exposure = raw_input('how many days exposure?\n')

allNeutrons = 0
print 'total number of neutrons for ',exposure,' days of exposure\n'
for iVol in range(len(volumes)):
    totFluxIntegral_U238_an = totalFlux_U238_an[iVol] * volumes[iVol] * contaminU238[iVol] * fraction_U238_an[iVol]*24*3600
    totFluxIntegral_U238_sf = totalFlux_U238_sf[iVol] * volumes[iVol] * contaminU238[iVol] * fraction_U238_sf[iVol]*24*3600
    totFluxIntegral_Th232_an = totalFlux_Th232_an[iVol] * volumes[iVol] * contaminTh232[iVol] * fraction_Th232_an[iVol] * 24*3600
    if material[iVol]=='PMT glass':
       totFluxIntegral_U235_an = totalFlux_U235_an[iVol] * volumes[iVol] * contaminU235[iVol] * fraction_U235_an[iVol] * 24*3600
    else:
       totFluxIntegral_U235_an = 0
    totalNeutrons = (totFluxIntegral_U235_an + totFluxIntegral_U238_an + totFluxIntegral_U238_sf + totFluxIntegral_Th232_an)*int(exposure)
    print 'neutrons from ',material[iVol],':',round(totalNeutrons,2),'\n'
    allNeutrons += totalNeutrons

print 'total number of neutrons:',round(allNeutrons,2)

raw_input()

