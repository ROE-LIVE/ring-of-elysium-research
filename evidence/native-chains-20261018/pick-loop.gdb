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
hbreak *0x140bafc90 if *(unsigned int*)$r8==0x3b64
commands 1
silent
printf "MESSAGE_LOOP decoded_command=%x drop=%u qty=%u def=%u caller=%llx\n", *(unsigned int*)$rdx, *(unsigned int*)($rdx+4), *(unsigned int*)($rdx+0xc), *(unsigned int*)($rdx+0x11), *(unsigned long long*)$rsp
detach
quit
end
continue
