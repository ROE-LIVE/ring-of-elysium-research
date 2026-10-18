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
set $picked=0
hbreak *0x140c69b00
commands 1
silent
set $pick_out=$rcx
set $pick_reader=$rdx
printf "PICK_DECODER entry=%llx reader_offset=%llu reader_length=%llu type=%u caller=%llx\n", $pc, *(unsigned long long*)($rdx+8), *(unsigned long long*)($rdx+16), $r8d, *(unsigned long long*)$rsp
continue
end
hbreak *0x140c6c7c7
commands 2
silent
printf "PICK_DECODED result=%d drop=%u qty=%u def=%u consumed=%llu\n", $eax, *(unsigned int*)$pick_out, *(unsigned int*)($pick_out+8), *(unsigned int*)($pick_out+13), *(unsigned long long*)($pick_reader+8)
continue
end
hbreak *0x140d629a0
commands 3
silent
printf "PICK_CALLBACK decoded_command=%x same_output=%u drop=%u qty=%u def=%u caller=%llx\n", *(unsigned int*)$rdx, $rdx+4==$pick_out, *(unsigned int*)($rdx+4), *(unsigned int*)($rdx+0xc), *(unsigned int*)($rdx+0x11), *(unsigned long long*)$rsp
set $picked=1
continue
end
hbreak *0x140c4ba10 if $picked==1
commands 4
silent
printf "DELTA_DECODER entry=%llx reader_offset=%llu reader_length=%llu type=%u caller=%llx\n", $pc, *(unsigned long long*)($rdx+8), *(unsigned long long*)($rdx+16), $r8d, *(unsigned long long*)$rsp
detach
quit
end
continue
