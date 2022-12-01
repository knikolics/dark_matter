from ROOT import TFile, TH1, TCanvas, TLegend, gROOT
import math
import sys

gROOT.SetStyle('Plain')

#infile = raw_input('choose between SS, Ar or Poly\n')

hList1 = []
hList2 = []

def acceptance(hist):
   h = hist.Clone()
   nbinsX = hist.GetNbinsX()
   for i in range(nbinsX):
      totIntegral = hist.Integral()
      acc = hist.Integral(i,nbinsX)/totIntegral
      h.SetBinContent(i+1,1-acc)
   hList2.append(h)

tankVol = 1.50896e5 # cm^3

totalFlux_U238_sf = [1.09e-10,1.282e-11,1.226e-11] # SS, HiPoly, resistors
totalFlux_U238_an = [3.864e-11,1.367e-11,4.315e-11] # SS, HiPoly, resistors
totalFlux_Th232_an = [5.167e-11,5.829e-12,2.630e-11] # SS, HiPoly, resistors

# contamination [Bq/kg]
material = ['SS (Pa-234m)','HiPoly (Pa-234m)','PMT glass (average)','PMT base (average)','PMT electrode (Pa-234m)','PMT polyethylene (Pa-234m)','resistors (average)','Perlite (average)']
activityU238 = [0.32412,0.14674,0.67934,11.19209,1.9743,2.9976,1.85843,52.80022]
activityTh232 = [0.01872,0.01284,0.12920,13.246,0.11722,0.15482,1.91256,54.58463]

# grams of element producing 1 Bq
# U238_g = 8.040833e-05
# Th232_g = 2.464642e-04
# --> 1 ppb: SF = 1/1e-09
U238ppb = 8.040833e04
Th232ppb = 2.464642e05

contaminU238 = []
contaminTh232 = []
for iAct in range(len(activityU238)):
    contaminU238.append(activityU238[iAct]*U238ppb)
    print 'contamination [ppb] of ', material[iAct],' with U-238: ',contaminU238[iAct],'\n'
    contaminTh232.append(activityTh232[iAct]*Th232ppb)
    print 'contamination [ppb] of ', material[iAct],' with Th-232: ',contaminTh232[iAct],'\n'

"""
if infile=='SS':
   #name = ['histos_SS_232Th_alphaN.root','histos_SS_238U_alphaN.root','histos_SS_238U_spontaneousFission.root']
   name = ['histos_neutron_Poly_238U_sf.root','histos_neutron_SS_238U_sf.root']
   legend = 'Stainless steel'
elif infile=='Ar':
   name = ['histos_Ar_232Th_an.root','histos_Ar_238U_an.root','histos_Ar_238U_sf.root']
   legend = 'Ar'
elif infile=='Poly':
   name = ['histos_Poly_232Th_an.root','histos_Poly_238U_an.root','histos_Poly_238U_sf.root']
   legend = "PE neutron shield"
else:
   print 'hey, i said: choose between SS or Ar!\n'
"""

f =[]
legend = 'Stainless steel'

#for i in range(len(name)):
for i in range(1,len(sys.argv)):
   #f.append(TFile(name[i],'read'))
   f.append(TFile(sys.argv[i],'read'))

for j in range(len(f)):
   #erecoil = f[j].Get('radialFid')
   #erecoil = f[j].Get('zFid')
   erecoil = f[j].Get('singleErecoil')
   hList1.append(erecoil)
   fraction = hList1[j].Integral(20,300)/1000   

totFluxIntegral = totalFlux_U238_an[0] * tankVol * contaminU238[0] * fraction 
print 'SS: neutrons per second ', totFluxIntegral,'\n'

c1 = TCanvas('c1','',800,600)

percent = hList1[0].GetEntries()/1000
print 'single scatter to total ', hList1[0].GetEntries()/100000,'\n'

c1.cd()
for k in range(len(hList1)):
  if k==0:
    hList1[k].SetTitle('%s: single scatter nuclear recoil events: %g %%'%(legend,round(percent,1)))
    hList1[k].SetXTitle('E_{recoil} (keV)')
    hList1[k].SetYTitle('Entries / (keV)')
    hList1[k].SetStats(0)
    hList1[k].SetLineWidth(2)
    hList1[k].SetLineColor(k+2)
    hList1[k].Draw()
  else:
    hList1[k].SetLineWidth(2)
    hList1[k].SetLineColor(k+2)
    hList1[k].Draw('same')

leg = TLegend(0.7,0.7,0.95,0.92)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
#leg.AddEntry(hList1[0],'232Th (#alpha,n)','l')
#leg.AddEntry(hList1[1],'238U (#alpha,n)','l')
#leg.AddEntry(hList1[2],'238U spont. fission','l')
#leg.Draw()
c1.Update()

c2 = TCanvas('c2','',800,600)
c2.cd()

for n in range(len(hList1)):
   acceptance(hList1[n])

for j in range(len(hList2)):
   if j==0: 
      hList2[j].SetTitle('%s'%(legend))
      hList2[j].SetXTitle('E_{threshold} (keV)')
      hList2[j].SetYTitle('Background rejection')
      hList2[j].SetStats(0)
      hList2[j].SetMarkerStyle(20)
      hList2[j].SetMarkerSize(0.8)
      hList2[j].SetLineColor(j+2)
      hList2[j].Draw()
   else: 
      hList2[j].SetStats(0)
      hList2[j].SetMarkerStyle(20)
      hList2[j].SetMarkerSize(0.8)
      hList2[j].SetLineColor(j+2)
      hList2[j].Draw('same') 

leg.Draw()
c2.Update()

raw_input()
