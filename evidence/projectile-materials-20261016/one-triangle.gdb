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
  geom=read(shape+0x40,'<Q')[0]+0x38 if read(shape+0x38,'<B')[0]&1 else shape+0x98
  typ=read(geom,'<I')[0]
  mesh=read(geom+40,'<Q')[0] if typ==5 else 0
  if mesh:
   count,faces=read(mesh+32,'<II');face=read(a+16,'<I')[0]
   assert 0<count<100000 and face<faces<100000
   vertices,triangles=read(mesh+40,'<QQ')
   ids=read(triangles+face*6,'<3H');ids32=read(triangles+face*12,'<3I')
   assert max(ids)<count
   ap=read(actor+0x60,'<Q')[0]+0xb0 if read(actor+0x58,'<B')[0]&0x40 else actor+0x90
   sp=read(shape+0x40,'<Q')[0] if read(shape+0x38,'<B')[0]&4 else shape+0x70
   print('ONE_TRIANGLE '+json.dumps({'face':face,'indices16':ids,'indices32_candidate':ids32,'vertices_local':[read(vertices+idx*12,'<3f') for idx in ids],'actor_pose':read(ap,'<7f'),'shape_pose':read(sp,'<7f'),'native_point':read(a+28,'<3f'),'native_normal':read(a+40,'<3f')}))
  if mesh: print('MESH_BOUNDS '+json.dumps({'counts':read(mesh+32,'<II'),'bounds':read(mesh+192,'<6f'),'format_flags':read(mesh+224,'<B')[0],'actor_extra_methods':[hex(x) for x in read(read(actor,'<Q')[0]+192,'<8Q')]}))
  print('SHAPE_GEOMETRY '+json.dumps({'type':typ,'scale_quaternion':read(geom+4,'<7f') if typ==5 else None,'geometry_flags':read(geom+32,'<I')[0] if typ==5 else None,'mesh_methods':[hex(x) for x in read(read(read(geom+40,'<Q')[0],'<Q')[0],'<16Q')] if typ==5 else None,'actor_methods':[hex(x) for x in read(read(actor,'<Q')[0],'<24Q')]}))
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
