0000000140f15ff0 mov      qword ptr [rsp + 0x10], rbx
0000000140f15ff5 mov      qword ptr [rsp + 0x18], rsi
0000000140f15ffa push     rdi
0000000140f15ffb sub      rsp, 0x60
0000000140f15fff mov      eax, dword ptr [r8 + 0x20]
0000000140f16003 mov      rdi, r8
0000000140f16006 mov      rsi, rdx
0000000140f16009 mov      rbx, rcx
0000000140f1600c test     al, 1
0000000140f1600e je       0x140f16030
0000000140f16010 movss    xmm3, dword ptr [rsp + 0x90]
0000000140f16019 mov      rbx, qword ptr [rsp + 0x78]
0000000140f1601e mov      rsi, qword ptr [rsp + 0x80]
0000000140f16026 add      rsp, 0x60
0000000140f1602a pop      rdi
0000000140f1602b jmp      0x140f16750
0000000140f16030 mov      qword ptr [rsp + 0x70], rbp
0000000140f16035 bt       eax, 0x12
0000000140f16039 jae      0x140f1610f
0000000140f1603f mov      edx, dword ptr [rip + 0x217f87b]
0000000140f16045 lea      r10, [rip + 0x217ed44]
0000000140f1604c mov      eax, edx
0000000140f1604e shr      eax, 8
0000000140f16051 movzx    ecx, al
0000000140f16054 movzx    eax, dl
0000000140f16057 mov      ecx, dword ptr [r10 + rcx*4 + 0x400]
0000000140f1605f mov      r8d, dword ptr [r10 + rax*4]
0000000140f16063 mov      eax, 0xa0a0a0a1
0000000140f16068 add      r8d, 0x16af
0000000140f1606f add      r8d, ecx
0000000140f16072 mul      r8d
0000000140f16075 shr      edx, 6
0000000140f16078 imul     eax, edx, 0x66
0000000140f1607b xor      edx, edx
0000000140f1607d sub      r8d, eax
0000000140f16080 movzx    eax, word ptr [rip + 0x217f83d]
0000000140f16087 mov      rcx, qword ptr [r10 + r8*8 + 0x800]
0000000140f1608f mov      r8, qword ptr [rdi + 0x28]
0000000140f16093 xor      rcx, rax
0000000140f16096 mov      rax, qword ptr [rcx + 0x16a0]
0000000140f1609d mov      r11d, dword ptr [rax + 0x48]
0000000140f160a1 mov      r10, qword ptr [rax + 0x40]
0000000140f160a5 mov      eax, r8d
0000000140f160a8 div      r11d
0000000140f160ab mov      rax, qword ptr [r10 + rdx*8]
0000000140f160af test     rax, rax
0000000140f160b2 je       0x140f160c2
0000000140f160b4 cmp      r8, qword ptr [rax]
0000000140f160b7 je       0x140f160c6
0000000140f160b9 mov      rax, qword ptr [rax + 0x18]
0000000140f160bd test     rax, rax
0000000140f160c0 jne      0x140f160b4
0000000140f160c2 mov      rax, qword ptr [r10 + r11*8]
0000000140f160c6 mov      rcx, r11
0000000140f160c9 cmp      rax, qword ptr [r10 + rcx*8]
0000000140f160cd je       0x140f16297
0000000140f160d3 mov      rbp, qword ptr [rax + 8]
0000000140f160d7 test     rbp, rbp
0000000140f160da je       0x140f16297
0000000140f160e0 mov      r8d, dword ptr [rsi + 0x18]
0000000140f160e4 mov      rdx, rdi
0000000140f160e7 mov      rcx, rbx
0000000140f160ea call     0x140f17360
0000000140f160ef mov      rax, qword ptr [rbx]
0000000140f160f2 test     byte ptr [rax + 0x68], 1
0000000140f160f6 je       0x140f16297
0000000140f160fc mov      r8, rdi
0000000140f160ff mov      rdx, rbp
0000000140f16102 mov      rcx, rsi
0000000140f16105 call     0x141310510
0000000140f1610a jmp      0x140f16297
0000000140f1610f bt       eax, 0xe
0000000140f16113 jae      0x140f16292
0000000140f16119 call     0x140f69f70
0000000140f1611e xor      ebp, ebp
0000000140f16120 test     rax, rax
0000000140f16123 je       0x140f161df
0000000140f16129 mov      rdx, qword ptr [rax]
0000000140f1612c mov      rcx, rax
