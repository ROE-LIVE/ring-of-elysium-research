0000000141466b70 mov      qword ptr [rsp + 0x10], rbx
0000000141466b75 push     rdi
0000000141466b76 sub      rsp, 0x430
0000000141466b7d mov      rbx, rcx
0000000141466b80 xor      r9d, r9d
0000000141466b83 mov      rcx, qword ptr [rcx + 0x10]
0000000141466b87 mov      rax, rcx
0000000141466b8a mov      qword ptr [rsp + 0x440], r9
0000000141466b92 mov      rdx, qword ptr [rbx + 0x18]
0000000141466b96 sub      rax, rdx
0000000141466b99 sar      rax, 4
0000000141466b9d cmp      eax, 1
0000000141466ba0 jne      0x141466d08
0000000141466ba6 cmp      rdx, rcx
0000000141466ba9 lea      rdi, [rip + 0x11b4830]
0000000141466bb0 mov      rax, rdi
0000000141466bb3 cmovb    rax, rdx
0000000141466bb7 mov      r8d, dword ptr [rax + 8]
0000000141466bbb cmp      r8d, 7
0000000141466bbf je       0x141466c37
0000000141466bc1 cmp      r8d, 2
0000000141466bc5 je       0x141466c37
0000000141466bc7 cmp      rdx, rcx
0000000141466bca jae      0x141466bf7
0000000141466bcc cmp      rdx, rdi
0000000141466bcf je       0x141466bd7
0000000141466bd1 cmp      dword ptr [rdx + 8], r9d
0000000141466bd5 je       0x141466c37
0000000141466bd7 cmp      rdx, rcx
0000000141466bda jae      0x141466bf7
0000000141466bdc cmp      rdx, rdi
0000000141466bdf je       0x141466bf7
0000000141466be1 movsxd   rax, dword ptr [rdx + 8]
0000000141466be5 cmp      eax, -1
0000000141466be8 je       0x141466bf7
0000000141466bea lea      rcx, [rip + 0x11b48af]
0000000141466bf1 mov      rcx, qword ptr [rcx + rax*8]
0000000141466bf5 jmp      0x141466bfe
0000000141466bf7 lea      rcx, [rip + 0x1381b1a]
0000000141466bfe mov      qword ptr [rsp + 0x28], rcx
0000000141466c03 lea      rax, [rip + 0x139a596]
0000000141466c0a lea      rcx, [rsp + 0x30]
0000000141466c0f mov      qword ptr [rsp + 0x20], rax
0000000141466c14 mov      r9d, 1
0000000141466c1a lea      r8, [rip + 0x139b1ff]
0000000141466c21 lea      rdx, [rip + 0x1382328]
0000000141466c28 call     0x1404f65f0
0000000141466c2d lea      rdx, [rsp + 0x30]
0000000141466c32 jmp      0x141466d0f
0000000141466c37 mov      dword ptr [rsp + 0x20], r9d
0000000141466c3c lea      r8, [rsp + 0x440]
0000000141466c44 mov      r9, qword ptr [rip + 0x1be3c95]
0000000141466c4b mov      edx, 1
0000000141466c50 mov      rcx, rbx
0000000141466c53 call     0x1413a37e0
0000000141466c58 test     eax, eax
0000000141466c5a jns      0x141466cd6
0000000141466c5c mov      rax, qword ptr [rbx + 0x18]
0000000141466c60 cmp      rax, qword ptr [rbx + 0x10]
0000000141466c64 jae      0x141466c84
0000000141466c66 cmp      rax, rdi
0000000141466c69 je       0x141466c84
0000000141466c6b movsxd   rcx, dword ptr [rax + 8]
0000000141466c6f cmp      ecx, -1
0000000141466c72 je       0x141466c84
0000000141466c74 mov      rax, rcx
0000000141466c77 lea      rcx, [rip + 0x11b4822]
0000000141466c7e mov      rcx, qword ptr [rcx + rax*8]
0000000141466c82 jmp      0x141466c8b
0000000141466c84 lea      rcx, [rip + 0x1381a8d]
0000000141466c8b mov      rax, qword ptr [rip + 0x1be3c4e]
0000000141466c92 test     rax, rax
0000000141466c95 je       0x141466ca0
0000000141466c97 mov      rax, qword ptr [rax + 8]
0000000141466c9b test     rax, rax
0000000141466c9e jne      0x141466ca7
0000000141466ca0 lea      rax, [rip + 0x1382369]
0000000141466ca7 mov      qword ptr [rsp + 0x28], rcx
0000000141466cac lea      r8, [rip + 0x139b055]
0000000141466cb3 lea      rcx, [rsp + 0x30]
0000000141466cb8 mov      qword ptr [rsp + 0x20], rax
0000000141466cbd mov      r9d, 1
0000000141466cc3 lea      rdx, [rip + 0x1382286]
0000000141466cca call     0x1404f65f0
0000000141466ccf lea      rdx, [rsp + 0x30]
0000000141466cd4 jmp      0x141466d0f
0000000141466cd6 mov      rax, qword ptr [rsp + 0x440]
0000000141466cde lea      rdx, [rip + 0x1381cc7]
0000000141466ce5 mov      rcx, rbx
0000000141466ce8 movsx    r8d, byte ptr [rax + 0x4d]
0000000141466ced call     0x14139b420
0000000141466cf2 mov      eax, 1
0000000141466cf7 mov      rbx, qword ptr [rsp + 0x448]
0000000141466cff add      rsp, 0x430
0000000141466d06 pop      rdi
0000000141466d07 ret
0000000141466d08 lea      rdx, [rip + 0x1233975]
0000000141466d0f mov      rcx, rbx
0000000141466d12 call     0x14139b420
0000000141466d17 mov      rcx, rbx
0000000141466d1a call     0x1418deb50
0000000141466d1f mov      rbx, qword ptr [rsp + 0x448]
0000000141466d27 xor      eax, eax
0000000141466d29 add      rsp, 0x430
0000000141466d30 pop      rdi
0000000141466d31 ret
