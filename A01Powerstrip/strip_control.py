from KasaSmartPowerStrip import SmartPowerStrip
import subprocess
import os
import time
power_strip = SmartPowerStrip('192.168.50.70')
print(power_strip.get_system_info())
for i in range(0,6):
	print(power_strip.get_plug_info(i))
print(power_strip.toggle_plug('off', plug_name='pump'))

state = 0  # 0 - off, 1 - on
ii = 0
while True:
	result = subprocess.run(['xbutil', 'query'], stdout=subprocess.PIPE)
	msg = str(result.stdout)
	idx = msg.find('Temperature')
	msg = msg[idx:idx + 280].replace('\\n', ' ')
	temp = [int(s) for s in msg.split() if s.isdigit()]
	start = 0  # 0 turn on , 1 turn off
	if temp[0] > 40 or temp[1] > 40 or temp[2] > 45 or temp[3] > 40 or \
		temp[4] > 40:
		start = 1
	if start == 1 and state == 0:
		print('[Action] Turn on the pump:{0}'.format(
			power_strip.toggle_plug('on', plug_name='pump')))
		state = 1
	elif start == 0 and state == 1:
		print('[Action] Turn off the pump:{0}'.format(
			power_strip.toggle_plug('off', plug_name='pump')))
		state = 0
	else:
		print('[Action] Do nothing')
	print('[Monitor {0}] PCB_TOP: {1}, PCB_REAR: {2}, VCC: {3}, FPGA: {4}, TCRIT: {5}'.format(ii, temp[0], temp[1], temp[2], temp[3], temp[4]))
	if state == 1:
		time.sleep(10)
	else:
		time.sleep(60)
	ii = ii + 1
