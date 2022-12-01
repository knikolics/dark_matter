from ROOT import TFile, TH1D, TCanvas, THStack, TLegend
import sys

f11 = TFile(sys.argv[1],'r') # Data
f1 = TFile(sys.argv[2],'r') # SS Dewar
f2 = TFile(sys.argv[3],'r') # SS Top Flange
f3 = TFile(sys.argv[4],'r') # PMT Glass

hdata = f11.Get('totPE')
h1 = f1.Get('h_totPE')
h2 = f2.Get('h_totPE')
h3 = f3.Get('h_totPE')

httr =  f11.Get('totPE_TTR_ext')
h11 = f1.Get('h_ttr')
h22 = f2.Get('h_ttr')
h33 = f2.Get('h_ttr')
h1.Rebin(4)
h2.Rebin(4)
h3.Rebin(4)

massDewar = 1143.36 # kg
activityDewar = 0.068 # Bq/kg
massTopFlange = 303.58 # kg
activityTopFlange = 0.068 # Bq/kg
massPMTGlass = 13.53 # kg
activityPMTGlass = 1.337 # Bq/kg
massTot = massDewar+massTopFlange+massPMTGlass 
sf_Dewar = activityDewar*massDewar/massTot
sf_TopFlange = activityTopFlange*massTopFlange/massTot
sf_PMTGlass = activityPMTGlass*massPMTGlass/massTot


hs1 = THStack('hs1','')
h1.SetLineColor(1)
h1.SetFillColor(2)
h1.Scale(sf_Dewar)
h2.SetLineColor(1)
h2.SetFillColor(4)
h2.Scale(sf_TopFlange)
h3.SetLineColor(1)
h3.SetFillColor(8)
h3.Scale(sf_PMTGlass/0.36)

inData = hdata.Integral(200,1000)
inMC = h1.Integral(200,1000)+h2.Integral(200,1000)+h3.Integral(200,1000)
sf_Data = inData/inMC
print 'sf_Data ',sf_Data
hdata.Scale(sf_Data)
hdata.SetMarkerStyle(20)
hdata.SetMarkerSize(1)

hs1.Add(h1)
hs1.Add(h2)
hs1.Add(h3)

leg = TLegend(0.6,0.7,0.85,0.92)
#leg.AddEntry(hdata,'Data','p')
leg.AddEntry(h1,'SS Dewar','f')
leg.AddEntry(h2,'SS Top Flange','f')
leg.AddEntry(h3,'PMT Glass','f')

c1 = TCanvas('c1','',800,640)
#c1.SetLogy()
hs1.Draw()
#hdata.Draw('p same')
leg.Draw()
c1.Update()

h11.Rebin2D(4,1)
h11.Scale(sf_Dewar)
h11.SetMarkerColor(2)
h22.Rebin2D(4,1)
h22.Scale(sf_TopFlange)
h22.SetMarkerColor(4)
h33.Rebin2D(4,1)
h33.Scale(sf_PMTGlass/0.36)
h33.SetMarkerColor(8)

c2 = TCanvas('c2','',800,640)
c2.cd()
#hs2.Draw()
h11.Draw()
h22.Draw('same')
h33.Draw('same')
c2.Update()

c3 = TCanvas('c3','',800,640)
c3.cd()
hsum = h11.Clone()
binsX =  h11.GetNbinsX()
binsY =  h11.GetNbinsY()

for iBinX in range(1,binsX+1):
   for iBinY in range(1,binsY+1):
       binContent = h11.GetBinContent(iBinX,iBinY)+h22.GetBinContent(iBinX,iBinY)+h33.GetBinContent(iBinX,iBinY)
       hsum.SetBinContent(iBinX,iBinY,binContent)

hsum.Draw('colz')
c3.Update()

c4 = TCanvas('c4','',800,640)
c4.cd()
httr.Rebin2D(4,2)
httr.Draw('colz')
c4.Update()

raw_input()
