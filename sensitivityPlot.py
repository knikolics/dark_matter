from ROOT import TF1, TH2D, TGraph, TCanvas, gStyle, TLegend, TF1
from array import array
import numpy as np
import xml.etree.ElementTree as ET
import sys
from cmath import sqrt, pi
#from scipy import special as sci

dt = np.dtype('d')

curves = []
name = []

def theoryCurve(xmlFile):
   npoints = 0
   xy = []
   xCoord = array('d',[])
   yCoord = array('d',[])
   xmldoc = ET.parse(xmlFile)
   limit = xmldoc.getroot()
   name.append(limit[1].text)
   points = limit[3].text #'data_values'
   points = points[2:]
   points = points[:-2]
   points = points.replace(',',';')
   points = points.translate(None,'][')
   xy = (points).split(';')
   npoints = len(xy)
   coord = 0
   for i in range(npoints):
      coord = xy[i].split()
      if float(coord[1]) > 1e-15:
         SF = 1e-36
      else:
         SF = 1
      xCoord.append(np.array(coord[0],dtype=dt))
      yCoord.append(np.array(coord[1],dtype=dt)*SF)
   theory = TGraph(npoints,xCoord,yCoord)
   curves.append(theory)
   theory = 0
   del xy
   del xCoord
   del yCoord

for i in range(1,len(sys.argv)):
   filename = sys.argv[i]
   theoryCurve(filename)

#-----analytical computation
c = 3*1e8  #speed of light
#R0 = 1     #total event rate per unit mass (events/(kg*d)
R0 = 0.9948     #total event rate per unit mass (events/(kg*d)
N0 = 6.022e23 #Avogadro number (mol^-1)
c1 = 0.751
c2 = 0.561

v0 = 230e3 #most probable incident velocity (m/s)
v0_cmd = v0*100*24*3600 # incident velocity (cm/d)
v0_prob = v0/c 
rhoW = 0.4 #WIMP density(GeV*c^-2*cm^-3)
M_nuc = 0.932 #(GeV/c^2)
M_Ar = 39.9  #g/mol
sqrtA = np.real(sqrt(M_Ar))
MT = M_Ar*M_nuc #target mass in GeV/c^2
N0_kg = N0*1000/M_Ar #Avogadro number in kg^-1
qfact = pow(2*M_nuc*M_Ar,0.5)/197.3  #momentum transfer factor
rn = pow(pow((1.23*pow(M_Ar,1/3)-0.6),2)+23.03*0.5*0.52-5*0.9*0.9,0.5) #nuclear radius in solid-sphere-approximation (fm)
s = 0.9 #skin thickness of sphere (fm)
sqrtPi = np.real(sqrt(pi))

ERange = raw_input('Limited energy range? y/n ')

if ERange=='n':
   cs_Ar = TF1('cs_Ar','2*[11]*[0]*[1]/([2]*[3]*[4]*[5]**2*(4*x*[6]/((x+[6])**2)))*(1/(3*(sin([7]*pow(0.5*x*1e6*[9]**2*(4*x*[6]/((x+[6])**2)),0.5)*[8])-[7]*pow(0.5*x*1e6*[9]**2*(4*x*[6]/((x+[6])**2)),0.5)*[8]*cos([7]*pow(0.5*x*1e6*[9]**2*(4*x*[6]/((x+[6])**2)),0.5)*[8]))/([7]*pow(0.5*x*1e6*[9]**2*(4*x*[6]/((x+[6])**2)),0.5)*[8])**3*exp(-([7]*pow(0.5*x*1e6*[9]**2*(4*x*[6]/((x+[6])**2)),0.5)*[10])**2/2))**2)/100000',0,1000)
   cs_Ar.SetParameter(0,M_nuc)
   cs_Ar.SetParameter(1,R0)
   cs_Ar.SetParameter(2,N0_kg)
   cs_Ar.SetParameter(3,rhoW)
   cs_Ar.SetParameter(4,v0_cmd)
   cs_Ar.SetParameter(5,M_Ar)
   cs_Ar.SetParameter(6,MT)
   cs_Ar.SetParameter(7,qfact)
   cs_Ar.SetParameter(8,rn)
   cs_Ar.SetParameter(9,v0_prob)
   cs_Ar.SetParameter(10,s)
   cs_Ar.SetParameter(11,sqrtPi)

else:
   E1 = raw_input('Lower Threshold (keV)? ')
   E2 = raw_input('Upper Threshold (keV)? ')
   cs_Ar = TF1('cs_Ar','2*[15]*[0]*[1]*([12]/[11])*1/(exp(-[12]*[13]/(0.5*x*1e6*[9]**2*(4*x*[6]/((x+[6])**2))))-exp(-[12]*[14]/(0.5*x*1e6*[9]**2*(4*x*[6]/((x+[6])**2)))))/([2]*[3]*[4]*[5]**2*(4*x*[6]/((x+[6])**2)))*(1/(3*(sin([7]*pow(0.5*x*1e6*[9]**2*(4*x*[6]/((x+[6])**2)),0.5)*[8])-[7]*pow(0.5*x*1e6*[9]**2*(4*x*[6]/((x+[6])**2)),0.5)*[8]*cos([7]*pow(0.5*x*1e6*[9]**2*(4*x*[6]/((x+[6])**2)),0.5)*[8]))/([7]*pow(0.5*x*1e6*[9]**2*(4*x*[6]/((x+[6])**2)),0.5)*[8])**3*exp(-([7]*pow(0.5*x*1e6*[9]**2*(4*x*[6]/((x+[6])**2)),0.5)*[10])**2/2))**2)/100000',0,1000);
   cs_Ar.SetParameter(0,M_nuc)
   cs_Ar.SetParameter(1,R0)
   cs_Ar.SetParameter(2,N0_kg)
   cs_Ar.SetParameter(3,rhoW)
   cs_Ar.SetParameter(4,v0_cmd)
   cs_Ar.SetParameter(5,M_Ar)
   cs_Ar.SetParameter(6,MT)
   cs_Ar.SetParameter(7,qfact)
   cs_Ar.SetParameter(8,rn)
   cs_Ar.SetParameter(9,v0_prob)
   cs_Ar.SetParameter(10,s)
   cs_Ar.SetParameter(11,c1)
   cs_Ar.SetParameter(12,c2)
   cs_Ar.SetParameter(13,float(E1))
   cs_Ar.SetParameter(14,float(E2))
   cs_Ar.SetParameter(15,sqrtPi)

canvas1 = TCanvas('canvas1','',800,640)
canvas1.SetLogx()
canvas1.SetLogy()

h = TH2D('h','',100,0,1000,1000,1e-48,1e-38)
h.SetStats(0)
h.SetXTitle('M_{WIMP} (GeV/c^{2})')
h.SetYTitle('cross section (cm^{2})')
h.GetXaxis().SetTitleOffset(1.35)
h.GetXaxis().SetMoreLogLabels()
h.GetYaxis().SetTitleOffset(1.3)
h.Draw()
"""
# DM Online Tools
bins = '10.00 10.72 11.50 12.33 13.22 14.17 15.20 16.30 17.48 18.74 20.09 21.54 23.10 24.77 26.56 28.48 30.54 32.75 35.11 37.65 40.37 43.29 46.42 49.77 53.37 57.22 61.36 65.79 70.55 75.65 81.11 86.97 93.26 100.00 107.23 114.98 123.28 132.19 141.75 151.99 162.98 174.75 187.38 200.92 215.44 231.01 247.71 265.61 284.80 305.39 327.45 351.12 376.49 403.70 432.88 464.16 497.70 533.67 572.24 613.59 657.93 705.48 756.46 811.13 869.75 932.60 1000.00 1072.27 1149.76 1232.85 1321.94 1417.47 1519.91 1629.75 1747.53 1873.82 2009.23 2154.43 2310.13 2477.08 2656.09 2848.04 3053.86 3274.55 3511.19 3764.94 4037.02 4328.76 4641.59 4977.02 5336.70 5722.37 6135.91 6579.33 7054.80 7564.63 8111.31 8697.49 9326.03 10000.00'

ardmData = '1.00e10 1.00e10 1.00e10 1.00e10 1.00e10 6.58e-6 5.81e-7 1.99e-7 9.89e-8 5.61e-8 3.42e-8 2.28e-8 1.59e-8 1.17e-8 9.09e-9 7.16e-9 5.86e-9 4.91e-9 4.22e-9 3.69e-9 3.29e-9 2.98e-9 2.74e-9 2.56e-9 2.43e-9 2.32e-9 2.24e-9 2.18e-9 2.15e-9 2.13e-9 2.12e-9 2.13e-9 2.14e-9 2.17e-9 2.21e-9 2.26e-9 2.33e-9 2.40e-9 2.48e-9 2.57e-9 2.67e-9 2.78e-9 2.90e-9 3.04e-9 3.19e-9 3.35e-9 3.52e-9 3.71e-9 3.92e-9 4.14e-9 4.37e-9 4.63e-9 4.90e-9 5.20e-9 5.52e-9 5.85e-9 6.23e-9 6.63e-9 7.06e-9 7.50e-9 8.01e-9 8.53e-9 9.08e-9 9.69e-9 1.03e-8 1.10e-8 1.18e-8 1.26e-8 1.34e-8 1.44e-8 1.53e-8 1.64e-8 1.76e-8 1.88e-8 2.01e-8 2.15e-8 2.30e-8 2.46e-8 2.64e-8 2.82e-8 3.02e-8 3.23e-8 3.46e-8 3.70e-8 3.97e-8 4.25e-8 4.56e-8 4.88e-8 5.23e-8 5.59e-8 6.00e-8 6.43e-8 6.89e-8 7.39e-8 7.92e-8 8.48e-8 9.09e-8 9.75e-8 1.04e-7 1.12e-7'

mass = array('d',[])
ardm = array('d',[])
temp1 = bins.split()
temp2 = ardmData.split()

for i in range(100):
    mass.append(np.array(temp1[i],dtype=dt))
    ardm.append(np.array(temp2[i],dtype=dt)*1e-36)

ardmXSec = TGraph(100,mass,ardm)
"""
leg = TLegend(0.6,0.75,0.95,0.95)
leg.SetBorderSize(0)
leg.SetFillColor(0)
#leg.AddEntry(ardmXSec,'ArDM, 500kg fiducial mass, 100 live days','l')

for j in range(len(curves)):
   curves[j].SetLineWidth(2)
   curves[j].SetLineColor(39+j)
   curves[j].SetFillColor(39+j)
   curves[j].SetFillStyle(3001)
   if j<3:
      curves[j].Draw('CF')
      leg.AddEntry(curves[j],name[j],'f')
   else:
      curves[j].Draw('C')
      leg.AddEntry(curves[j],name[j],'l')

cs_Ar.SetLineColor(2);
cs_Ar.SetLineWidth(2)
cs_Ar.Draw('C same')
if ERange=='n':
   leg.AddEntry(cs_Ar,'ArDM, 500kg fiducial mass, 100 live days','l')
else:
   leg.AddEntry(cs_Ar,'ArDM, 500kg fid. mass, 100 live days, %s-%s keV'%(E1,E2),'l')
#ardmXSec.SetLineWidth(2)
#ardmXSec.SetLineColor(2)
#ardmXSec.Draw('C')
leg.Draw()

canvas1.Update()
raw_input()
