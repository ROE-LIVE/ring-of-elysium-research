0000000141465ae0 mov      qword ptr [rsp + 0x10], rbx
0000000141465ae5 push     rdi
0000000141465ae6 sub      rsp, 0x430
0000000141465aed mov      rdx, qword ptr [rcx + 0x10]
0000000141465af1 xor      r9d, r9d
0000000141465af4 mov      rbx, rcx
0000000141465af7 mov      qword ptr [rsp + 0x440], r9
0000000141465aff mov      rcx, qword ptr [rcx + 0x18]
0000000141465b03 mov      rax, rdx
0000000141465b06 sub      rax, rcx
0000000141465b09 sar      rax, 4
0000000141465b0d cmp      eax, 1
0000000141465b10 jne      0x141465c81
0000000141465b16 cmp      rcx, rdx
0000000141465b19 lea      rdi, [rip + 0x11b58c0]
0000000141465b20 mov      rax, rdi
0000000141465b23 cmovb    rax, rcx
0000000141465b27 mov      r8d, dword ptr [rax + 8]
0000000141465b2b cmp      r8d, 7
0000000141465b2f je       0x141465ba7
0000000141465b31 cmp      r8d, 2
0000000141465b35 je       0x141465ba7
0000000141465b37 cmp      rcx, rdx
0000000141465b3a jae      0x141465b67
0000000141465b3c cmp      rcx, rdi
0000000141465b3f je       0x141465b47
0000000141465b41 cmp      dword ptr [rcx + 8], r9d
0000000141465b45 je       0x141465ba7
0000000141465b47 cmp      rcx, rdx
0000000141465b4a jae      0x141465b67
0000000141465b4c cmp      rcx, rdi
0000000141465b4f je       0x141465b67
0000000141465b51 movsxd   rax, dword ptr [rcx + 8]
0000000141465b55 cmp      eax, -1
0000000141465b58 je       0x141465b67
0000000141465b5a lea      rcx, [rip + 0x11b593f]
0000000141465b61 mov      rcx, qword ptr [rcx + rax*8]
0000000141465b65 jmp      0x141465b6e
0000000141465b67 lea      rcx, [rip + 0x1382baa]
0000000141465b6e mov      qword ptr [rsp + 0x28], rcx
0000000141465b73 lea      rax, [rip + 0x139b626]
0000000141465b7a lea      rcx, [rsp + 0x30]
0000000141465b7f mov      qword ptr [rsp + 0x20], rax
0000000141465b84 mov      r9d, 1
0000000141465b8a lea      r8, [rip + 0x139b917]
0000000141465b91 lea      rdx, [rip + 0x13833b8]
0000000141465b98 call     0x1404f65f0
0000000141465b9d lea      rdx, [rsp + 0x30]
0000000141465ba2 jmp      0x141465c88
0000000141465ba7 mov      dword ptr [rsp + 0x20], r9d
0000000141465bac lea      r8, [rsp + 0x440]
0000000141465bb4 mov      r9, qword ptr [rip + 0x1be4d25]
0000000141465bbb mov      edx, 1
0000000141465bc0 mov      rcx, rbx
0000000141465bc3 call     0x1413a37e0
0000000141465bc8 test     eax, eax
0000000141465bca jns      0x141465c46
0000000141465bcc mov      rax, qword ptr [rbx + 0x18]
0000000141465bd0 cmp      rax, qword ptr [rbx + 0x10]
0000000141465bd4 jae      0x141465bf4
0000000141465bd6 cmp      rax, rdi
0000000141465bd9 je       0x141465bf4
0000000141465bdb movsxd   rcx, dword ptr [rax + 8]
0000000141465bdf cmp      ecx, -1
0000000141465be2 je       0x141465bf4
0000000141465be4 mov      rax, rcx
0000000141465be7 lea      rcx, [rip + 0x11b58b2]
0000000141465bee mov      rcx, qword ptr [rcx + rax*8]
0000000141465bf2 jmp      0x141465bfb
0000000141465bf4 lea      rcx, [rip + 0x1382b1d]
0000000141465bfb mov      rax, qword ptr [rip + 0x1be4cde]
0000000141465c02 test     rax, rax
0000000141465c05 je       0x141465c10
0000000141465c07 mov      rax, qword ptr [rax + 8]
0000000141465c0b test     rax, rax
0000000141465c0e jne      0x141465c17
0000000141465c10 lea      rax, [rip + 0x13833f9]
0000000141465c17 mov      qword ptr [rsp + 0x28], rcx
0000000141465c1c lea      r8, [rip + 0x139ba35]
0000000141465c23 lea      rcx, [rsp + 0x30]
0000000141465c28 mov      qword ptr [rsp + 0x20], rax
0000000141465c2d mov      r9d, 1
0000000141465c33 lea      rdx, [rip + 0x1383316]
0000000141465c3a call     0x1404f65f0
0000000141465c3f lea      rdx, [rsp + 0x30]
0000000141465c44 jmp      0x141465c88
0000000141465c46 mov      rcx, qword ptr [rbx + 0x10]
0000000141465c4a mov      rax, qword ptr [rsp + 0x440]
0000000141465c52 movd     xmm0, dword ptr [rax + 0x43]
0000000141465c57 mov      eax, 1
0000000141465c5c cvtdq2pd xmm0, xmm0
0000000141465c60 mov      dword ptr [rcx + 8], 3
0000000141465c67 movsd    qword ptr [rcx], xmm0
0000000141465c6b add      qword ptr [rbx + 0x10], 0x10
0000000141465c70 mov      rbx, qword ptr [rsp + 0x448]
0000000141465c78 add      rsp, 0x430
0000000141465c7f pop      rdi
0000000141465c80 ret
0000000141465c81 lea      rdx, [rip + 0x12349fc]
0000000141465c88 mov      rcx, rbx
0000000141465c8b call     0x14139b420
0000000141465c90 mov      rcx, rbx
0000000141465c93 call     0x1418deb50
0000000141465c98 mov      rbx, qword ptr [rsp + 0x448]
0000000141465ca0 xor      eax, eax
0000000141465ca2 add      rsp, 0x430
0000000141465ca9 pop      rdi
0000000141465caa ret
