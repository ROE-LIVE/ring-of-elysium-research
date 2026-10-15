Исследовательские пути ниже относительны к полному `ROE_SERVER`. Выбранные числовые доказательства находятся в `snapshots/windows-starter-20261015/`; оригинальных клиентов/ключей/сырых AUTH в этом снимке нет.

# Windows c6ada6: слоты, стартовый набор и выбор клетки

Клиент2022 x64 0.2.989.0; корневой EXE SHA256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`. Первичные данные: `logs/20261014T225741-c6ada6/{launch-summary.json,weapon-snowboard.json,scene/events.jsonl}`. Ключи и сырые авторизационные пакеты не читались.

Windows-запуск материализовал `weapon_slots=2`. Отказ seq5089 на ground→equipment: `request_byte=1,request_short=2,request_flag=0`; старый guard вернул `byte_zero/short_zero/flag_one`. В актуальном коде это штатный manual_gun; профиль уже имеет три слота. Следовательно, два заявленных дефекта воспроизводятся **в старом комплекте запуска**, а не опровергают native377/378. Точный commit старого запуска неизвестен: журнал не содержит source hashes. Новый launch-summary сохраняет revision и SHA launcher/weapon peer/winter selection/manifest; endpoint ready пишет действительный slot count и starter flag.

Положительное Windows-наблюдение пользователя: стрельба/перезарядка, drop/pickup Citori с сохранением одного патрона, карта и двери. Журнал содержит12fire/6reload, discard70002→pickup70002. Отдельный автомат дверей не проверен: `winter_doors_enabled=false`, входящих6F57 нет, есть пять door_snapshot. Для контрольного повтора требуется `-WinterDoors`.

Выбор клетки:11принятых и12отказов `identity_or_cell`; после третьего выбора12отказов за3.18с, следующий принятый в22:58:51.543. Санитизированный журнал не содержит полей отклонённых11DF, поэтому конкретная причина задержки неизвестна. Новый peer пишет kind/UID-match/cell/flag при отказе. Native001–004:114принятых запросов (28+32+27+27), ни одного отказа; быстрые разные клетки принимаются≈каждые0.25с. Это не воспроизвело Windows-задержку. В map_reject_probe `xdotool mousemove --sync` на неизменной позиции сам ждал≈15с; этот инструментальный эффект не считать клиентским cooldown.

## Восстановленный состав стартового набора

Первичный `full-extraction-20261010/extracted/DATA/TABLE/INITITEM.XML:217–268`, map16010/stage1:

| Выбор | Способность | Оружие | Патроны | Бинты |
|---|---|---|---|---|
|1|планер200907|Glock17/20002|9мм30003×15|70001×5|
|2|сноуборд200906|Desert Eagle/20003|.50/30006×10|70001×5|
|3|кирки200904|Citori10402|12ga30004×10|70001×5|

Исходные capacity/reload Glock17: `EQUIPMENTTABLE/EQUIPMENTTABLEEUROPA.XML:922`, capacity17, empty2030ms/nonempty1600ms; M4/Citori имеют `RIGHT_WEAPON;LEFT_WEAPON;SUB_WEAPON` на строках268/744. Определения и количество source items восстановлены; начальный магазин/номера слотов исходный InitItem не задаёт. Наш peer оставляет явную политику полного магазина и первого слота. Исходные бронирование/баллистика этим не установлены.

`winter_starter_inventory=true` выбирает состав последнего принятого комплекта перед первой5FB. По InitItem на старте нет жилета/шлема; их можно подобрать с земли. Legacy research fixtures без этого флага сохраняют Citori/диагностическое снаряжение. Исправлен startup4A0: старое clip2 из сценария теперь заменяется текущим магазином только собственного starter gun; чужие UID не затрагиваются.

Native001 дал Glock/15/пять бинтов/планер, но старый scenario4A0 перезаписал HUD в2; слишком ранние действия fire не достигли peer. Этот отрицательный контроль сохранён. После исправления native002 подтвердил Glock17/15→fire16/15→R17/14, cap150; native003 — DE7/10→6/10→7/9, cap225; native004 — Citori2/10→1/10→2/9, cap300. PNG инвентаря подтверждают определения/количество/пустые armor slots. Native004 также настоящими drag принял Citori15700 вslot2 и M415705 вslot3 без замены исходной Citori; PNG `three-drag-third.png` показывает три оружия. Дополнительная M4/5.56 рядом — диагностически перемещённые fixture, не новый исходный loot RNG.

Данные: `windows-evidence.json`, `windows-public-events.json`, `native-checks.json`, выбранные `recovery-kit01-starter-selection-20261014-001..004-public-events.json`; реальные запуски и PNG под `host-console-20261007/recovery-kit01-starter-selection-20261014-001..004`. Все четыре завершены штатным таймаутом, selected original/runtime EXE/две DLL SHA до/после совпали. Следующий контроль: новый Windows-run с source hashes, три слота/manual drag/все комплекты; numeric rejected11DF при повторе задержки. Этапы KIT01=90, INV06=82.5 пока не повышены.
