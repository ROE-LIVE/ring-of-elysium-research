0000000141468c30 mov      qword ptr [rsp + 0x10], rbx
0000000141468c35 push     rdi
0000000141468c36 sub      rsp, 0x430
0000000141468c3d mov      rdx, qword ptr [rcx + 0x10]
0000000141468c41 xor      r9d, r9d
0000000141468c44 mov      rbx, rcx
0000000141468c47 mov      qword ptr [rsp + 0x440], r9
0000000141468c4f mov      rcx, qword ptr [rcx + 0x18]
0000000141468c53 mov      rax, rdx
0000000141468c56 sub      rax, rcx
0000000141468c59 sar      rax, 4
0000000141468c5d cmp      eax, 1
0000000141468c60 jne      0x141468dd1
0000000141468c66 cmp      rcx, rdx
0000000141468c69 lea      rdi, [rip + 0x11b2770]
0000000141468c70 mov      rax, rdi
0000000141468c73 cmovb    rax, rcx
0000000141468c77 mov      r8d, dword ptr [rax + 8]
0000000141468c7b cmp      r8d, 7
0000000141468c7f je       0x141468cf7
0000000141468c81 cmp      r8d, 2
0000000141468c85 je       0x141468cf7
0000000141468c87 cmp      rcx, rdx
0000000141468c8a jae      0x141468cb7
0000000141468c8c cmp      rcx, rdi
0000000141468c8f je       0x141468c97
0000000141468c91 cmp      dword ptr [rcx + 8], r9d
0000000141468c95 je       0x141468cf7
0000000141468c97 cmp      rcx, rdx
0000000141468c9a jae      0x141468cb7
0000000141468c9c cmp      rcx, rdi
0000000141468c9f je       0x141468cb7
0000000141468ca1 movsxd   rax, dword ptr [rcx + 8]
0000000141468ca5 cmp      eax, -1
0000000141468ca8 je       0x141468cb7
0000000141468caa lea      rcx, [rip + 0x11b27ef]
0000000141468cb1 mov      rcx, qword ptr [rcx + rax*8]
0000000141468cb5 jmp      0x141468cbe
0000000141468cb7 lea      rcx, [rip + 0x137fa5a]
0000000141468cbe mov      qword ptr [rsp + 0x28], rcx
0000000141468cc3 lea      rax, [rip + 0x13984d6]
0000000141468cca lea      rcx, [rsp + 0x30]
0000000141468ccf mov      qword ptr [rsp + 0x20], rax
0000000141468cd4 mov      r9d, 1
0000000141468cda lea      r8, [rip + 0x1398fbf]
0000000141468ce1 lea      rdx, [rip + 0x1380268]
0000000141468ce8 call     0x1404f65f0
0000000141468ced lea      rdx, [rsp + 0x30]
0000000141468cf2 jmp      0x141468dd8
0000000141468cf7 mov      dword ptr [rsp + 0x20], r9d
0000000141468cfc lea      r8, [rsp + 0x440]
0000000141468d04 mov      r9, qword ptr [rip + 0x1be1bd5]
0000000141468d0b mov      edx, 1
0000000141468d10 mov      rcx, rbx
0000000141468d13 call     0x1413a37e0
0000000141468d18 test     eax, eax
0000000141468d1a jns      0x141468d96
0000000141468d1c mov      rax, qword ptr [rbx + 0x18]
0000000141468d20 cmp      rax, qword ptr [rbx + 0x10]
0000000141468d24 jae      0x141468d44
0000000141468d26 cmp      rax, rdi
0000000141468d29 je       0x141468d44
0000000141468d2b movsxd   rcx, dword ptr [rax + 8]
0000000141468d2f cmp      ecx, -1
0000000141468d32 je       0x141468d44
0000000141468d34 mov      rax, rcx
0000000141468d37 lea      rcx, [rip + 0x11b2762]
0000000141468d3e mov      rcx, qword ptr [rcx + rax*8]
0000000141468d42 jmp      0x141468d4b
0000000141468d44 lea      rcx, [rip + 0x137f9cd]
0000000141468d4b mov      rax, qword ptr [rip + 0x1be1b8e]
0000000141468d52 test     rax, rax
0000000141468d55 je       0x141468d60
0000000141468d57 mov      rax, qword ptr [rax + 8]
0000000141468d5b test     rax, rax
0000000141468d5e jne      0x141468d67
0000000141468d60 lea      rax, [rip + 0x13802a9]
0000000141468d67 mov      qword ptr [rsp + 0x28], rcx
0000000141468d6c lea      r8, [rip + 0x1398dfd]
0000000141468d73 lea      rcx, [rsp + 0x30]
0000000141468d78 mov      qword ptr [rsp + 0x20], rax
0000000141468d7d mov      r9d, 1
0000000141468d83 lea      rdx, [rip + 0x13801c6]
0000000141468d8a call     0x1404f65f0
0000000141468d8f lea      rdx, [rsp + 0x30]
0000000141468d94 jmp      0x141468dd8
0000000141468d96 mov      rcx, qword ptr [rbx + 0x10]
0000000141468d9a mov      rax, qword ptr [rsp + 0x440]
0000000141468da2 movd     xmm0, dword ptr [rax + 0x64]
0000000141468da7 mov      eax, 1
0000000141468dac cvtdq2pd xmm0, xmm0
0000000141468db0 mov      dword ptr [rcx + 8], 3
0000000141468db7 movsd    qword ptr [rcx], xmm0
0000000141468dbb add      qword ptr [rbx + 0x10], 0x10
0000000141468dc0 mov      rbx, qword ptr [rsp + 0x448]
0000000141468dc8 add      rsp, 0x430
0000000141468dcf pop      rdi
0000000141468dd0 ret
0000000141468dd1 lea      rdx, [rip + 0x12318ac]
0000000141468dd8 mov      rcx, rbx
0000000141468ddb call     0x14139b420
0000000141468de0 mov      rcx, rbx
0000000141468de3 call     0x1418deb50
0000000141468de8 mov      rbx, qword ptr [rsp + 0x448]
0000000141468df0 xor      eax, eax
0000000141468df2 add      rsp, 0x430
0000000141468df9 pop      rdi
0000000141468dfa ret
