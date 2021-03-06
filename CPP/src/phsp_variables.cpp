#include <cstdlib>
#include <iostream>
#include <vector>
#include "TLorentzVector.h"
#include "k3pi_cpp.h"

std::vector<double> phsp_variables(double p1_pt, double p1_eta, double p1_phi,
                                   double p1_m, double p2_pt, double p2_eta,
                                   double p2_phi, double p2_m, double p3_pt,
                                   double p3_eta, double p3_phi, double p3_m,
                                   double p4_pt, double p4_eta, double p4_phi,
                                   double p4_m) {
  // 3 Kaon
  // 1 and 4 the opposite charge pions
  // 2 the same charge pion
  TLorentzVector d1, d2, d3, d4;
  // std::srand(std::time(0));
  d2.SetPtEtaPhiM(p2_pt, p2_eta, p2_phi, p2_m);
  d3.SetPtEtaPhiM(p3_pt, p3_eta, p3_phi, p3_m);

  // Randomise the assignment of d2 and d4, which should be the two OS pions.
  if (((double)std::rand() / (RAND_MAX)) < 0.5) {
    d1.SetPtEtaPhiM(p1_pt, p1_eta, p1_phi, p1_m);
    d4.SetPtEtaPhiM(p4_pt, p4_eta, p4_phi, p4_m);
  } else {
    d4.SetPtEtaPhiM(p1_pt, p1_eta, p1_phi, p1_m);
    d1.SetPtEtaPhiM(p4_pt, p4_eta, p4_phi, p4_m);
  }

  // Boost everything to D0 restframe
  auto mum = d1 + d2 + d3 + d4;
  double m12 = (d1 + d2).M();
  double m34 = (d3 + d4).M();

  d1.Boost(-mum.BoostVector());
  d2.Boost(-mum.BoostVector());
  d3.Boost(-mum.BoostVector());
  d4.Boost(-mum.BoostVector());

  TLorentzVector d12, d34;
  d12 = d1 + d2;
  d34 = d3 + d4;

  TVector3 d1n = d1.Vect().Unit();
  TVector3 d2n = d2.Vect().Unit();
  TVector3 d3n = d3.Vect().Unit();
  TVector3 d4n = d4.Vect().Unit();
  TVector3 d12n = d12.Vect().Unit();
  TVector3 d34n = d34.Vect().Unit();

  TVector3 n1 = d1n.Cross(d2n);
  TVector3 n2 = d3n.Cross(d4n);
  TVector3 n3 = n1.Unit().Cross(n2.Unit());

  // Calculation of the angle Phi between the planes.
  double cosp = n1.Unit().Dot(n2.Unit());
  double sinp = n3.Dot(d34n);
  double phi1 = acos(cosp);
  if (sinp < 0) phi1 *= -1;

  // Vectors in rest fram of their resonance.
  TLorentzVector d1r = d1;
  TLorentzVector d3r = d3;
  d1r.Boost(-d12.BoostVector());
  d3r.Boost(-d34.BoostVector());
  TVector3 d1rn = d1r.Vect().Unit();
  TVector3 d3rn = d3r.Vect().Unit();

  // helicity angle for d12 and d34 frame
  double cos1 = d12n.Dot(d1rn);
  double cos2 = d34n.Dot(d3rn);

  std::vector<double> vars = {m12, m34, cos1, cos2, phi1};
  return vars;
}

double phsp_variables_m12(double p1_pt, double p1_eta, double p1_phi,
                          double p1_m, double p2_pt, double p2_eta,
                          double p2_phi, double p2_m, double p3_pt,
                          double p3_eta, double p3_phi, double p3_m,
                          double p4_pt, double p4_eta, double p4_phi,
                          double p4_m) {
  // 3 Kaon
  // 1 and 4 the opposite charge pions
  // 2 the same charge pion
  TLorentzVector d1, d2, d3, d4;
  // std::srand(std::time(0));
  d2.SetPtEtaPhiM(p2_pt, p2_eta, p2_phi, p2_m);
  d3.SetPtEtaPhiM(p3_pt, p3_eta, p3_phi, p3_m);

  // Randomise the assignment of d2 and d4, which should be the two OS pions.
  if (((double)std::rand() / (RAND_MAX)) < 0.5) {
    d1.SetPtEtaPhiM(p1_pt, p1_eta, p1_phi, p1_m);
    d4.SetPtEtaPhiM(p4_pt, p4_eta, p4_phi, p4_m);
  } else {
    d4.SetPtEtaPhiM(p1_pt, p1_eta, p1_phi, p1_m);
    d1.SetPtEtaPhiM(p4_pt, p4_eta, p4_phi, p4_m);
  }

  // Boost everything to D0 restframe
  return (d1 + d2).M();
}

std::vector<double> phsp_variables_maxime(
    double p1_e, double p1_px, double p1_py, double p1_pz, double p2_e,
    double p2_px, double p2_py, double p2_pz, double p3_e, double p3_px,
    double p3_py, double p3_pz, double p4_e, double p4_px, double p4_py,
    double p4_pz) {
  // 3 Kaon
  // 1 and 4 the opposite charge pions
  // 2 the same charge pion
  // Km, Kp, pim, pip
  TLorentzVector d1, d2, d3, d4;
  std::cout << p1_px << ", " << p1_py << ", " << p1_pz << ", " << p1_e << ", "
            << std::endl;
  std::cout << p2_px << ", " << p2_py << ", " << p2_pz << ", " << p2_e << ", "
            << std::endl;
  std::cout << p3_px << ", " << p3_py << ", " << p3_pz << ", " << p3_e << ", "
            << std::endl;
  std::cout << p1_px << ", " << p1_py << ", " << p1_pz << ", " << p1_e << ", "
            << std::endl;
  d1.SetPxPyPzE(p1_px, p1_py, p1_pz, p1_e);
  d2.SetPxPyPzE(p2_px, p2_py, p2_pz, p2_e);
  d3.SetPxPyPzE(p3_px, p3_py, p3_pz, p3_e);
  d4.SetPxPyPzE(p4_px, p4_py, p4_pz, p4_e);

  double m12 = (d1 + d2).M();
  double m34 = (d3 + d4).M();

  double m14 = (d1 + d4).M();
  double m123 = (d1 + d2 + d3).M();
  double m234 = (d2 + d3 + d4).M();
  std::cout << m12 << ", " << m34 << ", " << m14 << ", " << m123 << ", " << m234
            << ", " << std::endl;
  std::cout << "------------------------------------" << std::endl;

  std::vector<double> vars = {m12, m34, m14, m123, m234};
  return vars;
}
