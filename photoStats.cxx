#include <iostream>
#include "TRandom3.h"
#include "TRandom2.h"
#include "TFile.h"
#include "TH1.h"
#include "TCanvas.h"
#include <cmath>

using namespace std;

TH1D *hdecspnuc;
TH1D *hdecspgam;
//int Anz=6;//8; 
int lowTh = 0;
int upTh = 0;

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
//  gRandom = new TRandom2(0);
//  double singtrip = gRandom->Rndm(i);
  double singtrip = drand48();
  double probi1 = 1.0/(1.0+(1.0/i1overi3));
  if(singtrip<probi1)    tau=tau_singlet;
  else   tau=tau_triplet;
  double dummy = drand48();
//  cout << "singtrip " << singtrip << ", dummy " << dummy << endl;
  double time = -log(dummy)*tau;
//  double time = gRandom->Exp(tau);
  return(time);
}


void ScintTimeRej(int nGam, double &fnuc, double &fgam)
{

  double tCut = 60; /* in ns */
  int abovenuc=0, abovegam=0;
  for(int ig=0;ig<nGam;ig++)//simult, one evt of ngamma photoels
    {
      double tnuc = ScintGammaTime(true);
//      cout << "tnuc " << tnuc << endl;
      hdecspnuc->Fill(tnuc);
      double tgam = ScintGammaTime(false);
//      cout << "tgam " << tgam << endl;
      hdecspgam->Fill(tgam);
      if(tnuc<tCut)abovenuc++;//detected prompt as n induced g
      if(tgam<tCut)abovegam++;//detected prompt as g induced g
    }
  fnuc=(double)abovenuc/nGam;//frac prompt to total for evts detected as n induced g
  fgam=(double)abovegam/nGam;//frac prompt to total for evts detected as g induced g
}


int main(int argc, char **argv)
{ 
  
  double fnuc, fgam;
  //double fCut = 0.82;
  double fCut = 0.62;
 if (argv[1]==NULL) {
   cout << "No photon numbers given!" << endl;
   return 0;
 }
 lowTh = atoi(argv[1]);
 cout << "lowTh " << lowTh << endl;
 upTh = atoi(argv[2]);
 int nPhotons = upTh-lowTh;
//   int trt;
 Float_t x[nPhotons], ynuc[nPhotons], ygam[nPhotons];

 TFile *hfile = new TFile("histos.root","RECREATE","ROOT file with histograms");
 TCanvas* c1 = new TCanvas("c1","fnuc/fgam",600,480);
 TCanvas* c2 = new TCanvas("c2","decay times",600,480);
//  TPad * pad = new TPad("pad","a2",0.,0.,1.,1.);

 TH1D *hnuc = new TH1D("fnuc","",100,0,1.0);
 TH1D *hgam = new TH1D("fgam","",100,0,1.0);
 hdecspnuc = new TH1D("decspnuc","",500,0,3000);
 hdecspgam = new TH1D("decspgam","",500,0,3000);
 TH1D *survProbNuc = new TH1D("survProbNuc","",nPhotons,lowTh,upTh);
 TH1D *survProbGam = new TH1D("survProbGam","",nPhotons,lowTh,upTh);

 std::cout << "nGam      fnuc      fgam "<<std::endl;
 
 srand48(time(NULL));
   // for(int nGam=Anz-1;nGam<Anz;nGam++)
 for(int nGam=lowTh;nGam<upTh;nGam++)
   { // std::cout << " fnuc  "<<fnuc <<std::endl;
      double sfnuc=0, sfgam=0;
      double ntot=0;
      while(sfnuc<10000000)//000)//averaging for a certain number of 
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
      int iGam = nGam-lowTh;
      survProbNuc->SetBinContent(iGam+1.5,survnuc);
      survProbGam->SetBinContent(iGam+1.5,survgam);
      std::cout << "ntot " << ntot <<std::endl;
      std::cout << nGam << " " <<survnuc << "   "<<survgam<<std::endl;
   }   

 c1->cd();
 hgam->SetLineColor(kRed);
 hnuc->Draw("");
 hgam->Draw("same");
 c1->Update();

  //hfile->Write();
  c2->cd();
  hdecspnuc->Draw("");//histo of decay times n evt

  hdecspgam->SetLineColor(kRed);
  hdecspgam->Draw("same");//histo of decay times g evt
  //c1->Draw("");  
  c2->Update();
  hfile->Write();
//  return 0;
 }
