0000000140f16750 mov      qword ptr [rsp + 8], rbx
0000000140f16755 mov      qword ptr [rsp + 0x10], rbp
0000000140f1675a mov      qword ptr [rsp + 0x18], rsi
0000000140f1675f mov      qword ptr [rsp + 0x20], rdi
0000000140f16764 push     r14
0000000140f16766 sub      rsp, 0x80
0000000140f1676d mov      rdi, rcx
0000000140f16770 movaps   xmmword ptr [rsp + 0x60], xmm7
0000000140f16775 mov      rcx, qword ptr [r8 + 0x28]
0000000140f16779 movaps   xmm7, xmm3
0000000140f1677c mov      rbp, r8
0000000140f1677f mov      r14, rdx
0000000140f16782 call     0x1411c2db0
0000000140f16787 mov      rbx, rax
0000000140f1678a test     rax, rax
0000000140f1678d je       0x140f167c3
0000000140f1678f mov      rax, qword ptr [rax]
0000000140f16792 mov      rcx, rbx
0000000140f16795 call     qword ptr [rax + 8]
0000000140f16798 test     rax, rax
0000000140f1679b je       0x140f167c3
0000000140f1679d mov      rax, qword ptr [rbx]
0000000140f167a0 mov      rcx, rbx
0000000140f167a3 call     qword ptr [rax + 8]
0000000140f167a6 test     rax, rax
0000000140f167a9 je       0x140f167c3
0000000140f167ab lea      rcx, [rip + 0x217f7ce]
0000000140f167b2 cmp      rax, rcx
0000000140f167b5 je       0x140f1680b
0000000140f167b7 mov      rax, qword ptr [rax + 0x180]
0000000140f167be test     rax, rax
0000000140f167c1 jne      0x140f167b2
0000000140f167c3 xor      r9b, r9b
0000000140f167c6 xor      esi, esi
0000000140f167c8 test     r9b, r9b
0000000140f167cb cmovne   rsi, rbx
0000000140f167cf test     rsi, rsi
0000000140f167d2 je       0x140f16912
0000000140f167d8 mov      rbx, qword ptr [rdi]
0000000140f167db mov      rcx, rbx
