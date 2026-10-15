0000000141465f10 mov      qword ptr [rsp + 0x10], rbx
0000000141465f15 push     rdi
0000000141465f16 sub      rsp, 0x430
0000000141465f1d mov      rdx, qword ptr [rcx + 0x10]
0000000141465f21 xor      r9d, r9d
0000000141465f24 mov      rbx, rcx
0000000141465f27 mov      qword ptr [rsp + 0x440], r9
0000000141465f2f mov      rcx, qword ptr [rcx + 0x18]
0000000141465f33 mov      rax, rdx
0000000141465f36 sub      rax, rcx
0000000141465f39 sar      rax, 4
0000000141465f3d cmp      eax, 1
0000000141465f40 jne      0x1414660b3
0000000141465f46 cmp      rcx, rdx
0000000141465f49 lea      rdi, [rip + 0x11b5490]
0000000141465f50 mov      rax, rdi
0000000141465f53 cmovb    rax, rcx
0000000141465f57 mov      r8d, dword ptr [rax + 8]
0000000141465f5b cmp      r8d, 7
0000000141465f5f je       0x141465fd7
0000000141465f61 cmp      r8d, 2
0000000141465f65 je       0x141465fd7
0000000141465f67 cmp      rcx, rdx
0000000141465f6a jae      0x141465f97
0000000141465f6c cmp      rcx, rdi
0000000141465f6f je       0x141465f77
0000000141465f71 cmp      dword ptr [rcx + 8], r9d
0000000141465f75 je       0x141465fd7
0000000141465f77 cmp      rcx, rdx
0000000141465f7a jae      0x141465f97
0000000141465f7c cmp      rcx, rdi
0000000141465f7f je       0x141465f97
0000000141465f81 movsxd   rax, dword ptr [rcx + 8]
0000000141465f85 cmp      eax, -1
0000000141465f88 je       0x141465f97
0000000141465f8a lea      rcx, [rip + 0x11b550f]
0000000141465f91 mov      rcx, qword ptr [rcx + rax*8]
0000000141465f95 jmp      0x141465f9e
0000000141465f97 lea      rcx, [rip + 0x138277a]
0000000141465f9e mov      qword ptr [rsp + 0x28], rcx
0000000141465fa3 lea      rax, [rip + 0x139b1f6]
0000000141465faa lea      rcx, [rsp + 0x30]
0000000141465faf mov      qword ptr [rsp + 0x20], rax
0000000141465fb4 mov      r9d, 1
0000000141465fba lea      r8, [rip + 0x139b71f]
0000000141465fc1 lea      rdx, [rip + 0x1382f88]
0000000141465fc8 call     0x1404f65f0
0000000141465fcd lea      rdx, [rsp + 0x30]
0000000141465fd2 jmp      0x1414660ba
0000000141465fd7 mov      dword ptr [rsp + 0x20], r9d
0000000141465fdc lea      r8, [rsp + 0x440]
0000000141465fe4 mov      r9, qword ptr [rip + 0x1be48f5]
0000000141465feb mov      edx, 1
0000000141465ff0 mov      rcx, rbx
0000000141465ff3 call     0x1413a37e0
0000000141465ff8 test     eax, eax
0000000141465ffa jns      0x141466076
0000000141465ffc mov      rax, qword ptr [rbx + 0x18]
0000000141466000 cmp      rax, qword ptr [rbx + 0x10]
0000000141466004 jae      0x141466024
0000000141466006 cmp      rax, rdi
0000000141466009 je       0x141466024
000000014146600b movsxd   rcx, dword ptr [rax + 8]
000000014146600f cmp      ecx, -1
0000000141466012 je       0x141466024
0000000141466014 mov      rax, rcx
0000000141466017 lea      rcx, [rip + 0x11b5482]
000000014146601e mov      rcx, qword ptr [rcx + rax*8]
0000000141466022 jmp      0x14146602b
0000000141466024 lea      rcx, [rip + 0x13826ed]
000000014146602b mov      rax, qword ptr [rip + 0x1be48ae]
0000000141466032 test     rax, rax
0000000141466035 je       0x141466040
0000000141466037 mov      rax, qword ptr [rax + 8]
000000014146603b test     rax, rax
000000014146603e jne      0x141466047
0000000141466040 lea      rax, [rip + 0x1382fc9]
0000000141466047 mov      qword ptr [rsp + 0x28], rcx
000000014146604c lea      r8, [rip + 0x139b57d]
0000000141466053 lea      rcx, [rsp + 0x30]
0000000141466058 mov      qword ptr [rsp + 0x20], rax
000000014146605d mov      r9d, 1
0000000141466063 lea      rdx, [rip + 0x1382ee6]
000000014146606a call     0x1404f65f0
000000014146606f lea      rdx, [rsp + 0x30]
0000000141466074 jmp      0x1414660ba
0000000141466076 mov      rdx, qword ptr [rbx + 0x10]
000000014146607a xorps    xmm0, xmm0
000000014146607d mov      rax, qword ptr [rsp + 0x440]
0000000141466085 mov      ecx, dword ptr [rax + 0x47]
0000000141466088 mov      eax, 1
000000014146608d mov      dword ptr [rdx + 8], 3
0000000141466094 cvtsi2sd xmm0, rcx
0000000141466099 movsd    qword ptr [rdx], xmm0
000000014146609d add      qword ptr [rbx + 0x10], 0x10
00000001414660a2 mov      rbx, qword ptr [rsp + 0x448]
00000001414660aa add      rsp, 0x430
00000001414660b1 pop      rdi
00000001414660b2 ret
00000001414660b3 lea      rdx, [rip + 0x12345ca]
00000001414660ba mov      rcx, rbx
00000001414660bd call     0x14139b420
00000001414660c2 mov      rcx, rbx
00000001414660c5 call     0x1418deb50
00000001414660ca mov      rbx, qword ptr [rsp + 0x448]
00000001414660d2 xor      eax, eax
00000001414660d4 add      rsp, 0x430
00000001414660db pop      rdi
00000001414660dc ret
