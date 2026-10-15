# NET04: совместные UDP потери, перестановки и дубли

09.10.2026, 2022x64 0.2.989.0, map16010, SHA256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`. Cold87, независимый Proton runtime, свои localhost peer/lobby/bridge в netnamespace. [Evidence](../snapshots/recovery-20261009-udp-combined/evidence.json), [tc/действия/UTC](../snapshots/recovery-20261009-udp-combined/netem-trial-evidence.json), [выбранные события](../snapshots/recovery-20261009-udp-combined/cold87-selected-events.json).

Opt-in reliable sender/receiver/FrameStream, idlehandoff и исправленияZONE02. Два90с профиля: delay100±20ms/reorder25% correlation50%/duplicate10%, затем дополнительноloss2%. Flower фильтруетUDP src/dst18001; TCP lobby не затрагивается. Первыйпрофиль:966пакетов вnetem,0dropped/57requeues; кконцувторого1948пакетов/20dropped/123requeues. Счётчикиtc накопительные. Послеfinally qdisc noqueue.

Приняты5genuine firecounter1..5 и5timed reload, каждыйamount1. Citori2/6→2/5→2/4→2/3→2/2→2/1, native230-final.png показывает2/1.664принятых application2a; конечныеMOVE ужепослеснятиянагрузки. Последнийfire/reload тожеaftercleanup. Повторныхeffect/duplicate_fire нет; триudp_retry по81байту, каждыйattempt1, приходятсянаloss-профиль. World_start1, stage10 околоworld+90.481, lateelapsed0.481; nativeконечныйтаймер0:42 соответствуетown deadlineworld+270. Handoff0, frame/parse/decrypt/receive/stream/delivery errors0.

Обе180с нагрузки пережиты безпересозданиямира и безAUTH/reconnect. Это ограниченныйположительныйтест нашей реализации; неисполняемыйoriginalhost и неполныйRUDP. Нетcongestioncontrol/remoteadvertisedwindow/FIN/expiry/Windows. Профиливероятностные; seed вtcstats, невыводитьгарантиюдлялюбыхпотерь.

Собственныйrunner остановлен послеhelpers, exit143. ТриEXE/DLL до/после совпали с оригиналами и имеют независимыеinode. Кодnative/клиентскиефайлы не менялись. NET04baseline60%, безповышенияэтапов. СледующийNET05: applicationserial32 fire/hand, затемLOOT05 lost821/82b.
