# Попадания и перенос модулей:2022,16.10.2026

Основной EXE — корневой `Europa_Client.exe`2022 x64, SHA256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`. Это внешний scene peer; исходный host/баланс не восстановлен. Проверки ниже выполнены на независимой копии под Proton, не на Windows.

## Ground→gun

Поддержан настоящий C2S `3B63`33B `>IIQBHB3iB` с container3, ненулевым targetGunUID, partIndexH и auto0. Старый guard требовал target0 и отвергал этот вариант. Теперь совместимость и конкретный экземпляр проверяются до изменения состояния, новый предмет устанавливается непосредственно в оружие. Ответ `82B` удаляет предмет с земли; без него раннийNative002 оставлял ground ghost.

Native004: коллиматор40305/point2, AR-магазин40403/point3 и глушитель40103/point0 установлены прямо на M4slot2. Послеreload40/20, выстрела39/20 и drop/repick вslot3 сохранены все три модуля,39/20 и gunUID. Это не доказательство любых обвесов/исходных эффектов. При замене прежний модуль возвращается в сумку; отказ при нехватке места атомарен. Политика замены — локальная, не доказанная оригинальная серверная.

Названия из `DATA/TABLE/EQUIPMENTTABLE/EQUIPMENTTABLEEUROPA.XML:965,983,986`:40305 — коллиматор,40103 — глушитель,40403 — магазин. Не переносить привычную нумерацию типов из других игр.

## Штатные отметки и звук

Прежний `11EA`, decoder140C41120→handler14130FD50, не подходит для hitmarker M4: проверяет type1430BB750=`EuRPG`, а M4 —1430A2C80=`QSRifle`. Имена подтверждены инициализаторами140179EC0/14015D5A0 и литералами1427DC1C8/142796D00. Native002 вышел именно на этой проверке.

Рабочий путь:

`11EB →140C413F0 decoder →14130FFA0 handler →14130DE60 →14117E080 →14117D170 →EventPlayerHitTarget →14138E970 →OnHitTarget + Wwise`.

`11EB`48B `>QQ3iBBIBB3I`: shooterUID,targetUID,relativeXYZ,POS-tail0,chPart_id,iDamage,bDead,bArticulo,iCli_logictick,iCli_offsetms,iWeapon_id. Offset относительно цели, сантиметры. Native decoder принял48B и отверг47B; SWIG getters141478060..14147A5D0 подтверждают имена. Пять выбранных48B первичного обмена подтверждают relativeXYZ/weaponID; это запись2023, поэтому совместимость отдельно проверена decoder2022.

| Контроль | Факт настоящего C2S/состояния | Штатный результат |
| --- | --- | --- |
| Native005 тело | part3,HP1000→900 | style0/headfalse, белые черточки,CDF864C1 |
| Native005 голова | part1,impactZ259234,HP900→800 | style0/headtrue, head-вариант,18856512 |
| Native005 промах | firecounter3,нет11DD/hit/11EB | отметки не возникли |
| Native006 броня | part3,HP100→50,armor100→50 | style1/headfalse,оранжевый,CDF864C1 |
| Native006 добивание | part3,HP50→0,armor50→0 | style2/headfalse,красный,CDF864C1 |

Штатный callback14138EAE6 вызывает `OnHitTarget(style,head)`,14138EB03 — Wwise. Хеши FNV1lower совпадают с `Play_HUD_hitmarker`/`Play_HUD_hitmarker_head` из `DATA/SOUNDS/WWISEAUDIO/SOUNDBANKSINFO.XML`. В GFX `DATA/UI/EUROPACROSSHAIRPANEL.SWF`,123090B,SHA256a3c14b77a2e92c506821e6ae5ed79cac17afdd8945e8df85424de49782689ae8, методOnHitTarget поfile+0x1D977 выбирает белые/оранжевые/красные clips и head-вариант. Методы разобраны статически, без исполнения игрового ActionScript. На записанных кадрах черточки видны; overlay не добавлялся. Системная запись/прослушивание аудиовыхода не выполнена: подтверждён вызов штатного звукового события.

**Part1 подтверждён для head feedback; исходный множитель урона не подтверждён.** Поле11DD+83 — shooter_path_use_c, не headshot. Учебные100raw/50%armor и LOS не становятся исходным балансом.11EB формируется только после принятого выстрела/hit; повтор не даёт нового урона или маркера. НекорректныеXYZ/part отвергаются до HP/armor/dedup. Shared combat передаёт feedback стрелку с его собственным UID; новый Windows/LAN-повтор отдельно.

Проверки:579source/551portable tests. Полное исследование, выбранные native logs и воспроизведение: `research/builds/2022/recovery/050-inv07/20261015T2337-ground-attachment/`. В компактном публичном исследовательском репозитории исходные ресурсы/полные прогоны не включены; выбранная обезличенная выборка находится в `evidence/hit-feedback-20261016/`.

Следующее: Windows W17, затем GUN07. Функция с прежнимreturnPC140D095D6 установлена как140D09590; она передаёт R8 без преобразования в1412F8F20. Источник R8+24 и исходная формула ещё требуют отдельного анализа.
