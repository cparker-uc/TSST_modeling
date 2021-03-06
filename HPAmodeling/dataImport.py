# File Name: dataImport.py
# Description: This module will be used to import all of the various data sets,
#  which will hopefully greatly improve readability of the code (as the data
#  imports take up the majority of the lines of code in each model right now)
# Author: Christopher Parker
# Created: Thu Jan 27, 2022 | 09:38P EST
# Last Modified: Wed May 04, 2022 | 11:51P EDT

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

# This function sets the concentration value at each time step to the average
#  of the five nearest points to that time step.
def smoothing(a, n = 5):
    idx = int((n - 1)/2)
    ret = np.cumsum(a, dtype = float)
    ret[idx + 1:-idx] = ret[n:] - ret[:-n]
    ret[idx] = ret[idx + 2]
    return ret[idx:-idx]/n

# Import the data from Yehuda et al. (1996) and return arrays for control, PTSD
#  and depressed groups, as well as smoothed versions of the same. This data
#  set only includes cortisol concentration data.
def yehuda():
    controlCortisol = np.genfromtxt("data_files/yehuda-control-cortisol.txt")
    PTSDCortisol = np.genfromtxt("data_files/yehuda-PTSD-cortisol.txt")
    depressedCortisol = np.genfromtxt("data_files/yehuda-depressed-cortisol.txt")

    controlCortisol_smooth = controlCortisol
    PTSDCortisol_smooth = PTSDCortisol
    depressedCortisol_smooth = depressedCortisol

    controlCortisol_smooth[2:-2,1] = smoothing(controlCortisol[:,1])
    PTSDCortisol_smooth[2:-2,1] = smoothing(PTSDCortisol[:,1])
    depressedCortisol_smooth[2:-2,1] = smoothing(depressedCortisol[:,1])

    controlCortisol = np.genfromtxt("data_files/yehuda-control-cortisol.txt")
    PTSDCortisol = np.genfromtxt("data_files/yehuda-PTSD-cortisol.txt")
    depressedCortisol = np.genfromtxt("data_files/yehuda-depressed-cortisol.txt")

    return [controlCortisol, controlCortisol_smooth, PTSDCortisol, PTSDCortisol_smooth, depressedCortisol, depressedCortisol_smooth]

# Import the data from Carroll et al. (2007) and save it to arrays for control,
#  low-cortisol depressed (LCDepressed) and high-cortisol depressed 
#  (HCDepressed), with separate arrays for ACTH and cortisol concentration.
# Also rearrange the data to have the same starting point as the Yehuda data,
#  which is 10AM, and save it to arrays with _rearr at the end. Then create
#  smoothed versions of both normal and rearranged arrays, and save them to
#  arrays with _smooth at the end.
def carroll():
    controlCortisol = np.genfromtxt("data_files/controlGroupCortisolCarroll.txt", dtype = float)
    HCDepressedCortisol = np.genfromtxt("data_files/HCDepressedCortisolCarroll.txt", dtype = float)
    LCDepressedCortisol = np.genfromtxt("data_files/LCDepressedCortisolCarroll.txt", dtype = float)

    controlACTH = np.genfromtxt("data_files/controlGroupACTHCarroll.txt", dtype = float)
    HCDepressedACTH = np.genfromtxt("data_files/HCDepressedACTHCarroll.txt", dtype = float)
    LCDepressedACTH = np.genfromtxt("data_files/LCDepressedACTHCarroll.txt", dtype = float)

    controlCortisol_rearr = np.vstack((controlCortisol[60:,:], controlCortisol[0:60,:]))
    HCDepressedCortisol_rearr = np.vstack((HCDepressedCortisol[60:,:], HCDepressedCortisol[0:60,:]))
    LCDepressedCortisol_rearr = np.vstack((LCDepressedCortisol[60:,:], LCDepressedCortisol[0:60,:]))

    controlACTH_rearr = np.vstack((controlACTH[60:,:], controlACTH[0:60,:]))
    HCDepressedACTH_rearr = np.vstack((HCDepressedACTH[60:,:], HCDepressedACTH[0:60,:]))
    LCDepressedACTH_rearr = np.vstack((LCDepressedACTH[60:,:], LCDepressedACTH[0:60,:]))

    controlCortisol_smooth = controlCortisol
    HCDepressedCortisol_smooth = HCDepressedCortisol
    LCDepressedCortisol_smooth = LCDepressedCortisol

    controlACTH_smooth = controlACTH
    HCDepressedACTH_smooth = HCDepressedACTH
    LCDepressedACTH_smooth = LCDepressedACTH

    controlCortisol_rearr_smooth = controlCortisol_rearr
    HCDepressedCortisol_rearr_smooth = HCDepressedCortisol_rearr
    LCDepressedCortisol_rearr_smooth = LCDepressedCortisol_rearr

    controlACTH_rearr_smooth = controlACTH_rearr
    HCDepressedACTH_rearr_smooth = HCDepressedACTH_rearr
    LCDepressedACTH_rearr_smooth = LCDepressedACTH_rearr

    controlCortisol_smooth[2:-2,1] = smoothing(controlCortisol[:,1])
    HCDepressedCortisol_smooth[2:-2,1] = smoothing(HCDepressedCortisol[:,1])
    LCDepressedCortisol_smooth[2:-2,1] = smoothing(HCDepressedCortisol[:,1])

    controlACTH_smooth[2:-2,1] = smoothing(controlACTH[:,1])
    HCDepressedACTH_smooth[2:-2,1] = smoothing(HCDepressedACTH[:,1])
    LCDepressedACTH_smooth[2:-2,1] = smoothing(LCDepressedACTH[:,1])

    controlCortisol_rearr_smooth[2:-2,1] = smoothing(controlCortisol_rearr[:,1])
    HCDepressedCortisol_rearr_smooth[2:-2,1] = smoothing(HCDepressedCortisol_rearr[:,1])
    LCDepressedCortisol_rearr_smooth[2:-2,1] = smoothing(LCDepressedCortisol_rearr[:,1])

    controlACTH_rearr_smooth[2:-2,1] = smoothing(controlACTH_rearr[:,1])
    HCDepressedACTH_rearr_smooth[2:-2,1] = smoothing(HCDepressedACTH_rearr[:,1])
    LCDepressedACTH_rearr_smooth[2:-2,1] = smoothing(LCDepressedACTH_rearr[:,1])

    controlCortisol = np.genfromtxt("data_files/controlGroupCortisolCarroll.txt", dtype = float)
    HCDepressedCortisol = np.genfromtxt("data_files/HCDepressedCortisolCarroll.txt", dtype = float)
    LCDepressedCortisol = np.genfromtxt("data_files/LCDepressedCortisolCarroll.txt", dtype = float)

    controlACTH = np.genfromtxt("data_files/controlGroupACTHCarroll.txt", dtype = float)
    HCDepressedACTH = np.genfromtxt("data_files/HCDepressedACTHCarroll.txt", dtype = float)
    LCDepressedACTH = np.genfromtxt("data_files/LCDepressedACTHCarroll.txt", dtype = float)

    controlCortisol_rearr = np.vstack((controlCortisol[60:,:], controlCortisol[0:60,:]))
    HCDepressedCortisol_rearr = np.vstack((HCDepressedCortisol[60:,:], HCDepressedCortisol[0:60,:]))
    LCDepressedCortisol_rearr = np.vstack((LCDepressedCortisol[60:,:], LCDepressedCortisol[0:60,:]))

    controlACTH_rearr = np.vstack((controlACTH[60:,:], controlACTH[0:60,:]))
    HCDepressedACTH_rearr = np.vstack((HCDepressedACTH[60:,:], HCDepressedACTH[0:60,:]))
    LCDepressedACTH_rearr = np.vstack((LCDepressedACTH[60:,:], LCDepressedACTH[0:60,:]))

    # change the time values of the rearranged sets so that 0 minutes is now 10AM
    #  like the non-rearranged sets
    for i in range(len(controlCortisol)):
        controlCortisol_rearr[i,0] = controlCortisol[i,0]
        controlACTH_rearr[i,0] = controlACTH[i,0]
        HCDepressedCortisol_rearr[i,0] = HCDepressedCortisol[i,0]
        HCDepressedACTH_rearr[i,0] = HCDepressedACTH[i,0]
        LCDepressedCortisol_rearr[i,0] = LCDepressedCortisol[i,0]
        LCDepressedACTH_rearr[i,0] = LCDepressedACTH[i,0]

        controlCortisol_rearr_smooth[i,0] = controlCortisol[i,0]
        controlACTH_rearr_smooth[i,0] = controlACTH[i,0]
        HCDepressedCortisol_rearr_smooth[i,0] = HCDepressedCortisol[i,0]
        HCDepressedACTH_rearr_smooth[i,0] = HCDepressedACTH[i,0]
        LCDepressedCortisol_rearr_smooth[i,0] = LCDepressedCortisol[i,0]
        LCDepressedACTH_rearr_smooth[i,0] = LCDepressedACTH[i,0]

    return controlCortisol, controlCortisol_rearr, controlCortisol_smooth, controlCortisol_rearr_smooth, controlACTH, controlACTH_rearr, controlACTH_smooth, controlACTH_rearr_smooth, HCDepressedCortisol, HCDepressedCortisol_rearr, HCDepressedCortisol_smooth, HCDepressedCortisol_rearr_smooth, HCDepressedACTH, HCDepressedACTH_rearr, HCDepressedACTH_smooth, HCDepressedACTH_rearr_smooth, LCDepressedCortisol, LCDepressedCortisol_rearr, LCDepressedCortisol_smooth, LCDepressedCortisol_rearr_smooth, LCDepressedACTH, LCDepressedACTH_rearr, LCDepressedACTH_smooth, LCDepressedACTH_rearr_smooth

# Import the data from Golier et al. (2007) and save it to arrays for PTSD,
#  Non-PTSD, Trauma-exposed controls, and Non-PTSD, non-exposed controls with
#  separate arrays for cortisol and ACTH concentration data.
# As with the Carroll data, create _rearr, _smooth and _rearr_smooth versions
#  of each array.
def golier():
    PTSDCortisol = np.genfromtxt("data_files/golier-PTSD-cortisol.txt", dtype = float)
    NonPTSDTraumaExposedCortisol = np.genfromtxt("data_files/golier-non-PTSD-trauma-exposed-cortisol.txt", dtype = float)
    NonPTSDNonExposedCortisol = np.genfromtxt("data_files/golier-non-exposed-control-cortisol.txt", dtype = float)

    PTSDACTH = np.genfromtxt("data_files/golier-PTSD-ACTH.txt", dtype = float)
    NonPTSDTraumaExposedACTH = np.genfromtxt("data_files/golier-non-PTSD-trauma-exposed-ACTH.txt", dtype = float)
    NonPTSDNonExposedACTH = np.genfromtxt("data_files/golier-non-exposed-control-ACTH.txt", dtype = float)

    # rearrange the arrays so that they start at 10AM like the Yehuda data sets
    PTSDCortisol_rearr = np.vstack((PTSDCortisol[7:,:], PTSDCortisol[0:7,:]))
    NonPTSDTraumaExposedCortisol_rearr = np.vstack((NonPTSDTraumaExposedCortisol[7:,:], NonPTSDTraumaExposedCortisol[0:7,:]))
    NonPTSDNonExposedCortisol_rearr = np.vstack((NonPTSDNonExposedCortisol[7:,:], NonPTSDNonExposedCortisol[0:7,:]))

    PTSDACTH_rearr = np.vstack((PTSDACTH[3:,:], PTSDACTH[0:3,:]))
    NonPTSDTraumaExposedACTH_rearr = np.vstack((NonPTSDTraumaExposedACTH[3:,:], NonPTSDTraumaExposedACTH[0:3,:]))
    NonPTSDNonExposedACTH_rearr = np.vstack((NonPTSDNonExposedACTH[3:,:], NonPTSDNonExposedACTH[0:3,:]))

    # create the smoothed arrays
    PTSDCortisol_smooth = PTSDCortisol
    NonPTSDTraumaExposedCortisol_smooth = NonPTSDTraumaExposedCortisol
    NonPTSDNonExposedCortisol_smooth = NonPTSDNonExposedCortisol
    PTSDACTH_smooth = PTSDACTH
    NonPTSDTraumaExposedACTH_smooth = NonPTSDTraumaExposedACTH
    NonPTSDNonExposedACTH_smooth = NonPTSDNonExposedACTH

    PTSDCortisol_smooth[2:-2,1] = smoothing(PTSDCortisol[:,1])
    NonPTSDTraumaExposedCortisol_smooth[2:-2,1] = smoothing(NonPTSDTraumaExposedCortisol[:,1])
    NonPTSDNonExposedCortisol_smooth[2:-2,1] = smoothing(NonPTSDNonExposedCortisol[:,1])

    PTSDACTH_smooth[2:-2,1] = smoothing(PTSDACTH[:,1])
    NonPTSDTraumaExposedACTH_smooth[2:-2,1] = smoothing(NonPTSDTraumaExposedACTH[:,1])
    NonPTSDNonExposedACTH_smooth[2:-2,1] = smoothing(NonPTSDNonExposedACTH[:,1])

    PTSDCortisol_rearr_smooth = PTSDCortisol_rearr
    NonPTSDTraumaExposedCortisol_rearr_smooth = NonPTSDTraumaExposedCortisol_rearr
    NonPTSDNonExposedCortisol_rearr_smooth = NonPTSDNonExposedCortisol_rearr
    PTSDACTH_rearr_smooth = PTSDACTH_rearr
    NonPTSDTraumaExposedACTH_rearr_smooth = NonPTSDTraumaExposedACTH_rearr
    NonPTSDNonExposedACTH_rearr_smooth = NonPTSDNonExposedACTH_rearr

    PTSDCortisol_rearr_smooth[2:-2,1] = smoothing(PTSDCortisol_rearr[:,1])
    NonPTSDTraumaExposedCortisol_rearr_smooth[2:-2,1] = smoothing(NonPTSDTraumaExposedCortisol_rearr[:,1])
    NonPTSDNonExposedCortisol_rearr_smooth[2:-2,1] = smoothing(NonPTSDNonExposedCortisol_rearr[:,1])

    PTSDACTH_rearr_smooth[2:-2,1] = smoothing(PTSDACTH_rearr[:,1])
    NonPTSDTraumaExposedACTH_rearr_smooth[2:-2,1] = smoothing(NonPTSDTraumaExposedACTH_rearr[:,1])
    NonPTSDNonExposedACTH_rearr_smooth[2:-2,1] = smoothing(NonPTSDNonExposedACTH_rearr[:,1])

    # re-run the genfromtxt() commands because the smoothing overwrites the non-smoothed
    #  arrays also, for some reason
    PTSDCortisol = np.genfromtxt("data_files/golier-PTSD-cortisol.txt", dtype = float)
    NonPTSDTraumaExposedCortisol = np.genfromtxt("data_files/golier-non-PTSD-trauma-exposed-cortisol.txt", dtype = float)
    NonPTSDNonExposedCortisol = np.genfromtxt("data_files/golier-non-exposed-control-cortisol.txt", dtype = float)

    PTSDACTH = np.genfromtxt("data_files/golier-PTSD-ACTH.txt", dtype = float)
    NonPTSDTraumaExposedACTH = np.genfromtxt("data_files/golier-non-PTSD-trauma-exposed-ACTH.txt", dtype = float)
    NonPTSDNonExposedACTH = np.genfromtxt("data_files/golier-non-exposed-control-ACTH.txt", dtype = float)

    # rearrange the arrays so that they start at 10AM like the Yehuda data sets
    PTSDCortisol_rearr = np.vstack((PTSDCortisol[7:,:], PTSDCortisol[0:7,:]))
    NonPTSDTraumaExposedCortisol_rearr = np.vstack((NonPTSDTraumaExposedCortisol[7:,:], NonPTSDTraumaExposedCortisol[0:7,:]))
    NonPTSDNonExposedCortisol_rearr = np.vstack((NonPTSDNonExposedCortisol[7:,:], NonPTSDNonExposedCortisol[0:7,:]))

    PTSDACTH_rearr = np.vstack((PTSDACTH[3:,:], PTSDACTH[0:3,:]))
    NonPTSDTraumaExposedACTH_rearr = np.vstack((NonPTSDTraumaExposedACTH[3:,:], NonPTSDTraumaExposedACTH[0:3,:]))
    NonPTSDNonExposedACTH_rearr = np.vstack((NonPTSDNonExposedACTH[3:,:], NonPTSDNonExposedACTH[0:3,:]))

    # change the time values of the rearranged sets so that 0 minutes is now 10AM
    #  like the non-rearranged sets
    for i in range(len(PTSDCortisol[:,0])):
        PTSDCortisol_rearr[i,0] = PTSDCortisol[i,0]
        PTSDCortisol_rearr_smooth[i,0] = PTSDCortisol[i,0]
        NonPTSDTraumaExposedCortisol_rearr[i,0] = NonPTSDTraumaExposedCortisol[i,0]
        NonPTSDTraumaExposedCortisol_rearr_smooth[i,0] = NonPTSDTraumaExposedCortisol[i,0]
        NonPTSDNonExposedCortisol_rearr[i,0] = NonPTSDNonExposedCortisol[i,0]
        NonPTSDNonExposedCortisol_rearr_smooth[i,0] = NonPTSDNonExposedCortisol[i,0]

    for i in range(len(PTSDACTH[:,0])):
        PTSDACTH_rearr[i,0] = PTSDACTH[i,0]
        PTSDACTH_rearr_smooth[i,0] = PTSDACTH[i,0]
        NonPTSDTraumaExposedACTH_rearr[i,0] = NonPTSDTraumaExposedACTH[i,0]
        NonPTSDTraumaExposedACTH_rearr_smooth[i,0] = NonPTSDTraumaExposedACTH[i,0]
        NonPTSDNonExposedACTH_rearr[i,0] = NonPTSDNonExposedACTH[i,0]
        NonPTSDNonExposedACTH_rearr_smooth[i,0] = NonPTSDNonExposedACTH[i,0]

    return PTSDCortisol, PTSDCortisol_rearr, PTSDCortisol_smooth, PTSDCortisol_rearr_smooth, PTSDACTH, PTSDACTH_rearr, PTSDACTH_smooth, PTSDACTH_rearr_smooth, NonPTSDTraumaExposedCortisol, NonPTSDTraumaExposedCortisol_rearr, NonPTSDTraumaExposedCortisol_smooth, NonPTSDTraumaExposedCortisol_rearr_smooth, NonPTSDTraumaExposedACTH, NonPTSDTraumaExposedACTH_rearr, NonPTSDTraumaExposedACTH_smooth, NonPTSDTraumaExposedACTH_rearr_smooth, NonPTSDNonExposedCortisol, NonPTSDNonExposedCortisol_rearr, NonPTSDNonExposedCortisol_smooth, NonPTSDNonExposedCortisol_rearr_smooth, NonPTSDNonExposedACTH, NonPTSDNonExposedACTH_rearr, NonPTSDNonExposedACTH_smooth, NonPTSDNonExposedACTH_rearr_smooth

# Import the data from Bremner et al. (2007) and save it to arrays for
#  abused PTSD, non-abused PTSD and non-abused non-PTSD control. This data set
#  only includes cortisol data, so no ACTH arrays here.
# As with the other data sets, create _rearr, _smooth and _rearr_smooth versions
#  of each array.
def bremner():
    abusedPTSDCortisol = np.genfromtxt("data_files/bremner-abused-PTSD-cortisol.txt", dtype = float)
    nonAbusedPTSDCortisol = np.genfromtxt("data_files/bremner-non-abused-PTSD-cortisol.txt", dtype = float)
    nonAbusedNonPTSDCortisol = np.genfromtxt("data_files/bremner-non-abused-non-PTSD-cortisol.txt", dtype = float)

    # rearrange the data so that we start at 10AM like the Yehuda data
    abusedPTSDCortisol_rearr = np.vstack((abusedPTSDCortisol[68:,:], abusedPTSDCortisol[0:68,:]))
    nonAbusedPTSDCortisol_rearr = np.vstack((nonAbusedPTSDCortisol[68:,:], nonAbusedPTSDCortisol[0:68,:]))
    nonAbusedNonPTSDCortisol_rearr = np.vstack((nonAbusedNonPTSDCortisol[68:,:], nonAbusedNonPTSDCortisol[0:68,:]))

    # create the smoothed arrays
    abusedPTSDCortisol_smooth = abusedPTSDCortisol
    abusedPTSDCortisol_rearr_smooth = abusedPTSDCortisol_rearr
    nonAbusedPTSDCortisol_smooth = nonAbusedPTSDCortisol
    nonAbusedPTSDCortisol_rearr_smooth = nonAbusedPTSDCortisol_rearr
    nonAbusedNonPTSDCortisol_smooth = nonAbusedNonPTSDCortisol
    nonAbusedNonPTSDCortisol_rearr_smooth = nonAbusedNonPTSDCortisol_rearr

    abusedPTSDCortisol_smooth[2:-2,1] = smoothing(abusedPTSDCortisol[:,1])
    abusedPTSDCortisol_rearr_smooth[2:-2,1] = smoothing(abusedPTSDCortisol_rearr[:,1])
    nonAbusedPTSDCortisol_smooth[2:-2,1] = smoothing(nonAbusedPTSDCortisol[:,1])
    nonAbusedPTSDCortisol_rearr_smooth[2:-2,1] = smoothing(nonAbusedPTSDCortisol_rearr[:,1])
    nonAbusedNonPTSDCortisol_smooth[2:-2,1] = smoothing(nonAbusedNonPTSDCortisol[:,1])
    nonAbusedNonPTSDCortisol_rearr_smooth[2:-2,1] = smoothing(nonAbusedNonPTSDCortisol_rearr[:,1])

    # re-run the genfromtxt() commands because the smoothing overwrites the non-smoothed
    #  arrays for some reason
    abusedPTSDCortisol = np.genfromtxt("data_files/bremner-abused-PTSD-cortisol.txt", dtype = float)
    nonAbusedPTSDCortisol = np.genfromtxt("data_files/bremner-non-abused-PTSD-cortisol.txt", dtype = float)
    nonAbusedNonPTSDCortisol = np.genfromtxt("data_files/bremner-non-abused-non-PTSD-cortisol.txt", dtype = float)

    # rearrange the data so that we start at 10AM like the Yehuda data
    abusedPTSDCortisol_rearr = np.vstack((abusedPTSDCortisol[68:,:], abusedPTSDCortisol[0:68,:]))
    nonAbusedPTSDCortisol_rearr = np.vstack((nonAbusedPTSDCortisol[68:,:], nonAbusedPTSDCortisol[0:68,:]))
    nonAbusedNonPTSDCortisol_rearr = np.vstack((nonAbusedNonPTSDCortisol[68:,:], nonAbusedNonPTSDCortisol[0:68,:]))

    # change the time steps of the rearranged arrays so that we start at 0
    for i in range(len(abusedPTSDCortisol[:,0])):
        abusedPTSDCortisol_rearr[i,0] = abusedPTSDCortisol[i,0]
        abusedPTSDCortisol_rearr_smooth[i,0] = abusedPTSDCortisol[i,0]
        nonAbusedPTSDCortisol_rearr[i,0] = nonAbusedPTSDCortisol[i,0]
        nonAbusedPTSDCortisol_rearr_smooth[i,0] = nonAbusedPTSDCortisol[i,0]
        nonAbusedNonPTSDCortisol_rearr[i,0] = nonAbusedNonPTSDCortisol[i,0]
        nonAbusedNonPTSDCortisol_rearr_smooth[i,0] = nonAbusedNonPTSDCortisol[i,0]

    return abusedPTSDCortisol, abusedPTSDCortisol_rearr, abusedPTSDCortisol_smooth, abusedPTSDCortisol_rearr_smooth, nonAbusedPTSDCortisol, nonAbusedPTSDCortisol_rearr, nonAbusedPTSDCortisol_smooth, nonAbusedPTSDCortisol_rearr_smooth, nonAbusedNonPTSDCortisol, nonAbusedNonPTSDCortisol_rearr, nonAbusedNonPTSDCortisol_smooth, nonAbusedNonPTSDCortisol_rearr_smooth

# Import the data from Dr Nelson for TSST tests on depressed and control subjects.
def nelson():
    ACTH_data = np.genfromtxt("data_files/tsst_acth_nelson.txt")
    cortisol_data = np.genfromtxt("data_files/tsst_cort_nelson.txt")
    subtypes = np.genfromtxt("data_files/nelson-MDD-subtypes.txt")

    ACTH_mean = np.zeros(11)
    cortisol_mean = np.zeros(11)
    ACTH = np.zeros((11,60))
    cortisol = np.zeros((11,60))

    # compute the mean of all patients' ACTH and cortisol concentrations at each
    #  data point
    for i in range(len(ACTH_data[1,:])-1):
        ACTH_mean[i] = np.mean(ACTH_data[:,i+1])
        cortisol_mean[i] = np.mean(cortisol_data[:,i+1])

    # create an array of the time points we have concentrations for in minutes
    t_nelson = np.array([0, 15, 30, 40, 50, 65, 80, 95, 110, 125, 140])

    # put the time points in the first column of our ACTH and cortisol arrays
    #  and the mean of all patients' concentrations in the second column
    for i in range(len(t_nelson)):
        ACTH[i,0] = t_nelson[i]
        ACTH[i,1] = ACTH_mean[i]

        cortisol[i,0] = t_nelson[i]
        cortisol[i,1] = cortisol_mean[i]

    # in the remaining columns, we put the concentrations at each data point for
    #  all remaining patients (one patient per column)
    for i in range(len(ACTH_data)):
        for j in range(len(t_nelson)):
            ACTH[j,i+2] = ACTH_data[i,j+1]
            cortisol[j,i+2] = cortisol_data[i,j+1]

    # Make lists of the indices in the ACTH and CORT arrays at which each
    #  subtype of patients are found
    atypical_indices = []
    melancholic_indices = []
    neither_indices = []
    healthy_indices = []

    for index, item in enumerate(subtypes[:,1]):
        if item == 1:
            atypical_indices.append(index)
        elif item == 2:
            melancholic_indices.append(index)
        elif item == 3:
            neither_indices.append(index)
        elif item == 4:
            healthy_indices.append(index)

    # create lists of the indices in the ACTH and CORT arrays for each subtype
    #  (we need to shift by 2 columns, because of the time column and mean
    #  concentrations columns), and the patient IDs of the patients in each
    #  subtype
    atypical_ids = []
    melancholic_ids = []
    neither_ids = []
    healthy_ids = []
    for idx, item in enumerate(atypical_indices):
        atypical_indices[idx] += 2
        atypical_ids.append(subtypes[item,0])
    for idx, item in enumerate(melancholic_indices):
        melancholic_indices[idx] += 2
        melancholic_ids.append(subtypes[item,0])
    for idx, item in enumerate(neither_indices):
        neither_indices[idx] += 2
        neither_ids.append(subtypes[item,0])
    for idx, item in enumerate(healthy_indices):
        healthy_indices[idx] += 2
        healthy_ids.append(subtypes[item,0])

    # create lists of the patients' data arrays for ACTH & CORT for each subtype

    # create lists of arrays of atypical patient CORT and ACTH data
    nelsonAtypicalCORTList = []
    nelsonAtypicalACTHList = []
    for idx in atypical_indices:
        nelsonAtypicalCORTList.append(cortisol[:,idx])
        nelsonAtypicalACTHList.append(ACTH[:,idx])

    # combine the lists of arrays into 2d arrays and transpose them so that 
    #  each patients' data is in a column
    nelsonAtypicalCORT = np.vstack(nelsonAtypicalCORTList)
    nelsonAtypicalCORT = np.transpose(nelsonAtypicalCORT)
    nelsonAtypicalACTH = np.vstack(nelsonAtypicalACTHList)
    nelsonAtypicalACTH = np.transpose(nelsonAtypicalACTH)

    # create lists of arrays of melancholic patient CORT and ACTH data
    nelsonMelancholicCORTList = []
    nelsonMelancholicACTHList = []
    for idx in melancholic_indices:
        nelsonMelancholicCORTList.append(cortisol[:,idx])
        nelsonMelancholicACTHList.append(ACTH[:,idx])

    # combine the lists of arrays into 2d arrays and transpose them so that 
    #  each patients' data is in a column
    nelsonMelancholicCORT = np.vstack(nelsonMelancholicCORTList)
    nelsonMelancholicCORT = np.transpose(nelsonMelancholicCORT)
    nelsonMelancholicACTH = np.vstack(nelsonMelancholicACTHList)
    nelsonMelancholicACTH = np.transpose(nelsonMelancholicACTH)

    # create lists of arrays of neither atypical nor melancholic MDD patient CORT and ACTH data
    nelsonNeitherCORTList = []
    nelsonNeitherACTHList = []
    for idx in neither_indices:
        nelsonNeitherCORTList.append(cortisol[:,idx])
        nelsonNeitherACTHList.append(ACTH[:,idx])

    # combine the lists of arrays into 2d arrays and transpose them so that 
    #  each patients' data is in a column
    nelsonNeitherCORT = np.vstack(nelsonNeitherCORTList)
    nelsonNeitherCORT = np.transpose(nelsonNeitherCORT)
    nelsonNeitherACTH = np.vstack(nelsonNeitherACTHList)
    nelsonNeitherACTH = np.transpose(nelsonNeitherACTH)

    # create lists of arrays of healthy patient CORT and ACTH data
    nelsonHealthyCORTList = []
    nelsonHealthyACTHList = []
    for idx in healthy_indices:
        nelsonHealthyCORTList.append(cortisol[:,idx])
        nelsonHealthyACTHList.append(ACTH[:,idx])

    # combine the lists of arrays into 2d arrays and transpose them so that 
    #  each patients' data is in a column
    nelsonHealthyCORT = np.vstack(nelsonHealthyCORTList)
    nelsonHealthyCORT = np.transpose(nelsonHealthyCORT)
    nelsonHealthyACTH = np.vstack(nelsonHealthyACTHList)
    nelsonHealthyACTH = np.transpose(nelsonHealthyACTH)

    return cortisol, ACTH, nelsonAtypicalCORT, nelsonAtypicalACTH, nelsonMelancholicCORT, nelsonMelancholicACTH, nelsonNeitherCORT, nelsonNeitherACTH, nelsonHealthyCORT, nelsonHealthyACTH, atypical_ids, melancholic_ids, neither_ids, healthy_ids

# Import the data for "Patient F" from the paper by Bangsgaard & Ottesen (2017)
#  and save the data to separate arrays for cortisol and ACTH concentration data.
#  Also create smoothed versions of these arrays with _smooth at the end of the
#  variable name.
def patientF():
    cortisol = np.genfromtxt("data_files/Bangsgaard-Ottesen-2017-patient-f-cortisol-data.txt", dtype = float)
    acth = np.genfromtxt("data_files/Bangsgaard-Ottesen-2017-patient-f-ACTH-data.txt", dtype = float)

    cortisol_smooth = cortisol
    acth_smooth = acth

    cortisol_smooth[2:-2,1] = smoothing(cortisol[:,1])
    acth_smooth[2:-2,1] = smoothing(acth[:,1])

    cortisol = np.genfromtxt("data_files/Bangsgaard-Ottesen-2017-patient-f-cortisol-data.txt", dtype = float)
    acth = np.genfromtxt("data_files/Bangsgaard-Ottesen-2017-patient-f-ACTH-data.txt", dtype = float)

    return cortisol, cortisol_smooth, acth, acth_smooth
