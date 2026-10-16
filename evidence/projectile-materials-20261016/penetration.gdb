set pagination off
set confirm off
set print frame-arguments none
handle SIG32 nostop noprint pass
handle SIG33 nostop noprint pass
handle SIGUSR1 nostop noprint pass
handle SIGUSR2 nostop noprint pass
handle SIGSEGV nostop noprint pass
handle SIGQUIT nostop noprint pass
handle SIGTRAP stop noprint nopass
python
import gdb,struct,json
inf=gdb.selected_inferior();seen=None
def reg(n):return int(gdb.parse_and_eval('$'+n))
def read(a,fmt):return struct.unpack(fmt,bytes(inf.read_memory(a,struct.calcsize(fmt))))
def xmm(n):return float(gdb.parse_and_eval('$xmm%d.v4_float[0]'%n))
class Point(gdb.Breakpoint):
 def __init__(self,pc,kind):self.kind=kind;super().__init__('*'+pc,type=gdb.BP_HARDWARE_BREAKPOINT)
 def stop(self):
  global seen
  if self.kind=='material':
   m=reg('rsi')
   if read(m,'<I')[0]!=305:return False
   seen=reg('rdi');print('MATERIAL '+json.dumps({'id':305,'modifier_lost':read(m+0x38,'<2f'),'no_average':read(m+0x40,'<B')[0],'flag_1d0':read(seen+0x1d0,'<B')[0],'power':read(seen+0x1b4,'<f')[0],'energy':read(seen+0x1bc,'<f')[0]}))
  elif seen and self.kind=='formula':
   print('FORMULA_INPUT '+json.dumps({'modifier':xmm(6),'lost_percent':xmm(8),'entry':read(reg('r14')+16,'<3f'),'exit':read(reg('r15')+16,'<3f'),'energy':read(seen+0x1bc,'<f')[0],'power':read(seen+0x1b4,'<f')[0],'constants':[xmm(i) for i in (9,12,13,14,15)]}))
  elif seen and self.kind=='loss':
   print('FORMULA_LOSS '+json.dumps({'before':xmm(5),'loss':xmm(0),'after_predicted':xmm(5)-xmm(0)}))
  elif seen and self.kind=='return':
   print('FORMULA_RETURN '+json.dumps({'energy':read(seen+0x1bc,'<f')[0],'return_al':reg('rax')&255}));return True
  return False
Point('0x140fc4404','material')
Point('0x140fc4898','formula')
Point('0x140fc4956','loss')
Point('0x140fc4bc4','return')
end
continue
detach
quit
