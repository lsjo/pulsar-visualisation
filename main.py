import csv
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from astropy.coordinates import SkyCoord


# function to get colour based on pulse period

def get_color(n):
    if n == np.nan:
        return 'k'
    elif n < 0.01:
        return "#db0909"
    elif n < 1:
        return "#dbde18"
    elif n < 5:
        return "#1ac41f"
    else:
        return "#118ebf"


# function to get colour based on spin down age

def getspindownagecolour(x):
    if x < 10000000000000:
        return "#5834eb"
    elif x < 1000000000000000:
        return "#a234eb"
    elif x < 100000000000000000:
        return "#eb3434"
    else:
        return "#0fa84c"


# function to convert strings to standard form so P1 can
# be used as a float and graphed with pyplot.

def to_standard(number):
    if type(number) == int or type(number) == float:
        return number
    if type(number) == str:
        values = number.split("e")
        new_num = float(values[0]) * (10 ** int(values[1]))
        places = abs(int(values[1]))
        new_num = round(new_num, places)
        return new_num


# function to convert the ASSOC column into a list for each pulsar

def assoc_list(assoc):
    if type(assoc) == str:
        assocList = assoc.split(",")
        return assocList
    else:
        return None
    


plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
colstring = "#;NAME;PSRJ;RAJ;DECJ;PMRA;PMDEC;PX;POSEPOCH;ELONG;ELAT;PMELONG;PMELAT;Gl;Gb;RAJD;DECJD;P0;P1;F0;F1;F2;F3;PEPOCH;DM;DM1;RM;W50;W10;UNITS;TAU_SC;S400;S1400;S2000;BINARY;T0;PB;A1;OM;ECC;TASC;EPS1;EPS2;Minimum;Median;BINCOMP;DIST;DIST_DM;DMsin(b);ZZ;XX;YY;ASSOC;SURVEY;OSURVEY;DISC.;PSR;NGLT"
columns = colstring.split(";")
data = pd.read_csv("data.txt", sep=";", usecols=columns)
data.pop("#")

snr_columns = ["#", "NAME", "RAJD", "DECJD", "P0", "P1", "F0", "ASSOC"]
snr_data = pd.read_csv("snr_pulsars.txt", sep=";", usecols=snr_columns)
snr_data.pop("#")

assoc_data = pd.read_csv("snr_objects.txt", sep=";", usecols=["#", "NAME", "ASSOC"])
assoc_data.pop("#")

snr_data["ASSOC_OBJECTS"] = assoc_data["ASSOC"]
print(snr_data)

colors = data["P0"].apply(get_color)


data["ASSOC_LIST"] = data["ASSOC"].apply(assoc_list)
snr_data["ASSOC_LIST"] = snr_data["ASSOC"].apply(assoc_list)


# graph to compare declination and right ascension of
# normal pulsars with pulsars in supernova remnants
# outlined in black and colour coded based on their period.

plt.scatter(x=data.RAJD, y=data.DECJD, c=colors, label="Normal Pulsars")
plt.xscale("linear")
plt.xlabel("Right Ascension (deg)")
plt.ylabel("Declination (deg)")


colors = snr_data["P0"].apply(get_color)
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.scatter(x=snr_data.RAJD, y=snr_data.DECJD, c=colors, edgecolors='black', label="SNR Pulsars")

plt.legend(loc="upper left")
plt.title("Position of Pulsars")
plt.show()

colors = data["P0"].apply(get_color)
colours = snr_data["P0"].apply(get_color)
data["P1Standard"] = data["P1"].apply(to_standard)
snr_data["P1Standard"] = snr_data["P1"].apply(to_standard)

# Creating columns for spin down age

data["SpinDownAge"] = data["P0"] / (data["P1Standard"] * 2)
snr_data["SpinDownAge"] = snr_data["P0"] / (snr_data["P1Standard"] * 2)

# Graph comparing P1 and P0 with spin down age as colours

normalspindowncolours = data["SpinDownAge"].apply(getspindownagecolour)
snrspindowncolours = snr_data["SpinDownAge"].apply(getspindownagecolour)

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.scatter(x=data.P0, y=data.P1Standard, label="Normal Pulsars", c=normalspindowncolours)
plt.scatter(x=snr_data.P0, y=snr_data.P1Standard, label="SNR Pulsars", edgecolors = "black", c=snrspindowncolours)
plt.xscale("log")
plt.xlabel("Period (s)")
plt.yscale("log")
plt.ylabel("Rate of Change")
plt.title("P0 vs P1 in Normal and SNR Pulsars")
plt.legend(loc = "lower right")
plt.show()
