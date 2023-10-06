import pexpect
import sys
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
    实例化请参考spawn类传入shell命令，以及 encoding="utf-8"
    封装了pexpect库的spawn类，操控spike模拟器
    实现单步调试，扫描寄存器、内存，表达式求值，监视点，difftest功能
    """
    reg = dict.fromkeys(['pc','zero','ra','sp','gp','tp',
           't0','t1','t2','t3','t4','t5','t6',
           'a0','a1','a2','a3','a4','a5','a6','a7',
           's0','s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11'])
    watch = []
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
        self.reg['pc']=int(self.before[-19:-1],16)
        
    def read_reg(self,reg_name:str=None):
        """
        读取指定寄存器
        """
        if reg_name in self.reg:
            if self.reg[reg_name] == None:
                print('寄存器状态未获取')
            else:
                print(reg_name + ' : 0x{:0>18X}'.format(self.reg[reg_name]))
        else:
            print('未找到该寄存器：%s'%reg_name)
            
    def run(self,steps:int = 1):
        for i in range(steps):
            self.sendline('')
            self.expect(['\n\('])
            self.reg_get()
            print(self.reg)
            
            
w=pyspike('spike -d pk abc',encoding="utf-8")
w.reg_get()
w.read_reg('a0')
w.run()







