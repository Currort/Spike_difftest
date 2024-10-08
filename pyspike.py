import pexpect
import sys
import csv
import time
import copy
# log=open("pyspike_log.txt","w")
# spike = pexpect.spawn('spike -d pk hello',encoding="utf-8")
# spike.logfile_read=log
# spike.sendline('')
# spike.expect(['\n\(',pexpect.EOF, pexpect.TIMEOUT])
# print(spike.before)


# output=spike.read()
# log.write(output)
# log.close()
class pyspike(pexpect.spawn):
    """
    实例化请参考spawn类传入shell命令
    封装了pexpect库的spawn类，操控spike模拟器
    实现单步调试，扫描寄存器、内存，表达式求值，监视点，difftest功能
    """
    reg = dict.fromkeys(['clk_cnt','pc','current_iaddr','zero','ra','sp','gp','tp',
           't0','t1','t2','t3','t4','t5','t6',
           'a0','a1','a2','a3','a4','a5','a6','a7',
           's0','s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11'])
    watch = []
    watch_last = []
    csv_file = 0
    def __init__(self, command, args=[], timeout=10, maxread=2000,
                 searchwindowsize=None, logfile=None, cwd=None, env=None,
                 ignore_sighup=False, echo=True, preexec_fn=None,
                 encoding='utf-8', codec_errors='strict', dimensions=None,
                 use_poll=False, delaybeforesend:float =None) -> None:
        super().__init__(command, args, timeout, maxread, searchwindowsize, logfile, cwd, env, ignore_sighup, echo, preexec_fn, encoding, codec_errors, dimensions, use_poll)
        self.reg['clk_cnt'] = 0
        self.delaybeforesend = delaybeforesend
    def run_for_start(self, start_pc=''):
        if start_pc =='' :
            print("start_pc 未定义 !")
            return
        self.sendline('until pc 0 ' + start_pc)
        self.expect(['\n\('])
        
    def reg_get(self):
        self.sendline('reg 0 ')   
        self.expect(['\n\('])
        for j in range(8):
            for ii in range(4):
                i=ii*-24+j*-96+j*-2;
                x=self.before[-25+i:-21+i].strip()
                y=int(self.before[-19+i:-1+i],16)
                z=self.before[-19+i:-1+i]
                if x in self.reg :
                    self.reg[x]=y
                else:
                    print("%s : %s 找不到字典"%(x,z))
        self.sendline('pc 0')
        self.expect(['\n\('])
        self.reg['current_iaddr'] = self.reg['pc']
        self.reg['pc']=int(self.before[-19:-1],16)
    
    def reg_read(self,reg_name:str=None)-> int:
        """
        读取指定寄存器
        """
        if reg_name in self.reg:
            if self.reg[reg_name] == None:
                print('寄存器状态未获取')
            else:
                print(reg_name + ' : 0x{:0>18X}'.format(self.reg[reg_name]))
                return self.reg[reg_name]
        else:
            print('未找到该寄存器：%s'%reg_name)
    
    def mem_read(self,mem_addr:int)->int:
        """
        读取指定地址内存，请传入内存地址的int类型
        """
        x='0x{:0>18X}'.format(mem_addr)
        self.sendline('mem 0 %s'%x)
        self.expect(['\n\('])
        return int(self.before[-19:-1],16)
        
    def run(self,steps:int = 1):
        """
        运行，默认运行1步
        """
        for i in range(steps):
            self.reg['clk_cnt'] = self.reg['clk_cnt'] + 1
            self.sendline('')
            self.expect(['\n\('])
            self.reg_get()
            self.watch_check()
    def run_all(self):
        """
        运行，直到停止或退出
        """
        self.sendline('run')
     
    def watch_append(self,watch_name:str = None):
        """
        添加监视点，支持寄存器表达式求值，表达式要求为bool类型
        """
        if isinstance(eval(watch_name,{},self.reg),bool):
            self.watch.append(watch_name)
            self.watch_last.append(None)
            self.watch_check()
        else:
            print('表达式错误，结果需要为bool类型')
            
    def watch_check(self)->bool:
        text=''
        for i in range(len(self.watch)):
            x = eval(self.watch[i],{},self.reg)
            if self.watch_last[i] == None:
                text+=('监视点%d: \'%s\' '%(i,self.watch[i]) + 'None --> %d\n'%x)
                self.watch_last[i]=x
                print(self.watch_last[i])
            elif x == self.watch_last[i]:
                continue
            else:
                text+=('监视点%d: \'%s\' '%(i,self.watch[i]) +'%d --> %d\n'%(self.watch_last[i],x))
                self.watch_last[i]=x
        if text=='':
            return False
        else:    
            print('监视点更新!\n'+text)
            return True
        
    def write_csv(self, csv_path:str, hex_out:bool):
        if(hex_out):
            c_reg = copy.deepcopy(self.reg)
            for key, value in c_reg.items():
                c_reg[key] = hex(value)[2:]
            if self.csv_file:
                with open(csv_path, 'a', newline='') as csv_file:  
                    writer = csv.DictWriter(csv_file, c_reg.keys())
                    writer.writerow(c_reg) 
            else:
                with open(csv_path, 'w', newline='') as csv_file:  
                    writer = csv.DictWriter(csv_file, c_reg.keys())
                    writer.writeheader()
                    writer.writerow(c_reg)         
                    
            self.csv_file = 1;
        else:
            if self.csv_file:
                with open(csv_path, 'a', newline='') as csv_file:  
                    writer = csv.DictWriter(csv_file, self.reg.keys())
                    writer.writerow(self.reg) 
            else:
                with open(csv_path, 'w', newline='') as csv_file:  
                    writer = csv.DictWriter(csv_file, self.reg.keys())
                    writer.writeheader()
                    writer.writerow(self.reg)         
            self.csv_file = 1;
        
        












