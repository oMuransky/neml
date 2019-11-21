#!/usr/bin/env python3

import sys
sys.path.append('..')

import numpy as np
from neml import interpolate, drivers, parse, damage, larsonmiller, elasticity

import matplotlib.pyplot as plt

if __name__ == "__main__":
  base_poly = np.array([-6.65302426e-09, 2.95224164e-04, -6.19561767e-01])
  base_C = 32.064788

  srange = np.linspace(140,250)
  lmp_range = np.linspace(32000,25000)
  
  emodel = elasticity.IsotropicLinearElasticModel(
      interpolate.PiecewiseLinearInterpolate([273.15,288.741836735,304.333673469,319.925510204,335.517346939,351.109183673,366.701020408,382.292857143,397.884693878,413.476530612,429.068367347,444.660204082,460.252040816,475.843877551,491.435714286,507.02755102,522.619387755,538.21122449,553.803061224,569.394897959,584.986734694,600.578571429,616.170408163,631.762244898,647.354081633,662.945918367,678.537755102,694.129591837,709.721428571,725.313265306,740.905102041,756.496938776,772.08877551,787.680612245,803.27244898,818.864285714,834.456122449,850.047959184,865.639795918,881.231632653,896.823469388,912.415306122,928.007142857,943.598979592,959.190816327,974.782653061,990.374489796,1005.96632653,1021.55816327,1037.15], [214750.0,213658.571429,212587.755102,211548.29932,210508.843537,209469.387755,208429.931973,207451.428571,206515.918367,205580.408163,204526.530612,203279.183673,202031.836735,200838.367347,199902.857143,198967.346939,198031.836735,197096.326531,196160.816327,195225.306122,194053.061224,192805.714286,191558.367347,190311.020408,189063.673469,187816.326531,186568.979592,185321.632653,184074.285714,182826.938776,181579.591837,180332.244898,179084.897959,177546.938776,175987.755102,174428.571429,172643.265306,170772.244898,168901.22449,166868.571429,164685.714286,162502.857143,160222.857143,157728.163265,155233.469388,152738.77551,150244.081633,147749.387755,145254.693878,142760.0]),
      "youngs", 0.3, "poissons")
  bmodel =  parse.parse_xml("example.xml", "gr91_simple")
  
  fn = interpolate.PolynomialInterpolate([-6.65303514e-09,  2.95224385e-04, -6.19561357e-01])
  C = 28.50845
  lmr = larsonmiller.LarsonMillerRelation(fn, C)
  estress = damage.VonMisesEffectiveStress()
  model = damage.LarsonMillerCreepDamageModel_sd(
      emodel, lmr, estress, bmodel)
  
  T = 550 + 273.15

  lmps = []

  for s in srange:
    res = drivers.creep(model, s, 100.0, 200000*3600.0, 
        T = T, check_dmg = True, dtol = 0.95, nsteps_up = 20,
        nsteps = 1000, logspace = True)
    #plt.figure()
    #plt.plot(res['rtime'], res['rstrain'])
    #plt.show()
    time = res['rtime'][-1] / 3600.0
    lmp = T * (np.log10(time) + base_C)
    print(lmp,time)
    lmps.append(lmp)
  
  plt.figure()
  
  plt.semilogy(lmp_range, 10.0**np.polyval(base_poly, lmp_range), 'k-', 
    label = "Base LMR")
  plt.semilogy(lmps, srange, 'r--', label = "Model results")
  plt.xlabel("LMP")
  plt.ylabel("Stress (MPa)")
  plt.legend(loc='best')
  plt.show()
