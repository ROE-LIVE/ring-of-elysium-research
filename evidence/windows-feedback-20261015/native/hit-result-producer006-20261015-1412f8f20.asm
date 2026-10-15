00000001412f8f20 mov      qword ptr [rsp + 8], rbx
00000001412f8f25 mov      qword ptr [rsp + 0x10], rbp
00000001412f8f2a mov      qword ptr [rsp + 0x18], rsi
00000001412f8f2f mov      qword ptr [rsp + 0x20], rdi
00000001412f8f34 push     r14
00000001412f8f36 sub      rsp, 0x30
00000001412f8f3a mov      rsi, qword ptr [rcx + 0xb8]
00000001412f8f41 mov      rbx, rcx
00000001412f8f44 mov      rcx, rsi
00000001412f8f47 movzx    ebp, r9b
00000001412f8f4b mov      rdi, r8
00000001412f8f4e mov      r14, rdx
00000001412f8f51 call     0x140d8fd40
00000001412f8f56 test     rax, rax
00000001412f8f59 jne      0x1412f8f7d
00000001412f8f5b mov      rcx, qword ptr [rsi + 0x130]
00000001412f8f62 call     0x140fb3b40
00000001412f8f67 test     rax, rax
00000001412f8f6a je       0x1412f9023
00000001412f8f70 add      rax, 0x58
00000001412f8f74 test     rax, rax
00000001412f8f77 je       0x1412f9023
00000001412f8f7d mov      eax, dword ptr [rdi]
00000001412f8f7f movzx    r9d, bpl
00000001412f8f83 mov      dword ptr [rbx + 0x60], eax
00000001412f8f86 mov      r8, rdi
00000001412f8f89 mov      eax, dword ptr [rdi + 4]
00000001412f8f8c mov      rdx, r14
00000001412f8f8f mov      dword ptr [rbx + 0x64], eax
00000001412f8f92 mov      eax, dword ptr [rdi + 8]
00000001412f8f95 mov      dword ptr [rbx + 0x68], eax
00000001412f8f98 mov      eax, dword ptr [rdi + 0xc]
00000001412f8f9b mov      dword ptr [rbx + 0x6c], eax
00000001412f8f9e mov      eax, dword ptr [rdi + 0x10]
00000001412f8fa1 mov      dword ptr [rbx + 0x70], eax
00000001412f8fa4 mov      eax, dword ptr [rdi + 0x14]
00000001412f8fa7 mov      dword ptr [rbx + 0x74], eax
00000001412f8faa mov      eax, dword ptr [rdi + 0x18]
00000001412f8fad mov      dword ptr [rbx + 0x78], eax
00000001412f8fb0 movups   xmm0, xmmword ptr [rdi + 0x20]
00000001412f8fb4 movups   xmmword ptr [rbx + 0x80], xmm0
00000001412f8fbb movups   xmm1, xmmword ptr [rdi + 0x30]
00000001412f8fbf movss    xmm0, dword ptr [rsp + 0x60]
00000001412f8fc5 movups   xmmword ptr [rbx + 0x90], xmm1
00000001412f8fcc mov      eax, dword ptr [rdi + 0x40]
00000001412f8fcf mov      dword ptr [rbx + 0xa0], eax
00000001412f8fd5 mov      eax, dword ptr [rdi + 0x44]
00000001412f8fd8 mov      dword ptr [rbx + 0xa4], eax
00000001412f8fde mov      eax, dword ptr [rdi + 0x48]
00000001412f8fe1 mov      dword ptr [rbx + 0xa8], eax
00000001412f8fe7 mov      eax, dword ptr [rdi + 0x4c]
00000001412f8fea mov      dword ptr [rbx + 0xac], eax
00000001412f8ff0 mov      eax, dword ptr [rdi]
00000001412f8ff2 mov      rcx, qword ptr [rbx + 0xb8]
00000001412f8ff9 mov      dword ptr [rbx + 0x100], eax
00000001412f8fff mov      eax, dword ptr [rdi + 4]
00000001412f9002 mov      dword ptr [rbx + 0x104], eax
00000001412f9008 mov      eax, dword ptr [rdi + 8]
00000001412f900b mov      dword ptr [rbx + 0x108], eax
00000001412f9011 mov      rcx, qword ptr [rcx + 0x1318]
00000001412f9018 movss    dword ptr [rsp + 0x20], xmm0
00000001412f901e call     0x140f15ff0
00000001412f9023 mov      rbx, qword ptr [rsp + 0x40]
00000001412f9028 mov      rbp, qword ptr [rsp + 0x48]
00000001412f902d mov      rsi, qword ptr [rsp + 0x50]
00000001412f9032 mov      rdi, qword ptr [rsp + 0x58]
00000001412f9037 add      rsp, 0x30
00000001412f903b pop      r14
00000001412f903d ret
