import sys
import os
sys.path.append('/home/zero/master_share/pyspike')
from pyspike import pyspike 
current_path = os.path.dirname(os.path.abspath(__file__))
run_file_path = []
spike_log_path = []
arguments = sys.argv
if len(arguments) > 1:
    for i in arguments[1:]:
        run_file_path.append('/home/zero/master_share/pyVerilator/build/' + i + '/run')
        spike_log_path.append(current_path + '/csv/' + i + '/spike_log.csv')
        os.makedirs(current_path + '/csv/' + i , exist_ok= True)
else:
    print("未传递c文件名称")
    sys.exit()
print(run_file_path)
print(spike_log_path)
# run_file_path = '/home/zero/master_share/pyVerilator/build/add/run'
spike_shell = []
j = 0
FreeRTOS_num = 0
for i in run_file_path: 
    if i == '/home/zero/master_share/pyVerilator/build/FreeRTOS/run':
        spike_shell.append('spike -d -m0x2000:0x42400 --misaligned ' + i)
        FreeRTOS_num = j
    else:
        spike_shell.append('spike -d pk ' + i)
        j += 1

# spike_log_path = '/home/zero/master_share/pyspike/csv/spike_log.csv'
start_pc = '0x201a'

main = '0x2100'

for i in range(len(run_file_path)):
    w = pyspike(spike_shell[i])
    if(j == i):
        w.run_for_start('2100')
    else:
        w.run_for_start(start_pc)
    w.expect(['\n\('])
    w.reg_get()
    # w.write_csv(spike_log_path)
    # w.watch_append('pc-2==0x1004-2')
    while w.reg['pc'] != 0xffffffc000001dcc:
        w.run()
        w.write_csv(spike_log_path[i], True)
        # print(w.reg['pc'])
        if (w.reg['pc'] == 0x214C ) and (j == i):
            break

# print(w.mem_read(int('0x0000000080000000',16)))