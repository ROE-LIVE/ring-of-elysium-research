0000000140f17360 mov      rax, rsp
0000000140f17363 mov      byte ptr [rax + 0x20], r9b
0000000140f17367 push     rbp
0000000140f17368 push     rsi
0000000140f17369 push     rdi
0000000140f1736a push     r12
0000000140f1736c push     r13
0000000140f1736e push     r14
0000000140f17370 push     r15
0000000140f17372 mov      rbp, rsp
0000000140f17375 sub      rsp, 0x80
0000000140f1737c mov      qword ptr [rbp - 0x50], 0xfffffffffffffffe
0000000140f17384 mov      qword ptr [rax + 0x18], rbx
0000000140f17388 movaps   xmmword ptr [rax - 0x48], xmm6
0000000140f1738c movaps   xmmword ptr [rax - 0x58], xmm7
0000000140f17390 mov      r13d, r8d
0000000140f17393 mov      rdi, rdx
0000000140f17396 mov      r15, rcx
0000000140f17399 mov      rbx, qword ptr [rcx]
0000000140f1739c mov      rcx, rbx
0000000140f1739f call     0x140d8fd40
0000000140f173a4 mov      rcx, rax
0000000140f173a7 xor      r14d, r14d
0000000140f173aa test     rax, rax
0000000140f173ad jne      0x140f173c7
0000000140f173af mov      rcx, qword ptr [rbx + 0x130]
0000000140f173b6 call     0x140fb3b40
0000000140f173bb test     rax, rax
0000000140f173be lea      rcx, [rax + 0x58]
0000000140f173c2 jne      0x140f173c7
0000000140f173c4 mov      ecx, r14d
0000000140f173c7 mov      rax, qword ptr [rcx]
0000000140f173ca call     qword ptr [rax + 0xb8]
0000000140f173d0 mov      edx, eax
0000000140f173d2 mov      ecx, dword ptr [rdi + 0x40]
0000000140f173d5 call     0x140f684d0
0000000140f173da mov      rsi, rax
0000000140f173dd test     rax, rax
0000000140f173e0 je       0x140f176f8
0000000140f173e6 call     0x140f69f70
0000000140f173eb mov      rbx, rax
0000000140f173ee test     rax, rax
0000000140f173f1 je       0x140f176f8
0000000140f173f7 mov      rdx, rdi
0000000140f173fa mov      rcx, qword ptr [r15]
0000000140f173fd call     0x14130fef0
0000000140f17402 mov      r12d, r14d
0000000140f17405 test     al, al
0000000140f17407 setne    r12b
0000000140f1740b mov      rdx, qword ptr [rbx]
0000000140f1740e mov      rcx, rbx
0000000140f17411 call     qword ptr [rdx + 0x1a8]
0000000140f17417 movss    xmm2, dword ptr [rdi]
0000000140f1741b subss    xmm2, dword ptr [rax]
0000000140f1741f movss    xmm0, dword ptr [rdi + 4]
0000000140f17424 subss    xmm0, dword ptr [rax + 4]
0000000140f17429 movss    xmm1, dword ptr [rdi + 8]
0000000140f1742e subss    xmm1, dword ptr [rax + 8]
0000000140f17433 mulss    xmm0, xmm0
0000000140f17437 mulss    xmm2, xmm2
0000000140f1743b addss    xmm0, xmm2
0000000140f1743f mulss    xmm1, xmm1
0000000140f17443 addss    xmm0, xmm1
0000000140f17447 call     0x141aa88cc
0000000140f1744c movaps   xmm7, xmm0
0000000140f1744f call     0x141087640
0000000140f17454 mov      rdx, rax
0000000140f17457 mov      qword ptr [rbp + 0x48], rax
0000000140f1745b mov      rbx, qword ptr [rsi + 8]
0000000140f1745f test     rbx, rbx
0000000140f17462 jne      0x140f17471
0000000140f17464 mov      rcx, qword ptr [rip + 0x213dcf5]
0000000140f1746b mov      qword ptr [rbp + 0x40], rcx
0000000140f1746f jmp      0x140f17497
0000000140f17471 cmp      byte ptr [rbx], r14b
0000000140f17474 jne      0x140f1747f
0000000140f17476 mov      rax, qword ptr [rip + 0x213dceb]
0000000140f1747d jmp      0x140f17493
0000000140f1747f call     0x1404982c0
0000000140f17484 mov      rdx, rbx
0000000140f17487 mov      rcx, rax
0000000140f1748a call     0x1404984f0
0000000140f1748f mov      rdx, qword ptr [rbp + 0x48]
0000000140f17493 mov      qword ptr [rbp + 0x40], rax
0000000140f17497 lea      r8, [rdi + 0xc]
0000000140f1749b lea      rcx, [rdx + 0x27c]
0000000140f174a2 movaps   xmm1, xmm7
0000000140f174a5 call     0x1410875d0
0000000140f174aa mulss    xmm0, dword ptr [rsi + 0x28]
0000000140f174af mov      dword ptr [rsp + 0x20], r12d
0000000140f174b4 movaps   xmm3, xmm0
0000000140f174b7 mov      rdx, rdi
0000000140f174ba lea      rcx, [rbp + 0x40]
0000000140f174be call     0x1409c0b30
0000000140f174c3 mov      ecx, dword ptr [rip + 0x217e3f7]
0000000140f174c9 movzx    eax, cl
0000000140f174cc lea      r9, [rip + 0x217d8bd]
0000000140f174d3 mov      edx, dword ptr [r9 + rax*4]
0000000140f174d7 shr      ecx, 8
0000000140f174da movzx    eax, cl
0000000140f174dd mov      eax, dword ptr [r9 + rax*4 + 0x400]
0000000140f174e5 lea      ecx, [rdx + 0x16af]
0000000140f174eb add      ecx, eax
0000000140f174ed mov      eax, 0xa0a0a0a1
0000000140f174f2 mul      ecx
0000000140f174f4 shr      edx, 6
0000000140f174f7 imul     eax, edx, 0x66
0000000140f174fa sub      ecx, eax
0000000140f174fc mov      edx, ecx
0000000140f174fe movzx    ecx, word ptr [rip + 0x217e3bf]
0000000140f17505 mov      r9, qword ptr [r9 + rdx*8 + 0x800]
0000000140f1750d xor      r9, rcx
0000000140f17510 movzx    ecx, byte ptr [r9 + 0x1690]
0000000140f17518 mov      r8d, dword ptr [r9 + rcx*4 + 0xb60]
0000000140f17520 mov      ecx, dword ptr [r9 + 0x1690]
0000000140f17527 shr      ecx, 8
0000000140f1752a movzx    ecx, cl
0000000140f1752d mov      edx, dword ptr [r9 + rcx*4 + 0xf60]
0000000140f17535 lea      ecx, [r8 + 0xd8]
0000000140f1753c add      ecx, edx
0000000140f1753e mov      eax, 0xa0a0a0a1
0000000140f17543 mul      ecx
0000000140f17545 shr      edx, 6
0000000140f17548 imul     eax, edx, 0x66
0000000140f1754b sub      ecx, eax
0000000140f1754d mov      eax, ecx
0000000140f1754f movzx    ecx, word ptr [r9 + 0x1694]
0000000140f17557 mov      r8, qword ptr [r9 + rax*8 + 0x1360]
0000000140f1755f xor      r8, rcx
0000000140f17562 mov      r9, qword ptr [rdi + 0x28]
0000000140f17566 mov      r10d, dword ptr [r8 + 0x48]
0000000140f1756a xor      edx, edx
0000000140f1756c mov      eax, r9d
0000000140f1756f div      r10d
0000000140f17572 mov      r11, qword ptr [r8 + 0x40]
0000000140f17576 mov      rcx, qword ptr [r11 + rdx*8]
0000000140f1757a test     rcx, rcx
0000000140f1757d je       0x140f1758e
0000000140f1757f nop
0000000140f17580 cmp      r9, qword ptr [rcx]
0000000140f17583 je       0x140f17592
0000000140f17585 mov      rcx, qword ptr [rcx + 0x18]
0000000140f17589 test     rcx, rcx
0000000140f1758c jne      0x140f17580
0000000140f1758e mov      rcx, qword ptr [r11 + r10*8]
0000000140f17592 mov      rax, r10
0000000140f17595 cmp      rcx, qword ptr [r11 + r10*8]
0000000140f17599 je       0x140f175de
0000000140f1759b mov      rbx, qword ptr [rcx + 8]
0000000140f1759f test     rbx, rbx
0000000140f175a2 je       0x140f175e1
0000000140f175a4 mov      rax, qword ptr [rbx]
0000000140f175a7 mov      rcx, rbx
0000000140f175aa call     qword ptr [rax + 8]
0000000140f175ad test     rax, rax
0000000140f175b0 je       0x140f175e1
0000000140f175b2 mov      rax, qword ptr [rbx]
0000000140f175b5 mov      rcx, rbx
0000000140f175b8 call     qword ptr [rax + 8]
0000000140f175bb test     rax, rax
0000000140f175be je       0x140f175e1
0000000140f175c0 lea      rcx, [rip + 0x21a4df9]
0000000140f175c7 cmp      rax, rcx
0000000140f175ca je       0x140f175da
0000000140f175cc mov      rax, qword ptr [rax + 0x180]
0000000140f175d3 test     rax, rax
0000000140f175d6 jne      0x140f175c7
0000000140f175d8 jmp      0x140f175e1
0000000140f175da mov      al, 1
0000000140f175dc jmp      0x140f175e3
0000000140f175de mov      rbx, r14
0000000140f175e1 xor      al, al
0000000140f175e3 test     al, al
0000000140f175e5 cmovne   r14, rbx
0000000140f175e9 mov      rcx, qword ptr [rbp + 0x48]
0000000140f175ed add      rcx, 0x288
0000000140f175f4 movaps   xmm1, xmm7
0000000140f175f7 call     0x1410875d0
0000000140f175fc movaps   xmm6, xmm0
0000000140f175ff test     r14, r14
0000000140f17602 je       0x140f17635
0000000140f17604 mov      rcx, qword ptr [rdi + 0x28]
0000000140f17608 call     0x140f68a40
0000000140f1760d test     al, al
0000000140f1760f je       0x140f17635
0000000140f17611 test     r13d, r13d
0000000140f17614 js       0x140f17635
0000000140f17616 movss    dword ptr [rsp + 0x28], xmm6
0000000140f1761c mov      dword ptr [rsp + 0x20], r13d
0000000140f17621 mov      r9, rsi
0000000140f17624 mov      r8, r14
0000000140f17627 mov      rdx, rdi
0000000140f1762a call     0x140f17850
0000000140f1762f lea      r14, [rdi + 0xc]
0000000140f17633 jmp      0x140f17689
0000000140f17635 mov      rbx, qword ptr [rsi + 0x30]
0000000140f17639 test     rbx, rbx
0000000140f1763c jne      0x140f17647
0000000140f1763e mov      rax, qword ptr [rip + 0x213db1b]
0000000140f17645 jmp      0x140f17665
0000000140f17647 cmp      byte ptr [rbx], 0
0000000140f1764a jne      0x140f17655
0000000140f1764c mov      rax, qword ptr [rip + 0x213db15]
0000000140f17653 jmp      0x140f17665
0000000140f17655 call     0x1404982c0
0000000140f1765a mov      rdx, rbx
0000000140f1765d mov      rcx, rax
0000000140f17660 call     0x1404984f0
0000000140f17665 mov      qword ptr [rbp + 0x40], rax
0000000140f17669 mulss    xmm6, dword ptr [rsi + 0x50]
0000000140f1766e mov      dword ptr [rsp + 0x20], r12d
0000000140f17673 movaps   xmm3, xmm6
0000000140f17676 lea      r14, [rdi + 0xc]
0000000140f1767a mov      r8, r14
0000000140f1767d mov      rdx, rdi
0000000140f17680 lea      rcx, [rbp + 0x40]
0000000140f17684 call     0x1409c0b30
0000000140f17689 mov      rcx, rdi
0000000140f1768c call     0x140f68740
0000000140f17691 test     al, al
0000000140f17693 je       0x140f176f8
0000000140f17695 mov      rbx, qword ptr [rsi + 0x58]
0000000140f17699 test     rbx, rbx
0000000140f1769c jne      0x140f176a7
0000000140f1769e mov      rax, qword ptr [rip + 0x213dabb]
0000000140f176a5 jmp      0x140f176c5
0000000140f176a7 cmp      byte ptr [rbx], 0
0000000140f176aa jne      0x140f176b5
0000000140f176ac mov      rax, qword ptr [rip + 0x213dab5]
0000000140f176b3 jmp      0x140f176c5
0000000140f176b5 call     0x1404982c0
0000000140f176ba mov      rdx, rbx
0000000140f176bd mov      rcx, rax
0000000140f176c0 call     0x1404984f0
0000000140f176c5 mov      qword ptr [rbp + 0x40], rax
0000000140f176c9 mov      rcx, qword ptr [rbp + 0x48]
0000000140f176cd add      rcx, 0x294
0000000140f176d4 movaps   xmm1, xmm7
0000000140f176d7 call     0x1410875d0
0000000140f176dc mulss    xmm0, dword ptr [rsi + 0x78]
0000000140f176e1 mov      dword ptr [rsp + 0x20], r12d
0000000140f176e6 movaps   xmm3, xmm0
0000000140f176e9 mov      r8, r14
0000000140f176ec mov      rdx, rdi
0000000140f176ef lea      rcx, [rbp + 0x40]
0000000140f176f3 call     0x1409c0b30
0000000140f176f8 cmp      byte ptr [rbp + 0x58], 0
0000000140f176fc jne      0x140f1781f
0000000140f17702 mov      eax, dword ptr [rdi + 0x20]
0000000140f17705 mov      dword ptr [rbp + 0x40], eax
0000000140f17708 mov      eax, dword ptr [rdi + 0x40]
0000000140f1770b mov      dword ptr [rbp + 0x58], eax
0000000140f1770e mov      rax, qword ptr [r15]
0000000140f17711 mov      rcx, qword ptr [rip + 0x2112250]
0000000140f17718 mov      r8d, 4
0000000140f1771e test     byte ptr [rax + 0x68], 1
0000000140f17722 je       0x140f1779d
0000000140f17724 mov      r14d, 0xe
0000000140f1772a lea      edx, [r14 + 1]
0000000140f1772e mov      rax, qword ptr [rcx]
0000000140f17731 mov      ebx, edx
0000000140f17733 call     qword ptr [rax + 8]
0000000140f17736 mov      rsi, rax
0000000140f17739 mov      qword ptr [rbp - 0x48], rax
0000000140f1773d add      rbx, rax
0000000140f17740 mov      qword ptr [rbp - 0x38], rbx
0000000140f17744 mov      r8d, r14d
0000000140f17747 lea      rdx, [rip + 0x18622b2]
0000000140f1774e mov      rcx, rax
0000000140f17751 call     0x141aa8776
0000000140f17756 lea      rax, [rsi + 0xe]
0000000140f1775a mov      qword ptr [rbp - 0x40], rax
0000000140f1775e mov      byte ptr [rax], 0
0000000140f17761 mov      r9, rdi
0000000140f17764 lea      r8, [rbp + 0x58]
0000000140f17768 lea      rdx, [rbp + 0x40]
0000000140f1776c lea      rcx, [rbp - 0x48]
0000000140f17770 call     0x140f2c970
0000000140f17775 nop
0000000140f17776 sub      rbx, rsi
0000000140f17779 cmp      rbx, 1
0000000140f1777d jle      0x140f17798
0000000140f1777f test     rsi, rsi
0000000140f17782 je       0x140f17798
0000000140f17784 mov      rcx, qword ptr [rip + 0x21121dd]
0000000140f1778b mov      rax, qword ptr [rcx]
0000000140f1778e xor      r8d, r8d
0000000140f17791 mov      rdx, rsi
0000000140f17794 call     qword ptr [rax + 0x18]
0000000140f17797 nop
0000000140f17798 jmp      0x140f1781f
0000000140f1779d mov      rax, qword ptr [rax + 0x28]
0000000140f177a1 mov      qword ptr [rbp + 0x48], rax
0000000140f177a5 mov      r14d, 0x11
0000000140f177ab lea      edx, [r14 + 1]
0000000140f177af mov      rax, qword ptr [rcx]
0000000140f177b2 mov      ebx, edx
0000000140f177b4 call     qword ptr [rax + 8]
0000000140f177b7 mov      rsi, rax
0000000140f177ba mov      qword ptr [rbp - 0x48], rax
0000000140f177be add      rbx, rax
0000000140f177c1 mov      qword ptr [rbp - 0x38], rbx
0000000140f177c5 mov      r8d, r14d
0000000140f177c8 lea      rdx, [rip + 0x1862299]
0000000140f177cf mov      rcx, rax
0000000140f177d2 call     0x141aa8776
0000000140f177d7 lea      rax, [rsi + 0x11]
0000000140f177db mov      qword ptr [rbp - 0x40], rax
0000000140f177df mov      byte ptr [rax], 0
0000000140f177e2 mov      qword ptr [rsp + 0x20], rdi
0000000140f177e7 lea      r9, [rbp + 0x58]
0000000140f177eb lea      r8, [rbp + 0x40]
0000000140f177ef lea      rdx, [rbp + 0x48]
0000000140f177f3 lea      rcx, [rbp - 0x48]
0000000140f177f7 call     0x140f2cba0
0000000140f177fc nop
0000000140f177fd sub      rbx, rsi
0000000140f17800 cmp      rbx, 1
0000000140f17804 jle      0x140f1781f
0000000140f17806 test     rsi, rsi
0000000140f17809 je       0x140f1781f
0000000140f1780b mov      rcx, qword ptr [rip + 0x2112156]
0000000140f17812 mov      rax, qword ptr [rcx]
0000000140f17815 xor      r8d, r8d
0000000140f17818 mov      rdx, rsi
0000000140f1781b call     qword ptr [rax + 0x18]
0000000140f1781e nop
0000000140f1781f mov      rbx, qword ptr [rsp + 0xd0]
0000000140f17827 movaps   xmm6, xmmword ptr [rsp + 0x70]
0000000140f1782c movaps   xmm7, xmmword ptr [rsp + 0x60]
0000000140f17831 add      rsp, 0x80
0000000140f17838 pop      r15
0000000140f1783a pop      r14
0000000140f1783c pop      r13
0000000140f1783e pop      r12
0000000140f17840 pop      rdi
0000000140f17841 pop      rsi
0000000140f17842 pop      rbp
0000000140f17843 ret
