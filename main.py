import fastf1 as f1
import fastf1.plotting
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# f1.Cache.enable_cache('fastf1-cache')
f1.plotting.setup_mpl(mpl_timedelta_support=False, color_scheme='fastf1')

session = f1.get_session(2025, 'Austria', 'Race')
session.load(telemetry=True, weather=True)

laps = session.laps
print(laps.columns)
laps_nor = laps.pick_drivers('NOR')[["LapNumber", "LapTime", "Position", "Compound", "TyreLife"]].sort_values(by="LapTime", ascending=True)
print(laps_nor)

tel_nor = laps.pick_drivers('NOR').get_telemetry()
print(tel_nor.columns)
print(tel_nor.head())

topLap = laps.pick_drivers("NOR").pick_fastest()
print(topLap)
tel_topLap = topLap.get_telemetry()
print(tel_topLap.head())


### TELEMETRY PLOTS ###
fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
ax[0].plot(tel_topLap['Distance'], tel_topLap['Speed'])
ax[0].set_ylabel('Speed (km/h)')
ax[1].plot(tel_topLap['Distance'], tel_topLap['Throttle'], color='orange')
ax[1].set_ylabel("Throttle (%)")
ax[1].set_xlabel("Distance (m)")
plt.tight_layout()
plt.show()



### LAP TIME COMPARISON ###
drv1 = session.laps.pick_drivers('LEC').pick_fastest()
drv2 = session.laps.pick_drivers('HAM').pick_fastest()
print('LEC: ', drv1['LapTime'])
print('HAM: ', drv2['LapTime'])


tel_drv1 = drv1.get_telemetry().add_distance()
tel_drv2 = drv2.get_telemetry().add_distance()

fig2, ax2 = plt.subplots(1, 1, figsize=(10, 4))
ax2.plot(tel_drv1['Distance'], tel_drv1['Speed'], label='LEC')
ax2.plot(tel_drv2['Distance'], tel_drv2['Speed'], label='HAM')
ax2.set_xlabel('Distance (m)')
ax2.set_ylabel('Speed (km/h)')
ax2.legend()
plt.tight_layout()
plt.show()


############## DASHBOARD SETUP ##############

st.set_page_config(page_title="📊 F1 Data Dashboard", layout="wide")
st.title("📊 F1 Data Dashboard")

st.text_input("Driver Name", value="NOR")
st.dataframe(laps_nor)











# fig, ax = plt.subplots(figsize=(8, 5))
#
# for drv in session.drivers:
#     drv_laps = session.laps.pick_drivers(drv)
#     name = drv_laps["Driver"].iloc[0]
#     style = f1.plotting.get_driver_style(identifier=name, style=['color', 'linestyle'], session=session)
#     ax.plot(drv_laps['LapNumber'], drv_laps['Position'], label=name, **style)
#
# ax.set_ylim([20.5, 0.5])
# ax.set_yticks([1, 5, 10, 15, 20])
# ax.set_xlabel('Lap')
# ax.set_ylabel('Position')
# ax.legend(bbox_to_anchor=(1.0, 1.02))
# plt.tight_layout()
#
# plt.show()



