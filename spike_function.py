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
    封装了pexpect库的spawn类，操控spike模拟器
    实现单步调试，扫描寄存器、内存，表达式求值，监视点，difftest功能
    """
    reg = dict.fromkeys(['zero','ra','sp','gp','tp',
           't0','t1','t2','t3','t4','t5','t6',
           'a0','a1','a2','a3','a4','a5','a6','a7',
           's0','s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11'])
    watch = []
    def state_get(self):
        self.sendline('reg 0 ')
        self.expect(['\n\('])
        print(self.before)
        
        # x=self.before[-23:-21]
        # y=int(self.before[-19:-1],16)
        for j in range(8):
            for ii in range(4):
                i=ii*-24+j*-96+j*-2;
                x=self.before[-25+i:-21+i].strip()
                print('i=%d'%(i))
                print('ii=%d'%(ii))
                print('j=%d'%(j))
                print('y= %s'%(self.before[-19+i:-1+i]))
                y=int(self.before[-19+i:-1+i],16)
                z=self.before[-19+i:-1+i]
                if x in self.reg :
                    self.reg[x]=y
                else:
                    print("%s : %s 找不到字典"%(x,z))
                print(x)
                print(y)
                print(z)
        
        
    def read_reg(self,reg_name=None):
        """
        读取指定寄存器
        """
        pass
    
w=pyspike('spike -d pk hello',encoding="utf-8")
w.state_get()
print(w.reg)







