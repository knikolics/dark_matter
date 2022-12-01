from ROOT import TFile, TH1F, TCanvas

f = TFile('histos_Fprompt-0.62.root','r')
h = f.Get('decspnuc')

nbins = h.GetNbinsX()

def compRatio(limit):
  fast = h.Integral(limit-9,limit)
  slow = h.Integral(limit,nbins)
  cr = fast/(fast+slow)
  return cr

hist = TH1F('hist','',nbins-9,0,nbins-9)

for iBin in range(9,nbins): # 500 bins from 0 to 3000 --> 6ns per bin
   tempCR = compRatio(iBin)
   hist.SetBinContent(iBin-8,tempCR)

c = TCanvas('c','',800,640)
hist.Draw()
c.Update()

raw_input()
