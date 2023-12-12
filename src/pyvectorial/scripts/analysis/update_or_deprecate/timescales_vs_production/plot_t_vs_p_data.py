#!/usr/bin/env python3

import sys
# import copy

import numpy as np
# import astropy.units as u
from astropy.visualization import quantity_support
import matplotlib.pyplot as plt
# from matplotlib import cm, colors
# from matplotlib import colors

__author__ = 'Shawn Oset'
__version__ = '0.0'

# solarbluecol = np.array([38, 139, 220]) / 255.
# solarblue = (solarbluecol[0], solarbluecol[1], solarbluecol[2], 1)
# solargreencol = np.array([133, 153, 0]) / 255.
# solargreen = (solargreencol[0], solargreencol[1], solargreencol[2], 1)
# solarblackcol = np.array([0, 43, 54]) / 255.
# solarblack = (solarblackcol[0], solarblackcol[1], solarblackcol[2], 1)
# solarwhitecol = np.array([238, 232, 213]) / 255.
# solarwhite = (solarblackcol[0], solarblackcol[1], solarblackcol[2], 1)


def generate2D_TvsQPlot(TvsQdata, modelProduction):

    timescales = TvsQdata[:, 1]
    Qs = TvsQdata[:, 2]

    # Make sure to clear the dark background setting from the 3D plots by defaulting everything here
    plt.style.use('default')
    plt.style.use('Solarize_Light2')

    fig, ax1 = plt.subplots(1, 1, figsize=(20, 10))

    ax1.set(xlabel="Dissociative lifetime of H2O, (s)")
    ax1.set(ylabel="Q(H2O)")
    fig.suptitle(f"Calculated productions against varying lifetimes for initial model Q = {modelProduction}")

    ax1.plot(timescales, Qs, color="#688894",  linewidth=2.5, linestyle="-", label="", zorder=1)
    ax1.scatter(timescales, Qs, color="#c74a77", zorder=2)

    plt.legend(loc='upper right', frameon=False)
    plt.show()
    # plt.savefig(filename)
    plt.close()


def generateAggregatePlots(t_vs_q_data, out_file=None):

    # Grab each set of values in a flat array for scatter plotting, with productions in log10
    model_qs = np.log10(t_vs_q_data[:, :, 0].flatten())
    timescales = t_vs_q_data[:, :, 1].flatten()
    qs = np.log10(t_vs_q_data[:, :, 2].flatten())

    # Make sure to clear the dark background setting from the 3D plots by defaulting everything here
    plt.style.use('default')
    plt.style.use('Solarize_Light2')

    fig = plt.figure(figsize=(30, 30))
    ax = plt.axes(projection='3d')

    # 3d scatter plot
    ax.scatter(model_qs, timescales, qs)

    # add linear best fit curves for each run
    for model_production in t_vs_q_data:
        # Each column in the data structure has the relevant data
        mqs = np.log10(model_production[:, 0])
        ts = model_production[:, 1]
        cps = np.log10(model_production[:, 2])
        coeffs = np.polyfit(ts, cps, 1)
        fitfunction = np.poly1d(coeffs)
        fit_ys = fitfunction(ts)
        ax.plot3D(mqs, ts, fit_ys, color="#c74a77")
        ax.plot3D(mqs, ts, cps, color="#afac7c")

    ax.set(xlabel="Model production, log10 Q(H2O)")
    ax.set(ylabel="Dissociative lifetime of H2O, (s)")
    ax.set(zlabel="Calculated production, log10 Q(H2O)")
    fig.suptitle("Calculated productions against varying lifetimes for range of model Q(H2O)")

    # Initialize 3d view at these angles for saving the plot
    ax.view_init(20, 30)

    if out_file:
        plt.savefig(out_file)
    plt.show()
    plt.close()


def main():

    quantity_support()

    with open('output.npdata', 'rb') as np_file:
        all_data = np.load(np_file)

    generateAggregatePlots(all_data)


if __name__ == '__main__':
    sys.exit(main())
