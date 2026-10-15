000000014130e510 mov      qword ptr [rsp + 8], rbx
000000014130e515 push     rdi
000000014130e516 sub      rsp, 0x2e0
000000014130e51d movss    xmm0, dword ptr [rsp + 0x310]
000000014130e526 mov      rdi, rdx
000000014130e529 mov      eax, dword ptr [rip + 0x1dbc2ad]
000000014130e52f mov      rbx, rcx
000000014130e532 movss    dword ptr [rsp + 0x28], xmm0
000000014130e538 mov      byte ptr [rsp + 0x20], r9b
000000014130e53d mov      r9, r8
000000014130e540 mov      r8, rdx
000000014130e543 mov      dword ptr [rsp + 0x30], eax
000000014130e547 mov      rdx, rcx
000000014130e54a lea      rcx, [rsp + 0x30]
000000014130e54f call     0x14132a1f0
000000014130e554 mov      r9, qword ptr [rbx + 0x80]
000000014130e55b mov      eax, dword ptr [rbx + 0x1c]
000000014130e55e mov      rcx, r9
000000014130e561 mov      r8, qword ptr [rbx + 0x78]
000000014130e565 mov      dword ptr [rsp + 0x94], eax
000000014130e56c sub      rcx, r8
000000014130e56f movabs   rax, 0xd79435e50d79436
000000014130e579 imul     rcx
000000014130e57c mov      rax, rdx
000000014130e57f shr      rax, 0x3f
000000014130e583 add      rdx, rax
000000014130e586 mov      eax, 0x1e
000000014130e58b cmp      edx, eax
000000014130e58d cmovbe   ax, dx
000000014130e591 xor      ebx, ebx
000000014130e593 mov      word ptr [rsp + 0x98], ax
000000014130e59b mov      edx, ebx
000000014130e59d cmp      r8, r9
000000014130e5a0 je       0x14130e5dd
000000014130e5a2 cmp      edx, 0x1e
000000014130e5a5 ja       0x14130e5dd
000000014130e5a7 movups   xmm0, xmmword ptr [r8]
000000014130e5ab mov      eax, edx
000000014130e5ad inc      edx
000000014130e5af imul     rcx, rax, 0x13
000000014130e5b3 movzx    eax, word ptr [r8 + 0x10]
000000014130e5b8 movups   xmmword ptr [rsp + rcx + 0x9a], xmm0
000000014130e5c0 mov      word ptr [rsp + rcx + 0xaa], ax
000000014130e5c8 movzx    eax, byte ptr [r8 + 0x12]
000000014130e5cd add      r8, 0x13
000000014130e5d1 mov      byte ptr [rsp + rcx + 0xac], al
000000014130e5d8 cmp      r8, r9
000000014130e5db jne      0x14130e5a2
000000014130e5dd movss    xmm2, dword ptr [rsp + 0x62]
000000014130e5e3 xorps    xmm1, xmm1
000000014130e5e6 cvtsi2ss xmm1, dword ptr [rsp + 0x59]
000000014130e5ec movss    xmm3, dword ptr [rsp + 0x66]
000000014130e5f2 xorps    xmm0, xmm0
000000014130e5f5 cvtsi2ss xmm0, dword ptr [rsp + 0x55]
000000014130e5fb subss    xmm3, xmm1
000000014130e5ff movss    xmm1, dword ptr [rsp + 0x6a]
000000014130e605 subss    xmm2, xmm0
000000014130e609 xorps    xmm0, xmm0
000000014130e60c cvtsi2ss xmm0, dword ptr [rsp + 0x5d]
000000014130e612 mulss    xmm3, xmm3
000000014130e616 subss    xmm1, xmm0
000000014130e61a mulss    xmm2, xmm2
000000014130e61e addss    xmm3, xmm2
000000014130e622 mulss    xmm1, xmm1
000000014130e626 addss    xmm3, xmm1
000000014130e62a comiss   xmm3, dword ptr [rip + 0x15d5ccb]
000000014130e631 jbe      0x14130e649
000000014130e633 test     rdi, rdi
000000014130e636 je       0x14130e79d
000000014130e63c mov      rcx, rdi
000000014130e63f call     0x14130da00
000000014130e644 jmp      0x14130e79d
000000014130e649 xorps    xmm2, xmm2
000000014130e64c xorps    xmm1, xmm1
000000014130e64f cvtsi2ss xmm2, dword ptr [rsp + 0x40]
000000014130e655 cvtsi2ss xmm1, dword ptr [rsp + 0x3c]
000000014130e65b subss    xmm2, dword ptr [rsp + 0x4d]
000000014130e661 subss    xmm1, dword ptr [rsp + 0x49]
000000014130e667 xorps    xmm0, xmm0
000000014130e66a cvtsi2ss xmm0, dword ptr [rsp + 0x44]
000000014130e670 mulss    xmm2, xmm2
000000014130e674 subss    xmm0, dword ptr [rsp + 0x51]
000000014130e67a mulss    xmm1, xmm1
000000014130e67e addss    xmm2, xmm1
000000014130e682 mulss    xmm0, xmm0
000000014130e686 addss    xmm2, xmm0
000000014130e68a comiss   xmm2, dword ptr [rip + 0x15d5c97]
000000014130e691 jbe      0x14130e705
000000014130e693 mov      edx, dword ptr [rip + 0x1d87227]
000000014130e699 lea      r9, [rip + 0x1d866f0]
000000014130e6a0 mov      eax, edx
000000014130e6a2 shr      eax, 8
000000014130e6a5 movzx    ecx, al
000000014130e6a8 movzx    eax, dl
000000014130e6ab mov      ecx, dword ptr [r9 + rcx*4 + 0x400]
000000014130e6b3 mov      r8d, dword ptr [r9 + rax*4]
000000014130e6b7 mov      eax, 0xa0a0a0a1
000000014130e6bc add      r8d, 0x16af
000000014130e6c3 add      r8d, ecx
000000014130e6c6 mul      r8d
000000014130e6c9 shr      edx, 6
000000014130e6cc imul     eax, edx, 0x66
000000014130e6cf sub      r8d, eax
000000014130e6d2 movzx    eax, word ptr [rip + 0x1d871eb]
000000014130e6d9 mov      rcx, qword ptr [r9 + r8*8 + 0x800]
000000014130e6e1 xor      rcx, rax
000000014130e6e4 je       0x14130e79d
000000014130e6ea call     0x140cd5d00
000000014130e6ef test     rax, rax
000000014130e6f2 je       0x14130e79d
000000014130e6f8 mov      rcx, rax
000000014130e6fb call     0x14130da00
000000014130e700 jmp      0x14130e79d
000000014130e705 mov      rcx, qword ptr [rip + 0x1d3206c]
000000014130e70c lea      r8, [rsp + 0x30]
000000014130e711 add      rcx, 8
000000014130e715 mov      dword ptr [rsp + 0x20], 1
000000014130e71d mov      r9d, 0x2a4
000000014130e723 mov      edx, 0x11dd
000000014130e728 call     0x140baf300
000000014130e72d test     al, al
000000014130e72f jne      0x14130e79d
000000014130e731 mov      edx, dword ptr [rip + 0x1d87189]
000000014130e737 lea      r9, [rip + 0x1d86652]
000000014130e73e movzx    r10d, word ptr [rip + 0x1d8717e]
000000014130e746 mov      eax, edx
000000014130e748 shr      eax, 8
000000014130e74b movzx    ecx, al
000000014130e74e movzx    eax, dl
000000014130e751 mov      ecx, dword ptr [r9 + rcx*4 + 0x400]
000000014130e759 mov      r8d, dword ptr [r9 + rax*4]
000000014130e75d mov      eax, 0xa0a0a0a1
000000014130e762 add      r8d, 0x16af
000000014130e769 add      r8d, ecx
000000014130e76c mul      r8d
000000014130e76f shr      edx, 6
000000014130e772 imul     eax, edx, 0x66
000000014130e775 sub      r8d, eax
000000014130e778 mov      rcx, qword ptr [r9 + r8*8 + 0x800]
000000014130e780 cmp      rcx, r10
000000014130e783 je       0x14130e79d
000000014130e785 xor      rcx, r10
000000014130e788 cmp      qword ptr [rcx + 0x2df0], rbx
000000014130e78f je       0x14130e79d
000000014130e791 lea      rcx, [rip + 0x145cae8]
000000014130e798 call     0x14046ae60
000000014130e79d mov      eax, dword ptr [rip + 0x1dbc039]
000000014130e7a3 inc      eax
000000014130e7a5 movd     xmm0, eax
000000014130e7a9 cvtdq2pd xmm0, xmm0
000000014130e7ad comisd   xmm0, xmmword ptr [rip + 0x15d55db]
000000014130e7b5 cmova    eax, ebx
000000014130e7b8 mov      rbx, qword ptr [rsp + 0x2f0]
000000014130e7c0 mov      dword ptr [rip + 0x1dbc016], eax
000000014130e7c6 add      rsp, 0x2e0
000000014130e7cd pop      rdi
000000014130e7ce ret
