0000000140f16880 mov      eax, dword ptr [r14 + 0x70]
0000000140f16884 movzx    r9d, byte ptr [rbp + 0x24]
0000000140f16889 test     eax, eax
0000000140f1688b jne      0x140f168a3
0000000140f1688d mov      r8, rbp
0000000140f16890 movss    dword ptr [rsp + 0x20], xmm7
0000000140f16896 mov      rdx, rsi
0000000140f16899 mov      rcx, r14
0000000140f1689c call     0x14130e510
0000000140f168a1 jmp      0x140f168bc
0000000140f168a3 cmp      eax, 1
0000000140f168a6 jne      0x140f168bc
0000000140f168a8 mov      r8, rbp
0000000140f168ab movss    dword ptr [rsp + 0x20], xmm7
0000000140f168b1 mov      rdx, rsi
0000000140f168b4 mov      rcx, r14
0000000140f168b7 call     0x14130e7d0
0000000140f168bc mov      rax, qword ptr [rdi]
0000000140f168bf test     byte ptr [rax + 0x68], 1
0000000140f168c3 je       0x140f16912
0000000140f168c5 mov      rax, qword ptr [rsi]
0000000140f168c8 mov      rcx, rsi
0000000140f168cb mov      rbx, qword ptr [rsi + 0x28]
0000000140f168cf mov      rdi, qword ptr [rip + 0x21137da]
0000000140f168d6 call     qword ptr [rax + 0x1a8]
0000000140f168dc mov      ecx, dword ptr [rdi]
0000000140f168de lea      rdx, [rsp + 0x40]
0000000140f168e3 mov      qword ptr [rsp + 0x40], rbx
0000000140f168e8 movss    xmm2, dword ptr [rax + 4]
0000000140f168ed movss    xmm0, dword ptr [rax + 8]
0000000140f168f2 movss    xmm1, dword ptr [rax]
0000000140f168f6 movss    dword ptr [rsp + 0x38], xmm0
0000000140f168fc mov      eax, dword ptr [rsp + 0x38]
0000000140f16900 unpcklps xmm1, xmm2
0000000140f16903 movsd    qword ptr [rsp + 0x48], xmm1
0000000140f16909 mov      dword ptr [rsp + 0x50], eax
0000000140f1690d call     0x1404e8390
0000000140f16912 movaps   xmm7, xmmword ptr [rsp + 0x60]
0000000140f16917 lea      r11, [rsp + 0x80]
0000000140f1691f mov      rbx, qword ptr [r11 + 0x10]
0000000140f16923 mov      rbp, qword ptr [r11 + 0x18]
0000000140f16927 mov      rsi, qword ptr [r11 + 0x20]
0000000140f1692b mov      rdi, qword ptr [r11 + 0x28]
0000000140f1692f mov      rsp, r11
0000000140f16932 pop      r14
0000000140f16934 ret
