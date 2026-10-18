# NET06: текущая Citori, pending R и реальная потеря UDP

Native016,18.10.2026, корневой2022 x64 0.2.989.0,
SHA256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`,
Iceland16010, независимый runtime/Proton/loopback. EXE/DLL не менялись.

После genuine M4 kill и corpse pickup12ga6 игрок обычной ходьбой подошёл к
исходной вторичной Citori15705/позиция366091,544149,259077. Настоящий drag
вslot1 заменил Glock; M4slot2 и AKslot3 сохранились. Ёмкость и ITEM_DATA —
актуальные, после исправления16.10. Контрольные показания — собственные числовые
native HUD getters; это не только peer log и не распознавание PNG.

| Шаг | Сервер | Native getters |
|---|---|---|
|До выстрела|Citori2/6|slot1=2,reserve_citori=6|
|Fire/R, начало cut|clip1,pendingR,reserve6|не снимались внутри окна|
|Authenticated idle handoff|clip1,reserve6,pendingR|состояние перенесено|
|Завершение R|clip2,reserve5|**2/5**|
|Следующий fire/R|clip2,reserve4|**2/4**|

Fault proxy действительно выполнил C2Sdrop_window20с; handoff записан после
21.405с idle. Время записи следующего пакета не означает изменение настроенного
20-секундного окна. WorldState сохранилHP1000 и stage_index6 (внутренний индекс,
не код стадии); M4остался29/30, AK0/60, бинты5 и планер1.

Этот контроль **не воспроизвёл** старое расхождение server2/5→HUD1/5.
Он не объясняет его причину и не заменяет точный совместный контроль374:
в374 были дверь7767/state2, диагностический перенос в другой квартал и старый
weapon-snowboard со старой starter policy. Новых задержек4A0 или повторных5FB
ради этого результата не добавляли. Windows Citori/полная связка дверей отдельно.

Первичные `research/builds/2022/recovery/011-net06/20261018T1646-citori-current/`:
`native016-citori-{before,after,final,result}.json`, `driver.log`.
Native source run: `host-console-20261007/recovery-gun06-terrain-20261018-016`;
UI-файлы016-citori* и fault proxy events. Оригинальные исходные результаты
helper также сохранены в0914-capacity-resume, не перезаписывались.

Далее: точный совместный повтор374 на явно зафиксированном современном
Citori fixture и двери, плюс Windows. Оценки этапов NET06 не повышены.
