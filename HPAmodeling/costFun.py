# File Name: costFunc.py
# Description: this module will contain the function for computing cost, 
#  although I'm not sure how reliably I'll be able to do that for all 6 models
#  as it currently has quite few hardcoded variables
# Author: Christopher Parker
# Created: Tue Jan 25, 2022 | 09:26P EST
# Last Modified: Mon May 30, 2022 | 07:12P EDT

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#                        Modified BSD License                                 #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#     Copyright 2022 Christopher John Parker <parkecp@mail.uc.edu>            #
#                                                                             #
# Redistribution and use in source and binary forms, with or without          #
# modification, are permitted provided that the following conditions are met: #
#                                                                             #
# 1. Redistributions of source code must retain the above copyright notice,   #
#    this list of conditions and the following disclaimer.                    #
#                                                                             #
# 2. Redistributions in binary form must reproduce the above copyright        #
#    notice, this list of conditions and the following disclaimer in the      #
#    documentation and/or other materials provided with the distribution.     #
#                                                                             #
# 3. Neither the name of the copyright holder nor the names of its            #
#    contributors may be used to endorse or promote products derived from     #
#    this software without specific prior written permission.                 #
#                                                                             #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" #
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE   #
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE  #
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE   #
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR         #
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF        #
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS    #
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN     #
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)     #
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE  #
# POSSIBILITY OF SUCH DAMAGE.                                                 #
#                                                                             #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

import numpy as np
from scipy.interpolate import interp1d

# This is the main function you'll want to call from this module. It takes
#  the time steps and data points for the real-world ACTH and cortisol
#  concentration values you're optimizing against as well as the data from 
#  a simulation with the model and returns the cost for the parameter set used
def SSE_cost(time_ACTH, data_ACTH, time_CORT, data_CORT, simData):
    # Compute the means of ACTH and CORT data arrays
    mean_ACTH = np.mean(data_ACTH)
    mean_CORT = np.mean(data_CORT)

    # Normalize the simData arrays by the mean values of data set to be matched
    simNorm_ACTH = simData[:,2]/mean_ACTH
    simNorm_CORT = simData[:,3]/mean_CORT

    # Normalize the data set to be matched, as well
    dataNorm_ACTH = data_ACTH/mean_ACTH
    dataNorm_CORT = data_CORT/mean_CORT

    # Now, we interpolate between the simulated data points, to ensure we have
    #  a simulated data point at the exact time of each real-world data point
    # We are currently doing a linear interpolation, although we could also
    #  choose to do cubic. however, I don't think it makes a huge amount of
    #  difference in this context
    spline_ACTH = interp1d(simData[:,0], simNorm_ACTH, kind = 'linear')
    spline_CORT = interp1d(simData[:,0], simNorm_CORT, kind = 'linear')

    # We use a try/except loop to ensure that we don't run into an error that
    #  causes the entire simulation to fail and have to start over
    try:
        # Compute the cost value for the current parameter set by finding the
        #  SSE between raw data and splines.
        acthSSE = np.sum((spline_ACTH(time_ACTH) - dataNorm_ACTH)**2)
        cortSSE = np.sum((spline_CORT(time_CORT) - dataNorm_CORT)**2)

        # We define cost as the average of the ACTH and CORT SSEs.
        cost = (acthSSE + cortSSE)/2

        return cost

    except ValueError:
        # In the case that we encounter a ValueError, this means that the ODE
        #  solver quit before computing all time steps up to t_end. The error
        #  arises when we attempt to plug in a time value after where the 
        #  solver quit to spline_ACTH or spline_CORT. So we catch the
        #  ValueError here, and let the user know that the ODE solver exited
        #  early.
        print("ODE solver did not make it through all data points.")


# This is similar to the function above, but does not take ACTH concentration
#  data as an input. So you'd use this one if your real-world data only has
#  cortisol concentrations
def SSE_cost_noACTH(time_CORT, data_CORT, simData):
    # Compute the mean of the CORT data array
    mean_CORT = np.mean(data_CORT)

    # Normalize the simData array by the mean value of data set to be matched
    simNorm_CORT = simData[:,3]/mean_CORT

    # Normalize the data set to be matched, as well
    dataNorm_CORT = data_CORT/mean_CORT

    # Now, we interpolate between the simulated data points, to ensure we have
    #  a simulated data point at the exact time of each real-world data point
    # We are currently doing a linear interpolation, although we could also
    #  choose to do cubic. however, I don't think it makes a huge amount of
    #  difference in this context
    spline_CORT = interp1d(simData[:,0], simNorm_CORT, kind = 'linear')

    # We use a try/except loop to ensure that we don't run into an error that
    #  causes the entire simulation to fail and have to start over
    try:
        # As the data we are matching does not include ACTH values, we simply
        #  define cost as the SSE between raw data and splines of the CORT array
        cost = np.sum((spline_CORT(time_CORT) - dataNorm_CORT)**2)

        return cost

    except ValueError:
        # In the case that we encounter a ValueError, this means that the ODE
        #  solver quit before computing all time steps up to t_end. The error
        #  arises when we attempt to plug in a time value after where the 
        #  solver quit to spline_CORT. So we catch the ValueError here, and let 
        #  the user know that the ODE solver exited early.
        print("ODE solver did not make it through all data points.")

# We also need to define cost functions for using the minimum and maximum
#  distance between the simulation and real-world data.
#  
# Here, we use the maximum distance
def max_cost(time_ACTH, data_ACTH, time_CORT, data_CORT, simData):
    # Compute the means of ACTH and CORT data arrays
    mean_ACTH = np.mean(data_ACTH)
    mean_CORT = np.mean(data_CORT)

    # Normalize the simData arrays by the mean values of data set to be matched
    simNorm_ACTH = simData[:,2]/mean_ACTH
    simNorm_CORT = simData[:,3]/mean_CORT

    # Normalize the data set to be matched, as well
    dataNorm_ACTH = data_ACTH/mean_ACTH
    dataNorm_CORT = data_CORT/mean_CORT

    # Now, we interpolate between the simulated data points, to ensure we have
    #  a simulated data point at the exact time of each real-world data point
    # We are currently doing a linear interpolation, although we could also
    #  choose to do cubic. however, I don't think it makes a huge amount of
    #  difference in this context
    spline_ACTH = interp1d(simData[:,0], simNorm_ACTH, kind = 'linear')
    spline_CORT = interp1d(simData[:,0], simNorm_CORT, kind = 'linear')

    # We use a try/except loop to ensure that we don't run into an error that
    #  causes the entire simulation to fail and have to start over
    try:
        # Compute the cost value for the current parameter set by finding the
        #  maximum distance between the simulations and data for each of ACTH 
        #  and CORT
        acthMAX = np.amax((spline_ACTH(time_ACTH) - dataNorm_ACTH)**2)
        cortMAX = np.amax((spline_CORT(time_CORT) - dataNorm_CORT)**2)

        # We define cost as the maximum of the maximums that we just found above
        cost = np.amax([acthMAX, cortMAX])

        return cost

    except ValueError:
        # In the case that we encounter a ValueError, this means that the ODE
        #  solver quit before computing all time steps up to t_end. The error
        #  arises when we attempt to plug in a time value after where the 
        #  solver quit to spline_ACTH or spline_CORT. So we catch the
        #  ValueError here, and let the user know that the ODE solver exited
        #  early.
        print("ODE solver did not make it through all data points.")

# And here we compute the cost based on the maximum distance for data sets that
#  only contain cortisol data
def max_cost_noACTH(time_CORT, data_CORT, simData):
    # Compute the mean of the CORT data array
    mean_CORT = np.mean(data_CORT)

    # Normalize the simData array by the mean value of data set to be matched
    simNorm_CORT = simData[:,3]/mean_CORT

    # Normalize the data set to be matched, as well
    dataNorm_CORT = data_CORT/mean_CORT

    # Now, we interpolate between the simulated data points, to ensure we have
    #  a simulated data point at the exact time of each real-world data point
    # We are currently doing a linear interpolation, although we could also
    #  choose to do cubic. however, I don't think it makes a huge amount of
    #  difference in this context
    spline_CORT = interp1d(simData[:,0], simNorm_CORT, kind = 'linear')

    # We use a try/except loop to ensure that we don't run into an error that
    #  causes the entire simulation to fail and have to start over
    try:
        # As the data we are matching does not include ACTH values, we simply
        #  define cost as the maximum distance between raw data and splines 
        #  of the CORT array
        cost = np.amax((spline_CORT(time_CORT) - dataNorm_CORT)**2)

        return cost

    except ValueError:
        # In the case that we encounter a ValueError, this means that the ODE
        #  solver quit before computing all time steps up to t_end. The error
        #  arises when we attempt to plug in a time value after where the 
        #  solver quit to spline_CORT. So we catch the ValueError here, and let 
        #  the user know that the ODE solver exited early.
        print("ODE solver did not make it through all data points.")
