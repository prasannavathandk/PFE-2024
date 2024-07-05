import multiprocessing
import warnings

import pandas as pd
from Calibrator import Calibrator
from Parameters import Parameters 
import numpy as np
import Helper as hp
from LIBORSimulator import LIBORSim
import NumericalSolver
from SwaptionPricer import SwaptionPricing

nofCores = multiprocessing.cpu_count()

def trigger(epoch):
    print("---Epoch %i started---" %(epoch+1))
    simulator = LIBORSim(maturity=np.array(Parameters.maturityDates), prices=np.array(Parameters.bondPrices), volatility=Parameters.intervalVolatility, scale = 1, measure=Parameters.measure, type=Parameters.scheme, iter = Parameters.batch(nofCores))
    df = simulator.simulate(epoch=epoch).analyze()
    df["epoch"] = epoch+1 
    df.set_index('epoch', append=True, inplace=True)  
    #print(df.head())
    df = df.swaplevel("epoch", "time").swaplevel("epoch", "iteration")
    del simulator
    timer.stop() 
    print("---Epoch %i done---"% (epoch+1))
    return df

def main():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)

        print("LIBOR Market Model")
        print("**********************************")
        global timer 
        timer = hp.timer()
        print("Simulation to run with the following parameters:")
        print("Maturity Dates:", Parameters.maturityDates)
        print("Bond Prices:", Parameters.bondPrices)
        print("----------------------------------")
        print("Simulation initiate...", timer.tick) 
        timer.start()   

        df = [trigger(ep) for ep in range(Parameters.epoch)]
        print("----------------------------------")
        print("Result Summary:")
        output = pd.concat(df).sort_index()
        output.info()
        output.describe(include='all')
        output.to_csv("Simulation-SpotMeasure-General.csv")
        plotOut = output.groupby('time').mean()
        #print(plotOut.head())
        hp.plotDF(plotOut, title="Curve-SpotMeasure-General", clear=False)
        hp.showPLot()

        # print("----------------------------------")
        # print("Volatitlity Calibration")
        # derivative = Parameters.derivatives['Swaption']
        # pricer = SwaptionPricing(derivative, LIBORSim)
        # print(pricer.analyticalPricing())
        # calibrator = Calibrator(pricer=pricer)
        # print(calibrator.calibrate())
         
    print("Simulation complete :) ...", timer.tock)

if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        NumericalSolver.Solver.manager = manager
        with multiprocessing.Pool(processes=nofCores) as pool:
            print("number of cores", nofCores)
            NumericalSolver.Solver.setPool(pool)
            NumericalSolver.Solver.setParallelism(flag=Parameters.parallel)
            main()