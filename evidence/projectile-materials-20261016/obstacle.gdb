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
import gdb, struct, json
inf=gdb.selected_inferior()
def reg(n): return int(gdb.parse_and_eval('$'+n))
def read(a,fmt): return struct.unpack(fmt,bytes(inf.read_memory(a,struct.calcsize(fmt))))
class Result(gdb.Breakpoint):
 def stop(self):
  a=reg('rdi');print('OBSTACLE_RESULT '+json.dumps({'point':read(a,'<3f'),'normal':read(a+12,'<3f'),'distance':read(a+24,'<f')[0],'flags_part':read(a+32,'<2I'),'material':read(a+64,'<I')[0],'shape_flags':read(a+72,'<2I')}));return True
class Hit(gdb.Breakpoint):
 def stop(self):
  a=reg('rdx');actor,shape=read(a,'<QQ');ud=read(actor+16,'<Q')[0]
  print('OBSTACLE_HIT '+json.dumps({'face_index':read(a+16,'<I')[0],'actor_vtable':hex(read(actor,'<Q')[0]),'shape_vtable':hex(read(shape,'<Q')[0]),'metadata':read(ud,'<IIQ') if ud else None,'point':read(a+28,'<3f'),'normal':read(a+40,'<3f'),'distance':read(a+52,'<f')[0],'shape_methods':[hex(x) for x in read(read(shape,'<Q')[0],'<28Q')]}));self.enabled=False;result.enabled=True;return False
class Entry(gdb.Breakpoint):
 def stop(self):self.enabled=False;hit.enabled=True;return False
result=Result('*0x140fc15d3',type=gdb.BP_HARDWARE_BREAKPOINT);result.enabled=False
hit=Hit('*0x140fc14fd',type=gdb.BP_HARDWARE_BREAKPOINT);hit.enabled=False
entry=Entry('*0x140fc3f20',type=gdb.BP_HARDWARE_BREAKPOINT)
end
continue
detach
quit
