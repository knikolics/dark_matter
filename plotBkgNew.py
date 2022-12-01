from ROOT import TFile, TH1D, TCanvas, THStack, TLegend, gStyle, TPie
from datetime import datetime
from time import strftime
from array import array
import numpy as np
import sys

dt = np.dtype('d')

gStyle.SetNumberContours(99)
gStyle.SetOptStat('e')

def runTime(hist):
   startTime = hist.GetBinContent(1)
   stopTime = hist.GetBinContent(2)
   timeSpan = stopTime-startTime
   duration = datetime.fromtimestamp(timeSpan).strftime('%H %M %S') # duration of run in s
   return timeSpan

f11 = TFile('testData.root','r')
f_u238 = [TFile('SSVessel_U238_histo.root','r'),TFile('TopFlange_U238_histo.root','r'),TFile('PMT_Glass_U238_histo.root','r'),TFile('PMT_Base_U238_histo.root','r')]
f_th232 = [TFile('SSVessel_Th232_histo.root','r'),TFile('TopFlange_Th232_histo.root','r'),TFile('PMT_Glass_Th232_histo.root','r'),TFile('PMT_Base_Th232_histo.root','r')]
f_k40 = [TFile('PMT_Glass_K40_histo.root','r'),TFile('PMT_Base_K40_histo.root','r')]

fAr39 = TFile('LArFV_Ar39_histo.root','r')
f_co60 = [TFile('SSVessel_Co60_histo.root','r'),TFile('SS_TopFlange_Co60_histo.root','r')]

# data : total run timer in s
firstRun = 29100 
lastRun = 29115
duration  = 0
for iRun in range(firstRun,lastRun+1):
   h = f11.Get('timeStamp_%i'%(iRun))
   if not h:
      continue
   else:
      duration += runTime(h)

print 'total integrated time: ',duration,'s\n'
sfData = 1./duration

hPE_u238 = []
hPE_th232 = []
hPE_k40 = []
hPE_co60 = []
hTTR_u238 = []
hTTR_th232 = []
hTTR_k40 = []
hTTR_co60 = []

hdataPE = f11.Get('totPE')
hdataPE.Scale(sfData)
hdataTTR =  f11.Get('totPE_TTR_ext')
#hdataTTR.Scale(sfData)

hAr39PE = fAr39.Get('h_totPE')
hAr39TTR = fAr39.Get('h_ttrPE')
acceptanceLAr = hAr39PE.GetEntries()/2e5

#hCo60PE = fCo60.Get('h_totPE')
#hCo60TTR = fCo60.Get('h_ttrPE')
#acceptance_co60 = hCo60PE.GetEntries()/1e6
#print 'acceptance_co60 ',acceptance_co60,'\n'

hAr39PE.Rebin(8)
acceptance_u238 = []
acceptance_th232 = []
acceptance_k40 = []
acceptance_co60 = []

for iHist in range(len(f_u238)):
    hPE_u238.append(f_u238[iHist].Get('h_totPE'))
    if (iHist < 2): 
       #print 'hPE_u238[iHist].GetEntries() ', hPE_u238[iHist].GetEntries(),'\n'
       acceptance_u238.append(hPE_u238[iHist].GetEntries()/1e6)
    else:
       acceptance_u238.append(hPE_u238[iHist].GetEntries()/1.44e6)
    hPE_u238[iHist].Rebin(8)
    hPE_th232.append(f_th232[iHist].Get('h_totPE'))
    if (iHist < 2):
       acceptance_th232.append(hPE_th232[iHist].GetEntries()/1e6)
    else:
       acceptance_th232.append(hPE_th232[iHist].GetEntries()/1.44e6)
    hPE_th232[iHist].Rebin(8)
    hTTR_u238.append(f_u238[iHist].Get('h_ttrPE'))
    hTTR_th232.append(f_th232[iHist].Get('h_ttrPE'))

for iHist in range(len(f_k40)):
    hPE_k40.append(f_k40[iHist].Get('h_totPE'))
    acceptance_k40.append(hPE_k40[iHist].GetEntries()/1.44e6)
    hPE_k40[iHist].Rebin(8)
    hTTR_k40.append(f_k40[iHist].Get('h_ttrPE'))
    hPE_co60.append(f_co60[iHist].Get('h_totPE'))
    acceptance_co60.append(hPE_co60[iHist].GetEntries()/1e6)
    hPE_co60[iHist].Rebin(8)
    hTTR_co60.append(f_co60[iHist].Get('h_ttrPE'))

N_A = 6.022e23 # Avogadro constant
activityU238 = 2.94e6 # s-1/mole; rate per mole = N_A * 0.693/tau; tau_U238 = 4.5e9a
activityTh232 = 9.385e5 # s-1/mole; rate per mole = N_A * 0.693/tau; tau_Th232 = 1.41e10 a

gamU238 = 10 
gamTh232 = 8

contaminationSS_u238 = 3.87 # ppb
contaminationSS_th232 = 4.4 # ppb
massDewar = 1143.36 # kg
activitySS_u238 = 0.047 #Bq/kg
activitySS_th232 = 0.019
activitySS_co60 = 0.0145 # Bq/kg
massDewar_u238 = massDewar*(contaminationSS_u238*1e-9)
massDewar_th232 = massDewar*(contaminationSS_th232*1e-9)
rateDewar_u238 = gamU238*activitySS_u238*massDewar #activitySS_u238*massDewar_u238/0.238
rateDewar_th232 = gamTh232*activitySS_th232*massDewar #activitySS_th232*massDewar_th232/0.232
rateDewar_co60 = activitySS_co60*massDewar

#activityDewar = 0.068 # Bq/kg
massTopFlange = 303.58 # kg
activityTopFlange = 0.047 # Bq/kg
massTopFlange_u238 = massTopFlange*(contaminationSS_u238*1e-9)
massTopFlange_th232 = massTopFlange*(contaminationSS_th232*1e-9)
rateTopFlange_u238 = gamU238*activitySS_u238*massTopFlange #activitySS_u238*massTopFlange_u238/0.238
rateTopFlange_th232 = gamTh232*activitySS_th232*massTopFlange #activitySS_th232*massTopFlange_th232/0.232
rateTopFlange_co60 = activitySS_co60*massTopFlange

contaminationPMTGlass = 55.63 # ppb
massPMTGlass = 13.53 # kg
activityPMTGlass_u238 = 0.679 # Bq/kg
activityPMTGlass_th232 = 0.129 # Bq/kg
ratePMTGlass_u238 = gamU238*activityPMTGlass_u238*massPMTGlass
ratePMTGlass_th232 = gamTh232*activityPMTGlass_th232*massPMTGlass

massPMTBase = 0.461 # kg 
activityPMTBase_u238 = 11.19 # Bq/kg
activityPMTBase_th232 = 13.246 # Bq/kg
ratePMTBase_u238 = gamU238*activityPMTBase_u238*massPMTBase
ratePMTBase_th232 = gamTh232*activityPMTBase_th232*massPMTBase

activityPMTGlass_k40 = 0.45 # Bq/kg
ratePMTGlass_k40 = activityPMTGlass_k40*massPMTGlass

activityPMTBase_k40 = 18.28 # Bq/kg
ratePMTBase_k40 = activityPMTBase_k40*massPMTBase

rate_u238 = [rateDewar_u238,rateTopFlange_u238,ratePMTGlass_u238,ratePMTBase_u238]
rate_th232 = [rateDewar_th232,rateTopFlange_th232,ratePMTGlass_th232,ratePMTBase_th232]
rate_k40 = [ratePMTGlass_k40,ratePMTBase_k40]
rate_co60 = [rateDewar_co60,rateTopFlange_co60]

print 'rate SS Vessel U238',rateDewar_u238,'\n'
print 'rate SS Vessel Th232',rateDewar_th232,'\n'
print 'rate SS Vessel Co60',rateDewar_co60,'\n'
print 'rate SS Top Flange U238',rateTopFlange_u238,'\n'
print 'rate SS Top Flange Th232',rateTopFlange_th232,'\n'
print 'rate PMT Base U238 ',ratePMTBase_u238,'\n'
print 'rate PMT Base Th232 ',ratePMTBase_th232,'\n'
print 'rate PMT Glass U238 ',ratePMTGlass_u238,'\n'
print 'rate PMT Glass Th232 ',ratePMTGlass_th232,'\n'
print 'rate PMT Glass K40 ',ratePMTGlass_k40,'\n'
print 'rate PMT Base K40 ',ratePMTBase_k40,'\n'

cPie = TCanvas('cPie','',800,640)
cPie.cd()

rates = array('d',[rateDewar_u238,rateDewar_th232,rateTopFlange_u238,rateTopFlange_th232,ratePMTGlass_u238,ratePMTGlass_th232,ratePMTBase_u238,ratePMTBase_th232,ratePMTGlass_k40,ratePMTGlass_k40,rateDewar_co60,rateTopFlange_co60])
nvals = len(rates)
entries = ['SS Vessel U238','SS Vessel Th232','Top Flange U238','Top Flange Th232','PMT Glass U238','PMT Glass Th232','PMT Base U238','PMT Base Th232','PMT Glass K40','PMT Base K40','SS Vessel Co60','Top Flange Co60']
ncolors = array('i',[2,3,4,5,6,7,28,30,42,46,38,41])

pie = TPie('pie','',nvals,rates,ncolors)
#pie.SetAngularOffset(1.)
#pie.SetEntryRadiusOffset( 4, 0.1)
#pie.SetEntryFillStyle(1,3030)
for iEntry in range(nvals):
    pie.SetEntryLabel(iEntry,'%s'%(entries[iEntry]))

pie.SetLabelsOffset(.01)
pie.SetRadius(.2)
#pie.SetLabelFormat("#splitline{%val (%perc)}{%txt}")
pie.SetLabelFormat("%perc")
#pie.SetCircle(.5,.45,.3)
#pie.Draw('3d t')
pie.Draw()
#legpie = TLegend(0.6,0.7,0.85,0.92)
legpie = pie.MakeLegend()
legpie.SetNColumns(2)

#legpie.Draw()
cPie.Update()

activityAr39 = 0.94 # Bq/kg
#massLAr = 1820
massLAr = 885.5

sf_u238_Dewar = gamU238/(1e6/rateDewar_u238) #(activitySS_u238*massDewar)/(1e6)
sf_th232_Dewar = gamTh232/(1e6/rateDewar_th232) #(activitySS_th232*massDewar)/(1e6)
sf_co60_Dewar = 1/(1e6/rateDewar_co60)

sf_u238_TopFlange = gamU238/(1e6/rateTopFlange_u238) #(activitySS_u238*massTopFlange)/(1e6)
sf_th232_TopFlange = gamTh232/(1e6/rateTopFlange_th232) #(activitySS_th232*massTopFlange)/(1e6)
sf_co60_TopFlange = 1/(1e6/rateTopFlange_co60)

sf_u238_PMTGlass = gamU238/(1.44e6/ratePMTGlass_u238) #(activityPMTGlass_u238*massPMTGlass)/(1.44e6)
sf_th232_PMTGlass = gamTh232/(1.44e6/ratePMTGlass_th232)  #(activityPMTGlass_th232*massPMTGlass)/(1.44e6)

sf_u238_PMTBase = gamU238/(1.44e6/ratePMTBase_u238) #(activityPMTBase_u238*massPMTBase)/(1.44e6)
sf_th232_PMTBase = gamTh232/(1.44e6/ratePMTBase_th232) # (activityPMTBase_th232*massPMTBase)/(1.44e6)

sf_k40_PMTGlass = 1/(1.44e6/ratePMTGlass_k40)
sf_k40_PMTBase = 1/(1.44e6/ratePMTBase_k40)


#activityAr39 = 5.52e13 # s-1/mole; rate per mole = N_A * 0.693/tau; tau_Ar39 = 239 a
rateLAr = activityAr39*massLAr*acceptanceLAr
sf_LAr_A39 = 1/(2e5/rateLAr) #(activityAr39*massLAr)/(2e5) # 5 times fewer events in the sim for Ar39
print 'rateLAr ',rateLAr,'\n'

sf_u238 = [sf_u238_Dewar,sf_u238_TopFlange,sf_u238_PMTGlass,sf_u238_PMTBase]
sf_th232 = [sf_u238_TopFlange,sf_th232_TopFlange,sf_th232_PMTGlass,sf_th232_PMTBase]
sf_k40 = [sf_k40_PMTGlass,sf_k40_PMTBase]
sf_co60 = [sf_co60_Dewar,sf_co60_TopFlange]

component = ['SS Vessel','SS top flange','PMT Glass','PMT Base']

hs1 = THStack('hs1','')
leg = TLegend(0.6,0.7,0.85,0.92)
leg.SetNColumns(2)

rateMC = rateLAr
for iHist in range(len(hPE_u238)):
   hPE_u238[iHist].SetLineColor(1)
   hPE_u238[iHist].SetFillColor(2+iHist)
   hPE_u238[iHist].Scale(sf_u238[iHist])
   hs1.Add(hPE_u238[iHist])
   leg.AddEntry(hPE_u238[iHist],'%s, U238'%(component[iHist]),'f')
   hPE_th232[iHist].SetLineColor(1)
   hPE_th232[iHist].SetFillColor(6+iHist)
   hPE_th232[iHist].Scale(sf_th232[iHist])
   hs1.Add(hPE_th232[iHist])
   leg.AddEntry(hPE_th232[iHist],'%s, Th232'%(component[iHist]),'f')
   print 'rate*acceptance_u238[iHist] ',rate_u238[iHist]*acceptance_u238[iHist], ' U238', component[iHist],'\n'
   print 'rate*acceptance_th232[iHist] ',rate_th232[iHist]*acceptance_th232[iHist], ' Th232', component[iHist],'\n'
   rateMC += rate_u238[iHist]*acceptance_u238[iHist] + rate_th232[iHist]*acceptance_th232[iHist]
   #rateMC += hPE_u238[iHist].Integral()+hPE_th232[iHist].Integral()

#hCo60PE.SetLineColor(1)
#hCo60PE.SetFillColor(31)
#hCo60PE.Scale(sf_co60_Dewar)
#leg.AddEntry(hCo60PE,'Co60 Vessel','f')

#hs1.Add(hCo60PE)

for iHist in range(len(hPE_k40)):
   hPE_k40[iHist].SetLineColor(1)
   hPE_k40[iHist].SetFillColor(41+iHist)
   hPE_k40[iHist].Scale(sf_k40[iHist])
   hs1.Add(hPE_k40[iHist])
   print 'rate*acceptance_k40[iHist] ',rate_k40[iHist]*acceptance_k40[iHist],' K40',component[iHist+2],'\n'
   leg.AddEntry(hPE_k40[iHist],'%s, K40'%(component[2+iHist]),'f')
   hPE_co60[iHist].SetLineColor(1)
   hPE_co60[iHist].SetFillColor(44+iHist)
   hPE_co60[iHist].Scale(sf_co60[iHist])
   hs1.Add(hPE_co60[iHist])
   leg.AddEntry(hPE_co60[iHist],'%s, Co60'%(component[iHist]),'f')
   print 'rate*acceptance_c60[iHist] ',rate_co60[iHist]*acceptance_co60[iHist],' Co60',component[iHist],'\n'
   rateMC += rate_k40[iHist]*acceptance_k40[iHist]+rate_co60[iHist]*acceptance_co60[iHist]

hAr39PE.SetLineColor(1)
hAr39PE.SetFillColor(30)
hAr39PE.Scale(sf_LAr_A39)
leg.AddEntry(hAr39PE,'Ar39','f')

hs1.Add(hAr39PE)


#hdataPE.Scale(sfData)
#hdataPE.SetMarkerStyle(20)
#hdataPE.SetMarkerSize(1)

print 'total rate data: ',hdataPE.Integral(),' s-1\n'
print 'total rate MC: ', rateMC,' s-1\n'

c1 = TCanvas('c1','',800,640)
#c1.SetLogy()
hs1.Draw()
#hdataPE.Draw('p same')
leg.Draw()
c1.Update()

c2 = TCanvas('c2','',800,640)
c2.cd()

leg1 = TLegend(0.6,0.7,0.85,0.92)
leg1.SetNColumns(2)

for iHist in range(len(hPE_u238)):
   #hTTR_u238[iHist].Rebin2D(2,1)
   hTTR_u238[iHist].Scale(sf_u238[iHist])
   hTTR_u238[iHist].SetMarkerColor(2+iHist)
   hTTR_u238[iHist].SetFillColor(2+iHist)
   hTTR_u238[iHist].Draw('same')
   leg1.AddEntry(hTTR_u238[iHist],'%s, U238'%(component[iHist]),'f')
   #hTTR_th232[iHist].Rebin2D(2,1)
   hTTR_th232[iHist].Scale(sf_th232[iHist])
   hTTR_th232[iHist].SetMarkerColor(6+iHist)
   hTTR_th232[iHist].SetFillColor(6+iHist)
   hTTR_th232[iHist].Draw('same')
   leg1.AddEntry(hTTR_th232[iHist],'%s, Th232'%(component[iHist]),'f')

for iHist in range(len(hPE_k40)):
   #hTTR_k40[iHist].Rebin2D(2,1)
   hTTR_k40[iHist].Scale(sf_k40[iHist])
   hTTR_k40[iHist].SetMarkerColor(41+iHist) 
   hTTR_k40[iHist].SetFillColor(41+iHist) 
   hTTR_k40[iHist].Draw('same')
   leg1.AddEntry(hPE_k40[iHist],'%s, K40'%(component[2+iHist]),'f') 

#hAr39TTR.Rebin2D(2,1)
hAr39TTR.SetMarkerColor(30)
hAr39TTR.SetFillColor(30)
hAr39TTR.Draw('same')
leg1.AddEntry(hAr39TTR,'Ar39','f')
leg1.Draw()
c2.Update()

c3 = TCanvas('c3','',800,640)
c3.cd()
hsum = hTTR_u238[0].Clone()
binsX =  hTTR_u238[0].GetNbinsX()
binsY =  hTTR_u238[0].GetNbinsY()

for iBinX in range(1,binsX+1):
   for iBinY in range(1,binsY+1):
       binContent = hAr39TTR.GetBinContent(iBinX,iBinY)
       for iHist in range(len(hTTR_u238)):
          binContent += hTTR_u238[iHist].GetBinContent(iBinX,iBinY)+hTTR_th232[iHist].GetBinContent(iBinX,iBinY)
       hsum.SetBinContent(iBinX,iBinY,binContent)

for iBinX in range(1,binsX+1):
   for iBinY in range(1,binsY+1):
       binContent = hsum.GetBinContent(iBinX,iBinY)
       for iHist in range(len(hPE_k40)):
          binContent += hTTR_k40[iHist].GetBinContent(iBinX,iBinY)
       hsum.SetBinContent(iBinX,iBinY,binContent)


hsum.SetYTitle('TTR')
hsum.SetXTitle('total light (PE)')
hsum.Draw('colz')
c3.Update()

c4 = TCanvas('c4','',800,640)
c4.cd()
hdataTTR.Rebin2D(4,2)
hdataTTR.Draw('colz')
c4.Update()

c5 = TCanvas('c5','',800,640)
c5.cd()
#hdataPE.SetMarkerStyle(20)
hdataPE.SetYTitle('Rate [Hz]')
hdataPE.SetXTitle('total light (PE)')
hdataPE.SetLineColor(1)
hdataPE.Draw()
c5.Update()

raw_input()
