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
set $pick_count=0
hbreak *0x140e162d0
commands 1
silent
printf "DELTA_ENTRY count=%u flag=%u uid=%llx return=%llx\n", *(unsigned char*)($rcx+4), *(unsigned char*)($rcx+0xa285), *(unsigned long long*)($rcx+0xa286), *(unsigned long long*)$rsp
continue
end
hbreak *0x140f48330
commands 2
silent
printf "CACHE_FLAG1 count=%u uid=%llx return=%llx\n", *(unsigned char*)$rdx, *(unsigned long long*)($rdx+0xa282), *(unsigned long long*)$rsp
continue
end
hbreak *0x140d629a0
commands 3
silent
printf "PICK_CALLBACK decoded_command=%u drop=%u qty=%u def=%u return=%llx\n", *(unsigned int*)$rdx, *(unsigned int*)($rdx+4), *(unsigned int*)($rdx+0xc), *(unsigned int*)($rdx+0x11), *(unsigned long long*)$rsp
set $pick_count=$pick_count+1
if $pick_count>=2
detach
quit
end
continue
end
continue
