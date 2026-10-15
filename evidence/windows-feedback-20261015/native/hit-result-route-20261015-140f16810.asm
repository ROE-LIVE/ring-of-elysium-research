0000000140f16810 call     0x140da2840
0000000140f16815 mov      rbx, qword ptr [rdi]
0000000140f16818 movss    xmm6, dword ptr [rax + 4]
0000000140f1681d mov      rcx, rbx
0000000140f16820 mov      rax, qword ptr [rbx]
0000000140f16823 call     qword ptr [rax + 0x178]
0000000140f16829 test     rax, rax
0000000140f1682c je       0x140f16848
0000000140f1682e mov      rax, qword ptr [rbx]
0000000140f16831 mov      rcx, rbx
0000000140f16834 call     qword ptr [rax + 0x178]
0000000140f1683a mov      rcx, rax
0000000140f1683d mov      rdx, qword ptr [rax]
0000000140f16840 call     qword ptr [rdx + 0x200]
0000000140f16846 jmp      0x140f1684d
0000000140f16848 call     0x140da2840
0000000140f1684d movss    xmm0, dword ptr [rax]
0000000140f16851 mov      rax, qword ptr [rsi + 0xfd8]
0000000140f16858 movss    dword ptr [rax + 0x11c], xmm6
0000000140f16860 movaps   xmm6, xmmword ptr [rsp + 0x70]
0000000140f16865 movss    dword ptr [rax + 0x118], xmm0
0000000140f1686d mov      dword ptr [rax + 0x120], 0
0000000140f16877 mov      rax, qword ptr [rdi]
0000000140f1687a test     byte ptr [rax + 0x68], 1
0000000140f1687e je       0x140f168bc
