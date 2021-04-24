from KasaSmartPowerStrip import SmartPowerStrip
import subprocess
import os
import time
power_strip = SmartPowerStrip('192.168.50.70')
print(power_strip.get_system_info())
for i in range(0,6):
	print(power_strip.get_plug_info(i))
# print(power_strip.toggle_plug('off', plug_name='pump'))
print(power_strip.get_realtime_energy_info(plug_num=3))
