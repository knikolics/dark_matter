from ROOT import TFile, gStyle, TCanvas, TH1D, TF1, TLatex, TCanvas
import math
import sys

gStyle.SetOptStat(11)

f = TFile(sys.argv[1],'r')
c = TCanvas('c','',800,640)
c.cd()

hf = f.Get('fgam')
hf.Rebin(2)
#hf.SetStats(11)
hf.SetLineColor(1)
hf.SetXTitle('CR')
hf.SetYTitle('Entries')
hf.Draw()

ff = TF1('ff','gaus',0,0.5)
hf.Fit('ff','r')

text = TLatex()
text.SetNDC()
#text.DrawLatex(0.55,0.8,'total entries = %g'%(round(hf.GetEntries(),1)))
text.DrawLatex(0.55,0.75,'mean = %g'%(round(ff.GetParameter(1),2)))
text.DrawLatex(0.55,0.7,'#sigma = %g'%(round(ff.GetParameter(2),2)))

c.Update()

raw_input()
