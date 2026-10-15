000000014132a1f0 mov      qword ptr [rsp + 0x10], rsi
000000014132a1f5 mov      qword ptr [rsp + 0x18], rdi
000000014132a1fa push     rbp
000000014132a1fb push     r14
000000014132a1fd push     r15
000000014132a1ff lea      rbp, [rsp - 0x37]
000000014132a204 sub      rsp, 0x100
000000014132a20b cmp      byte ptr [rdx + 0x2e], 0
000000014132a20f mov      r15, r9
000000014132a212 mov      r14, r8
000000014132a215 mov      rsi, rcx
000000014132a218 je       0x14132a245
000000014132a21a cvttss2si eax, dword ptr [rdx + 0x30]
000000014132a21f mov      dword ptr [rcx + 0xc], eax
000000014132a222 cvttss2si eax, dword ptr [rdx + 0x34]
000000014132a227 mov      dword ptr [rcx + 0x10], eax
000000014132a22a cvttss2si eax, dword ptr [rdx + 0x38]
000000014132a22f mov      dword ptr [rcx + 0x14], eax
000000014132a232 mov      eax, dword ptr [rdx + 0x3c]
000000014132a235 mov      dword ptr [rcx + 0x19], eax
000000014132a238 mov      eax, dword ptr [rdx + 0x40]
000000014132a23b mov      dword ptr [rcx + 0x1d], eax
000000014132a23e movss    xmm0, dword ptr [rdx + 0x44]
000000014132a243 jmp      0x14132a26d
000000014132a245 cvttss2si eax, dword ptr [rdx]
000000014132a249 mov      dword ptr [rcx + 0xc], eax
000000014132a24c cvttss2si eax, dword ptr [rdx + 4]
000000014132a251 mov      dword ptr [rcx + 0x10], eax
000000014132a254 cvttss2si eax, dword ptr [rdx + 8]
000000014132a259 mov      dword ptr [rcx + 0x14], eax
000000014132a25c mov      eax, dword ptr [rdx + 0xc]
000000014132a25f mov      dword ptr [rcx + 0x19], eax
000000014132a262 mov      eax, dword ptr [rdx + 0x10]
000000014132a265 mov      dword ptr [rcx + 0x1d], eax
000000014132a268 movss    xmm0, dword ptr [rdx + 0x14]
000000014132a26d mov      qword ptr [rsp + 0x120], rbx
000000014132a275 movaps   xmmword ptr [rsp + 0xf0], xmm6
000000014132a27d movss    dword ptr [rcx + 0x21], xmm0
000000014132a282 mov      eax, dword ptr [rdx + 0x28]
000000014132a285 movss    xmm0, dword ptr [rbp + 0x7f]
000000014132a28a mulss    xmm0, dword ptr [rip + 0x15b9e3e]
000000014132a292 mov      dword ptr [rcx + 0x4e], eax
000000014132a295 movzx    eax, byte ptr [rdx + 0x2c]
000000014132a299 mov      byte ptr [rcx + 0x52], al
000000014132a29c cmp      byte ptr [rdx + 0x2d], 0
000000014132a2a0 sete     al
000000014132a2a3 xor      edi, edi
000000014132a2a5 mov      byte ptr [rcx + 0x53], al
000000014132a2a8 mov      eax, dword ptr [rdx + 0x18]
000000014132a2ab mov      dword ptr [rcx + 0x58], eax
000000014132a2ae mov      eax, dword ptr [rdx + 0x24]
000000014132a2b1 mov      dword ptr [rcx + 0x54], eax
000000014132a2b4 mov      eax, dword ptr [rdx + 0x20]
000000014132a2b7 lea      rdx, [rsp + 0x30]
000000014132a2bc mov      dword ptr [rcx + 0x60], eax
000000014132a2bf mov      rax, qword ptr [r8 + 0x28]
000000014132a2c3 mov      qword ptr [rcx + 4], rax
000000014132a2c7 movzx    eax, byte ptr [rbp + 0x77]
000000014132a2cb mov      byte ptr [rcx + 0x3e], al
000000014132a2ce cvttss2si eax, xmm0
000000014132a2d2 mov      qword ptr [rsp + 0x30], rdi
000000014132a2d7 mov      dword ptr [rsp + 0x38], edi
000000014132a2db mov      word ptr [rsp + 0x3c], di
000000014132a2e0 mov      byte ptr [rsp + 0x3e], dil
000000014132a2e5 mov      qword ptr [rsp + 0x40], rdi
000000014132a2ea mov      dword ptr [rsp + 0x48], edi
000000014132a2ee mov      dword ptr [rcx + 0x5c], eax
000000014132a2f1 mov      rcx, r14
000000014132a2f4 call     0x140d922b0
000000014132a2f9 cmp      byte ptr [rsp + 0x3e], dil
000000014132a2fe je       0x14132a47f
000000014132a304 cvttss2si eax, dword ptr [rsp + 0x40]
