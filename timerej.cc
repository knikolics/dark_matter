#include <iostream>
#include "TApplication.h"
#include "TRandom.h"
#include "TFile.h"
#include "TH1.h"
#include "TCanvas.h"
#include "TGraph.h"

TH1D *hdecspnuc;
TH1D *hdecspgam;
int Anz=6;//8; 


double ScintGammaTime(bool nuclear)
{
  int i;
  double tau,i1overi3,tau_singlet,tau_triplet;

  /* time constants for Argon, singlet and triplet state of excimer */
  /* in ns */
  tau_singlet=6;
  tau_triplet=1590;//1590;

  if(nuclear)
    i1overi3 = 3;      /* from Boulay, Hime arXiv:astro-ph/0411358 */
  else
    i1overi3 = 0.3;      /* from Boulay, Hime arXiv:astro-ph/0411358 */

  /* select when long or short time constant */
  double singtrip = gRandom->Rndm(i);
  double probi1 = 1.0/(1.0+(1.0/i1overi3));
  if(singtrip<probi1)
    tau=tau_singlet;
  else
    tau=tau_triplet;
   double time = gRandom->Exp(tau);

  return(time);
}


void ScintTimeRej(int nGam, double &fnuc, double &fgam)
{

  double tCut = 50; /* in ns */
  int abovenuc=0, abovegam=0;
  for(int ig=0;ig<nGam;ig++)//simult, one evt of ngamma photoels
    {
      double tnuc = ScintGammaTime(true);
      hdecspnuc->Fill(tnuc);
      double tgam = ScintGammaTime(false);
      hdecspgam->Fill(tgam);
      if(tnuc<tCut)abovenuc++;//detected prompt as n induced g
      if(tgam<tCut)abovegam++;//detected prompt as g induced g
    }
  fnuc=(double)abovenuc/nGam;//frac prompt to total for evts detected as n induced g
  fgam=(double)abovegam/nGam;//frac prompt to total for evts detected as g induced g
}


int main(int argc, char **argv)
{ 
//  TApplication theApp("App", &argc, argv);
  
  double fnuc, fgam;
  double fCut = 0.62;
//  double fCut = 0.82;

   int trt;
   Float_t x[trt], y[trt];
 

  TFile *hfile = new TFile("hsimple.root","RECREATE","Demo ROOT file with histograms");
  TCanvas* c1 = new TCanvas("c1","fnuc",20,1,1600,600);
  TPad * pad = new TPad("pad","a2",0.,0.,1.,1.);
  pad->Divide(3,1);
  pad->Draw("");
  pad->cd();


  TH1D *hnuc = new TH1D("fnuc","",100,0,1.0);
  TH1D *hgam = new TH1D("fgam","",100,0,1.0);
 TH1D *hnuc1 = new TH1D("fnuc1","",100,0,1.0);
  TH1D *hgam1 = new TH1D("fgam1","",100,0,1.0);
 TH1D *hnuc2 = new TH1D("fnuc2","",100,0,1.0);
  TH1D *hgam2 = new TH1F("fgam2","",100,0,1.0);
  hdecspnuc = new TH1D("decspnuc","",100,0,3000);
  hdecspgam = new TH1D("decspgam","",100,0,3000);

   std::cout << "nGam   fnuc   fgam "<<std::endl;
 
   // for(int nGam=Anz-1;nGam<Anz;nGam++)
 for(int nGam=4;nGam<40;nGam++)
   { // std::cout << " fnuc  "<<fnuc <<std::endl;
      double sfnuc=0, sfgam=0;
      double ntot=0;
      while(sfnuc<100000)//000)//averaging for a certain number of 
	{
	  ScintTimeRej(nGam, fnuc, fgam);
	  
	  if(fnuc>fCut)sfnuc++;//ratio above tcut -> call it a n
	  if(fgam>fCut)sfgam++;//ratio below tcut -> call it a fake neutron

	      hnuc->Fill(fnuc);
	      hgam->Fill(fgam);

	  ntot++;
	}
      double survnuc = sfnuc/ntot;//aved
      double survgam = sfgam/ntot;
      std::cout << ntot << "ntot " <<std::endl;
      std::cout << nGam << " " <<survnuc << "   "<<survgam<<std::endl;
   }   

#if 0   
 for(int nGam=(Anz+2-1);nGam<(Anz+2);nGam++)
   { // std::cout << " fnuc  "<<fnuc <<std::endl;
      double sfnuc=0, sfgam=0;
      double ntot=0;
      while(sfgam<100000)//000)//averaging for a certain number of 
	{
	  ScintTimeRej(nGam, fnuc, fgam);
	  
	  if(fnuc>fCut)sfnuc++;//ratio above tcut -> call it a n
	  if(fgam<fCut)sfgam++;//ratio below tcut -> call it a gamma

	      hnuc1->Fill(fnuc);
	      hgam1->Fill(fgam);

	  ntot++;
	}
      double survnuc = sfnuc/ntot;//aved
      double survgam = sfgam/ntot;
 std::cout << ntot << "ntot " <<std::endl;
      std::cout << nGam << " " <<survnuc << "   "<<survgam<<std::endl;
       trt=nGam;
       x[trt]=trt;  
      y[trt]=survnuc;
      //          printf(" i %i %f %f n",nGam,x[nGam],y[nGam]);
   }
   

 for(int nGam=(Anz+4-1);nGam<(Anz+4);nGam++)
   { // std::cout << " fnuc  "<<fnuc <<std::endl;
      double sfnuc=0, sfgam=0;
      double ntot=0;
      while(sfgam<100000)//000)//averaging for a certain number of 
	{
	  ScintTimeRej(nGam, fnuc, fgam);
	  
	  if(fnuc>fCut)sfnuc++;//ratio above tcut -> call it a n
	  if(fgam<fCut)sfgam++;//ratio below tcut -> call it a gamma

	      hnuc2->Fill(fnuc);
	      hgam2->Fill(fgam);

	  ntot++;
	}
      double survnuc = sfnuc/ntot;//aved
      double survgam = sfgam/ntot;
 std::cout << ntot << " ntot " <<std::endl;
      std::cout << nGam << " " <<survnuc << "   "<<survgam<<std::endl;
       trt=nGam;
       x[trt]=trt;  
      y[trt]=survnuc;
      //          printf(" i %i %f %f n",nGam,x[nGam],y[nGam]);
   }
#endif


 TGraph *gr = new TGraph(trt,x,y);
   gr->SetFillColor(19);
   gr->SetLineColor(2);
   gr->SetLineWidth(4);
   gr->SetMarkerColor(4);
   gr->SetMarkerStyle(21);
   gr->SetTitle("graph");
 pad->cd(1);
 //   gr->Draw("ACP");


 hgam->SetFillColor(kRed);
 hnuc->Draw("");
 hgam->Draw("same");
 c1->Update();

  hfile->Write();

   pad->cd(2);
  hnuc1->Draw("");
  c1->Update();

  hgam1->Draw("same");
  hgam1->SetFillColor(kRed);

  pad->cd(3);
  hnuc2->Draw("");
  c1->Update();

  hgam2->Draw("same");
  hgam2->SetFillColor(kRed);

  //hdecspnuc->Draw("");//histo of decay times n evt
  c1->Update();

  hdecspgam->Draw("same");//histo of decay times g evt
  hdecspgam->SetFillColor(kRed);
  c1->Draw("");  

//  theApp.Run();
  return 0;
   }
