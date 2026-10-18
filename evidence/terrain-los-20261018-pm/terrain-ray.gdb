set pagination off
set confirm off
set print thread-events off
handle SIG32 nostop noprint pass
handle SIG33 nostop noprint pass
handle SIGUSR1 nostop noprint pass
handle SIGUSR2 nostop noprint pass
handle SIGSEGV nostop noprint pass
handle SIGQUIT nostop noprint pass
handle SIGTRAP stop noprint nopass
python
import gdb,struct,json,time
inf=gdb.selected_inferior();active={'queries':0,'query':None}
def reg(n):return int(gdb.parse_and_eval('$'+n))
def read(a,fmt):return struct.unpack(fmt,bytes(inf.read_memory(a,struct.calcsize(fmt))))
class Entry(gdb.Breakpoint):
 def stop(self):
  active['queries']+=1
  if active['queries']>80: print('QUERY_LIMIT',flush=True);return True
  origin=read(reg('r8'),'<3f');direction=read(read(reg('rsp')+0x28,'<Q')[0],'<3f');distance=float(gdb.parse_and_eval('$xmm3.v4_float[0]'))
  active['query']={'utc_ns':time.time_ns(),'origin':origin,'direction':direction,'length':distance,'end':[a+distance*d for a,d in zip(origin,direction)]}
  return False
class Hit(gdb.Breakpoint):
 def stop(self):
  a=reg('rdx'); print('TERRAIN_HIT '+json.dumps({'query':active['query'],'face_index':read(a+16,'<I')[0],'point':read(a+28,'<3f'),'normal':read(a+40,'<3f'),'distance':read(a+52,'<f')[0]}),flush=True)
  return False
class Result(gdb.Breakpoint):
 def stop(self):
  a=reg('rdi');print('TERRAIN_RESULT '+json.dumps({'point':read(a,'<3f'),'normal':read(a+12,'<3f'),'material':read(a+64,'<I')[0],'queries':active['queries']}),flush=True);return True
Entry('*0x140fc3f20',type=gdb.BP_HARDWARE_BREAKPOINT)
Hit('*0x140fc14fd',type=gdb.BP_HARDWARE_BREAKPOINT)
Result('*0x140fc15d3',type=gdb.BP_HARDWARE_BREAKPOINT)
end
continue
detach
quit
