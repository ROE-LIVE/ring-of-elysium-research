0000000141467bf0 mov      qword ptr [rsp + 0x10], rbx
0000000141467bf5 push     rdi
0000000141467bf6 sub      rsp, 0x430
0000000141467bfd mov      rdx, qword ptr [rcx + 0x10]
0000000141467c01 xor      r9d, r9d
0000000141467c04 mov      rbx, rcx
0000000141467c07 mov      qword ptr [rsp + 0x440], r9
0000000141467c0f mov      rcx, qword ptr [rcx + 0x18]
0000000141467c13 mov      rax, rdx
0000000141467c16 sub      rax, rcx
0000000141467c19 sar      rax, 4
0000000141467c1d cmp      eax, 1
0000000141467c20 jne      0x141467d91
0000000141467c26 cmp      rcx, rdx
0000000141467c29 lea      rdi, [rip + 0x11b37b0]
0000000141467c30 mov      rax, rdi
0000000141467c33 cmovb    rax, rcx
0000000141467c37 mov      r8d, dword ptr [rax + 8]
0000000141467c3b cmp      r8d, 7
0000000141467c3f je       0x141467cb7
0000000141467c41 cmp      r8d, 2
0000000141467c45 je       0x141467cb7
0000000141467c47 cmp      rcx, rdx
0000000141467c4a jae      0x141467c77
0000000141467c4c cmp      rcx, rdi
0000000141467c4f je       0x141467c57
0000000141467c51 cmp      dword ptr [rcx + 8], r9d
0000000141467c55 je       0x141467cb7
0000000141467c57 cmp      rcx, rdx
0000000141467c5a jae      0x141467c77
0000000141467c5c cmp      rcx, rdi
0000000141467c5f je       0x141467c77
0000000141467c61 movsxd   rax, dword ptr [rcx + 8]
0000000141467c65 cmp      eax, -1
0000000141467c68 je       0x141467c77
0000000141467c6a lea      rcx, [rip + 0x11b382f]
0000000141467c71 mov      rcx, qword ptr [rcx + rax*8]
0000000141467c75 jmp      0x141467c7e
0000000141467c77 lea      rcx, [rip + 0x1380a9a]
0000000141467c7e mov      qword ptr [rsp + 0x28], rcx
0000000141467c83 lea      rax, [rip + 0x1399516]
0000000141467c8a lea      rcx, [rsp + 0x30]
0000000141467c8f mov      qword ptr [rsp + 0x20], rax
0000000141467c94 mov      r9d, 1
0000000141467c9a lea      r8, [rip + 0x139a23f]
0000000141467ca1 lea      rdx, [rip + 0x13812a8]
0000000141467ca8 call     0x1404f65f0
0000000141467cad lea      rdx, [rsp + 0x30]
0000000141467cb2 jmp      0x141467d98
0000000141467cb7 mov      dword ptr [rsp + 0x20], r9d
0000000141467cbc lea      r8, [rsp + 0x440]
0000000141467cc4 mov      r9, qword ptr [rip + 0x1be2c15]
0000000141467ccb mov      edx, 1
0000000141467cd0 mov      rcx, rbx
0000000141467cd3 call     0x1413a37e0
0000000141467cd8 test     eax, eax
0000000141467cda jns      0x141467d56
0000000141467cdc mov      rax, qword ptr [rbx + 0x18]
0000000141467ce0 cmp      rax, qword ptr [rbx + 0x10]
0000000141467ce4 jae      0x141467d04
0000000141467ce6 cmp      rax, rdi
0000000141467ce9 je       0x141467d04
0000000141467ceb movsxd   rcx, dword ptr [rax + 8]
0000000141467cef cmp      ecx, -1
0000000141467cf2 je       0x141467d04
0000000141467cf4 mov      rax, rcx
0000000141467cf7 lea      rcx, [rip + 0x11b37a2]
0000000141467cfe mov      rcx, qword ptr [rcx + rax*8]
0000000141467d02 jmp      0x141467d0b
0000000141467d04 lea      rcx, [rip + 0x1380a0d]
0000000141467d0b mov      rax, qword ptr [rip + 0x1be2bce]
0000000141467d12 test     rax, rax
0000000141467d15 je       0x141467d20
0000000141467d17 mov      rax, qword ptr [rax + 8]
0000000141467d1b test     rax, rax
0000000141467d1e jne      0x141467d27
0000000141467d20 lea      rax, [rip + 0x13812e9]
0000000141467d27 mov      qword ptr [rsp + 0x28], rcx
0000000141467d2c lea      r8, [rip + 0x1399d75]
0000000141467d33 lea      rcx, [rsp + 0x30]
0000000141467d38 mov      qword ptr [rsp + 0x20], rax
0000000141467d3d mov      r9d, 1
0000000141467d43 lea      rdx, [rip + 0x1381206]
0000000141467d4a call     0x1404f65f0
0000000141467d4f lea      rdx, [rsp + 0x30]
0000000141467d54 jmp      0x141467d98
0000000141467d56 mov      rcx, qword ptr [rbx + 0x10]
0000000141467d5a mov      rax, qword ptr [rsp + 0x440]
0000000141467d62 movd     xmm0, dword ptr [rax + 0x54]
0000000141467d67 mov      eax, 1
0000000141467d6c cvtdq2pd xmm0, xmm0
0000000141467d70 mov      dword ptr [rcx + 8], 3
0000000141467d77 movsd    qword ptr [rcx], xmm0
0000000141467d7b add      qword ptr [rbx + 0x10], 0x10
0000000141467d80 mov      rbx, qword ptr [rsp + 0x448]
0000000141467d88 add      rsp, 0x430
0000000141467d8f pop      rdi
0000000141467d90 ret
0000000141467d91 lea      rdx, [rip + 0x12328ec]
0000000141467d98 mov      rcx, rbx
0000000141467d9b call     0x14139b420
0000000141467da0 mov      rcx, rbx
0000000141467da3 call     0x1418deb50
0000000141467da8 mov      rbx, qword ptr [rsp + 0x448]
0000000141467db0 xor      eax, eax
0000000141467db2 add      rsp, 0x430
0000000141467db9 pop      rdi
0000000141467dba ret
