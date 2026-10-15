# INV03: выброс, дубликат и повторный подбор после обрыва

09.10.2026; клиент2022 x64 0.2.989.0, map16010. Независимыйruntime, GE-Proton11-7/Xvfb, собственныйpeer в loopback namespace. EXE SHA256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`. Выбранные EXE/DLL до/после совпадают; оригиналы не изменены.

## Первичная привязка

Настоящий drag выдаёт3e80/tag2: U8tag/U8container/BE16slot/BE16quantity/BE64opaque/U8own; decoder140c4b470→140c4b2f0→140c4ae00. Референсы5fb/3e82 и ITEM union сверены в INV02 `../../022-inv02/20261009T1721-item-union/inventory-wire-layout.md`. Прочность: wire ITEM+32→native item+9e→equipment+3c, decoder140bcec10, handlers140fd1ec0/140fb1f20; UI показывает значение/10. Серверная политика сохранения — weapon_probe_2022.py, не извлечённый оригинальныйсервер.

## Cold95: оружие

NativeM4 сmag40403: reload40/10→fire39/10, UID0x1e00000100000001. Обычныйdrop70002, genuine repick70002. Для второгоdrop proxy разделил C2S рамку89байт на17/72; UDPseq1136599055, второй1136599072 доставлен дважды до первого. Выбранные20байт заголовков и proxy timestamps сохранены в cold95-duplicate-segment-headers.json; encryptedpayload не читался. Application3e80 обработан одинраз: создан ровноодин M4index70004.

Во время нахожденияM4 на земле C2S потерян20с. НовыйAUTH/idlehandoff18:30:11UTC сохраняет world.started39037.835571463, world_start1. После native repick70004 и настоящегоfire финал M438/10, прежнийUID иmag40403; Citori2/6. PNG inv03-24-final-late показывает этотрезультат. Cold95 exit124 (истёклимит), cleanup/hashafter сохранены.

Отрицательные контроли: inv03-14 былошибочнымподбором старогошлема70001, анеM4; он не засчитан. Presetdurability370 былпроигнорирован старымLootFixture.load, UI показал150. Этотопыт не доказывает сохранение повреждённойброни.

## Cold96: исправление прочности

LootFixture.load теперь принимает целуюdurability0..maximum только для поддержаннойброни; bool/float/string/выходзаграницы/другаякатегория отвергаются. Безполя сохраняется прежняя максимальнаяпрочность. Семьcodec/loaderрегрессий,244main и170kit tests прошли.

Свежийcold96: nativepickup200102,index15703 показывает37; drag550,175→810,450 выдаёт настоящийdiscard и создаёт70002. Шлем остаётся на земле во времяC2S20с. AUTH/idlehandoff18:47:03UTC, world.started40584.054869321, HP700,world_start1. Повторный nativepickup70002 в18:48:05 сохраняет37; Citori2/6, M40/50,mag в сумке иvest200 также сохранены. ТриPNG до/наземле/после подтверждают UI, выбранныеevents подтверждаютдействия. Exit143, своипроцессы остановлены, выбранныеSHA неизменны.

## Границы и следующий пункт

Проверены ограниченныеknownitems, nativeProton и транспортныйдубликат; не веськаталог,неWindows и не исходныеarmor/hit formulas. INV03 остаётсяbaseline90%, не объявляетсяdone/100. Следующий №24/KIT01: смена трёхнаборов при непустоминвентаре, проверка ровнооднойability и правильнойcapacity.

Переданные evidence/code — snapshots/recovery-inv03-drop-20261009. Полные ownruns/PNG находятся в ROE_SERVER по путямreport; снимок не является готовымстендом.
