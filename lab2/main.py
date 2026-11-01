import math
import matplotlib.pyplot as plt
import numpy as np

f_carrier = 1.8
num_sectors = 3
area_total = 100.0
area_micro = 4.0
tx_power_bs = 46.0
tx_power_ue = 24.0
ant_gain_bs = 21.0
mimo_gain = 3.0 
feeder_loss = 2.0 + 0.4 + 0.5
penetration_m = 15.0
im = 1.0
bw_dl = 20 * 10**6
nf_ue = 6.0
sinr_dl = 2.0 
bw_ul = 10 * 10**6
nf_bs = 2.4
sinr_ul = 4.0

h_bs = 30
h_ms = 1.5

A = 46.3
B = 33.9

#1 & 2

thermal_noise_dl = -174 + 10 * math.log10(bw_dl)
thermal_noise_ul = -174 + 10 * math.log10(bw_ul)

rx_sens_ue = nf_ue + thermal_noise_dl + sinr_dl
rx_sens_bs = nf_bs + thermal_noise_ul + sinr_ul

mapl_ul = tx_power_ue - feeder_loss + ant_gain_bs + mimo_gain - im - penetration_m - rx_sens_bs
mapl_dl = tx_power_bs - feeder_loss + ant_gain_bs + mimo_gain - im - penetration_m - rx_sens_ue

print("MAPL_UL : ", mapl_ul, "dB")
print("MAPL_DL : ", mapl_dl, "dB")

#3

def pl_fspm(d):
    f_hz = f_carrier * 1e9
    c = 3e8
    return 20 * np.log10((4 * np.pi * d * f_hz) / c)

def pl_uminlos(d):
    return 26 * np.log10(f_carrier) + 22.7 + 36.7 * np.log10(d)

def pl_cost231(d_meters):
    d_k = d_meters / 1000.0

    a_h_ms = 3.2 * (np.log10(11.75 * h_ms)) ** 2 - 4.97

    l_clutter = 0.0

    s = np.where(d_k >= 1.0, 44.9 - 6.55 * np.log10(f_carrier * 1000), (47.88 + 13.9 * np.log10(f_carrier * 1000) - 13.9 * np.log10(h_bs)) * (1 / np.log10(50)))

    pl = (A + B * np.log10(f_carrier * 1000) - 13.82 * np.log10(h_bs) - a_h_ms + s * np.log10(d_k) + l_clutter)
    return pl

d_m = np.linspace(1, 5000, 1000)

loss_fspm = pl_fspm(d_m)
loss_uminlos = pl_uminlos(d_m)
loss_cost231 = pl_cost231(d_m)

plt.figure()
plt.plot(d_m, loss_fspm, "g--", label="FSPM")
plt.plot(d_m, loss_uminlos, "b-.", label="UMiNLOS")
plt.plot(d_m, loss_cost231, "r-", label="COST 231")
plt.axhline(y=mapl_ul, color="orange", linestyle=":", label=f"MAPL UL = {mapl_ul:.2f} dB")
plt.axhline(y=mapl_dl, color="purple", linestyle=":", label=f"MAPL DL = {mapl_dl:.2f} dB")
plt.xlabel("Расстояние между приемником и передатчиком, m", fontsize=10)
plt.ylabel("PL, dB", fontsize=10)
plt.grid()
plt.legend()
plt.show()


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
ax1.plot(d_m, loss_uminlos, label="UMiNLOS")
ax1.axhline(y=mapl_ul, color="orange", linestyle=":", label=f"MAPL UL = {mapl_ul:.2f} dB")
ax1.axhline(y=mapl_dl, color="purple", linestyle=":", label=f"MAPL DL = {mapl_dl:.2f} dB")
ul_1 = np.argmin(np.abs(loss_uminlos - mapl_ul))
dl_1 = np.argmin(np.abs(loss_uminlos - mapl_dl))
ax1.axvline(x=d_m[ul_1], label=f"R UL = {d_m[ul_1]:.1f} m")
ax1.axvline(x=d_m[dl_1], label=f"R DL = {d_m[dl_1]:.1f} m")
ax1.set_xlabel("Расстояние между приемником и передатчиком, m", fontsize=10)
ax1.set_ylabel("PL, dB", fontsize=10)
ax1.grid()
ax1.legend()
ax1.set_ylim(0, 200)
ax1.set_xlim(-10, 5000)

ax2.plot(d_m, loss_cost231, label="COST 231")
ax2.axhline(y=mapl_ul, color="orange", linestyle=":", label=f"MAPL UL = {mapl_ul:.2f} dB")
ax2.axhline(y=mapl_dl, color="purple", linestyle=":", label=f"MAPL DL = {mapl_dl:.2f} dB")
ul_2 = np.argmin(np.abs(loss_cost231 - mapl_ul))
dl_2 = np.argmin(np.abs(loss_cost231 - mapl_dl))
ax2.axvline(x=d_m[ul_2], label=f"R UL = {d_m[ul_2]:.1f} m")
ax2.axvline(x=d_m[dl_2], label=f"R DL = {d_m[dl_2]:.1f} m")
ax2.set_xlabel("Расстояние между приемником и передатчиком, m", fontsize=10)
ax2.grid()
ax2.legend()
ax2.set_ylim(0, 200)
ax2.set_xlim(-10, 5000)
plt.tight_layout()
plt.show()

# 4

# COST231

a_h_ms = 3.2 * (math.log10(11.75 * h_ms)) ** 2 - 4.97
s_macro = 44.9 - 6.55 * math.log10(f_carrier * 1000)
const_part = A + B * math.log10(f_carrier * 1000) - 13.82 * math.log10(h_bs) - a_h_ms

r_macro_ul = 10 ** ((mapl_ul - const_part) / s_macro)
r_macro_dl = 10 ** ((mapl_dl - const_part) / s_macro)

if r_macro_ul < 1.0:
    s_macro_2 = (47.88 + 13.9 * math.log10(f_carrier * 1000) - 13.9 * math.log10(h_bs)) / math.log10(50)
    r_macro_ul = 10 ** ((mapl_ul - const_part) / s_macro_2)

if r_macro_dl < 1.0:
    s_macro_2 = (47.88 + 13.9 * math.log10(f_carrier * 1000) - 13.9 * math.log10(h_bs)) / math.log10(50)
    r_macro_dl = 10 ** ((mapl_dl - const_part) / s_macro_2)

s_site_macro = 1.95 * (min(r_macro_ul, r_macro_dl)**2)
num_bs_macro = math.ceil(area_total / s_site_macro)

# UMiNLOS

r_micro_ul = (10 ** ((mapl_ul - 26 * math.log10(f_carrier) - 22.7) / 36.7)) / 1000
r_micro_dl = (10 ** ((mapl_dl - 26 * math.log10(f_carrier) - 22.7) / 36.7)) / 1000

s_site_micro = 1.95 * (min(r_micro_ul, r_micro_dl)**2)
num_bs_micro = math.ceil(area_micro / s_site_micro)

print(f"\nmin BS (COST231): {num_bs_macro}")
print(f"Radius BS DL: {r_macro_dl:.3f} км")
print(f"Radius BS UL: {r_macro_ul:.3f} км")
print(f"BS DL area: {s_site_macro:.3f} кв. км")
print(f"min BS (UMiNLOS): {num_bs_micro}")
print(f"BS UL area: {s_site_micro:.3f} кв. км")