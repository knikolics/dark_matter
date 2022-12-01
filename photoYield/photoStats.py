from ROOT import TFile, TH1D, TRandom3, TCanvas
import numpy as np

dt = np.dtype('d')

hnuc = TH1D('fnuc','',100,0,1.0)
hgam = TH1D('fgam','',100,0,1.0)
hdecspnuc = TH1D('decspnuc','',100,0,3000)
hdecspgam = TH1D('decspgam','',100,0,3000)

fnuc = 0
fgam = 0

def ScintGammaTime(nuclear):
   # time constants for Argon, singlet and triplet state of excimer in ns
   tau_singlet=6
   tau_triplet=1590
   if nuclear:
     i1overi3 = 3 # from Boulay, Hime arXiv:astro-ph/0411358
   else:
     i1overi3 = 0.3
   gRandom = TRandom3(0)
   singtrip = gRandom.Rndm()
   probi1 = 1.0/(1.0+(1.0/i1overi3))
   if singtrip<probi1:
     tau=tau_singlet
   else:
     tau=tau_triplet
   time = gRandom.Exp(tau)
   return time

def ScintTimeRej(nGam, fnuc, fgam):
   tCut = 50 # in ns
   abovenuc=0
   abovegam=0
   for iGamma in range(nGam):
      tnuc = ScintGammaTime(True)
      hdecspnuc.Fill(tnuc)
      tgam = ScintGammaTime(False)
      hdecspgam.Fill(tgam)
      if tnuc<tCut: 
        abovenuc += 1 # detected prompt as n induced g
      if tgam<tCut:
        abovegam += 1 # detected prompt as g induced g
   fnuc = abovenuc/nGam
   fgam = abovegam/nGam

fCut = 0.82

c1 = TCanvas('c1','',1500,350)
c1.Divide(3,1)

print 'nGam   survnuc   survgam\n'

for nGam in range(4,40):
  sfnuc = 0
  sfgam = 0
  ntot = 0
  while (sfgam<100000):
     ScintTimeRej(nGam, fnuc, fgam)
     if(fnuc>fCut):
        sfnuc += 1 # ratio above tcut -> call it a n
     if(fgam<fCut):
        sfgam += 1 # ratio below tcut -> call it a fake neutron
     hnuc.Fill(fnuc)
     hgam.Fill(fgam)
     ntot += 1
  survnuc = np.array(sfnuc/ntot,dtype=dt)
  survgam = np.array(sfgam/ntot,dtype=dt)
  print 'ntot ', ntot,'\n'
  print nGam,'   ',survnuc,'    ',survgam,'\n'


c1.cd(1)
hnuc.Draw()
hgam.Draw('same')

c1.cd(2)
hdecspnuc.Draw()

c1.cd(3)
hdecspgam.Draw()

c1.Update()

raw_input()
