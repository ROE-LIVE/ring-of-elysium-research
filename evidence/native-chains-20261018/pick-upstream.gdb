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
hbreak *0x140baf920 if $edx==0x3b64 || $edx==0x3e82
commands 1
silent
printf "DISPATCH opcode=%x decoded_header=%x length=%u caller=%llx\n", $edx, *(unsigned int*)$r8, $r9d, *(unsigned long long*)$rsp
continue
end
hbreak *0x140d629a0
commands 2
silent
printf "PICK_CALLBACK decoded_command=%x drop=%u qty=%u def=%u caller=%llx\n", *(unsigned int*)$rdx, *(unsigned int*)($rdx+4), *(unsigned int*)($rdx+0xc), *(unsigned int*)($rdx+0x11), *(unsigned long long*)$rsp
detach
quit
end
continue
