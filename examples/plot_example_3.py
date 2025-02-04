#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
"""
Network covariance matrix spectral width: natural case
=========================================================


This example shows how to calculate the spectral width of the network covariance matrix. It makes use of 6 hours of real seismic data acquired the 2010.10.14 (between 10:00 and 16:00 - GMT) by the Piton de la Fournaise seismic network. This dataset contains seismovolcanic signals linked to a pre-eruptive seismic swarm and to the beginning of a co-eruptive tremor starting at 15:20 (GMT). This basic example makes use of a stream with already synchronized traces and does not apply any pre-processing.

Considering 15 stations of the Piton de la Fournaise seismic network (using only the vertical component), the covariance is of dimensions 15 times 15. The following example use a Fourier estimation window of 20 seconds and is estimated over 15 consecutive windows. The overlapping between the Fourier windows is 50%, and the step between two consecutive averaging window is 50%.

The lower the covariance matrix spectral width (yellow), the more coherent the seismic wavefield. 
"""

import covseisnet as csn
import matplotlib.pyplot as plt
from obspy import UTCDateTime
from obspy.clients.fdsn import Client

# download data from the YA Undervolc seismic network with RESIF Seismic data portal
client = Client("RESIF")
signal_duration_sec = 6 * 3600
t = UTCDateTime("2010-10-14T10:00:00.00")
stream = client.get_waveforms("YA", "UV*", "00", "HHZ", t, t + signal_duration_sec)

# downsample data to 25 Hz
stream.decimate(4)

# calculate covariance from stream
window_duration_sec = 20
average = 15
times, frequencies, covariances = csn.covariancematrix.calculate(
    stream, window_duration_sec, average
)

# calculate spectral width
spectral_width = covariances.coherence(kind="spectral_width")

# show network covariance matrix spectral width
fig, ax = plt.subplots(1, constrained_layout=True)
img = ax.pcolormesh(
    10 + times / 3600, frequencies, spectral_width.T, rasterized=True, cmap="viridis_r"
)
ax.set_ylim([0, stream[0].stats.sampling_rate / 2])
ax.set_xlabel("2010.10.14 (hours)")
ax.set_ylabel("Frequency (Hz)")
plt.colorbar(img).set_label("Covariance matrix spectral width")
