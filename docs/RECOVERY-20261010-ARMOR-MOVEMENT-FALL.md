# Состояние2022 после сессии10.10: броня, движение, падение

2022 x64 0.2.989.0, EXE SHA256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`, base140000000, winter16010. V99/Steam2018 не менялись. Архитектура прежняя: независимый клиент → локальное.NET lobby/TCP bridge → Python TGCP/UDP peer; Proton — стенд проверки, Windows — отдельный комплект. Native host не найден. Все новые опыты в isolated loopback namespace, без Docker/Ghidra/дополнительных моделей; git/network только чтение.

## Рабочие изменения

HP03/HP04: opt-in учебная body-only защита собственного жилета и расход прочности. Правило `absorbed=min(durable,raw_damage*percent//100)`; процент0..100, default0. Helmet/head/original nDEF отдельно, zone/fall не расходуют броню. Ответ3E82 меняет только equipment; нет5FB и сброса hand/ammo. Native write equipment+3C:140FB2047, constructor140FD1EF9. Cold125: vest1→0/HP525→476, следующая атака476→426; выброс/повторный подбор сохраняют0. HP03/HP04 partial diagnostic77.5, не done.

MOVE03: optional server-time token path budget. MOVE2A decoder140C56410, len27+28*N/N≤20; проверка всего пути перед world/weapon/loot mutation. Поправка27 на последнюю принятую позицию не даёт свежий burst; server27/restore явно задаёт anchor. Default disabled; normalXY5000/Z20000cm/s/burst2. Cold126 normal220accepted, W3смещение823.935см, snowboardFSM25. Cold127 strictXY100/burst0.2 намеренно блокирует обычную ходьбу:39reject/39correction/nativeXY0;20сS2C loss/handoff иповтор39/39/XY0. Awaitinganchor587 — загрузка, не нарушение скорости. Flight/vehicles/history/terrain/LOS/Windows открыты. Partial diagnostic77.5.

## Что выяснено без реализации исходного правила

GUN07: schema140596AB0 nDamage1DC/min1E0/head204. Bullet constructor140FC1BC5: Citori260/M4A1400 → config0.1 → bullet1BC26/40. Consumer140FC3F20 относится к penetration context; min/head watch при genuine hit не прочитаны. Не объявлять26/40 исходным authoritative HP damage. External blocked12.5: нужен sanitized original hurt/equipment trace либо executable authoritative provider; ключи не нужны.

MOVE05: пятьTableBin members сверены с original SFC SHA. UnitAttr gravity980/maxfall10000; MoveCfg fall_gravity1600; CharacterTable landing400/650/1100, fall700/1400. Cold128/129 подтверждают jump/window и контролируемые high falls, native5→6→0. Hardware14124520C выявил отдельный порог **−1200**, flag0→1 иevent7C, sampled velocity−5003.58, acceleration≈1600.32. Landing enter141246D30/update141247020: local events, прямого HP calculation не установлено. HP1000 на нашем peer не доказывает отсутствие original fall damage. Произвольный урон кандидату не добавлен. External blocked0: нужен original authoritative fall trace с режимом/высотой/скоростью/набором/HP до-после/hurt response или provider.

LOOT10: текущая **ready №49**. Native2022106E decoder140C2F6F0 (2UID/2NUL-strings≤128/3words), handler140D6EF90→140FE2800→EVENT_SHOW_REPORT_BUTTON142796E78. Во внешнем справочнике SHA EXE не указан; no-handler автоматически не переносить. Item list в этом сообщении нет, создание контейнера не доказано. Следующий опыт: remoteactor public interact component/UID/model до-после533, аппаратные точкиD69550/14122F490, genuine open. После binding — atomic transfer UID/quantity/durable/repeat/handoff. Общий аирдроп не доказательство corpse. При отсутствии binding нужен sanitized original corpse create→interact→open→pick trace.

## Запуск Windows и проверка

Windows run_roe_2022 HEAD `3f2338a7f80dbb22f5139c2cd4d3d39592a3f2d1` отправлен в upstream; functional commit68d04a6, последующий commit убирает только лишнюю строку EOF теста. После pull:

```powershell
.\run-roe-2022.cmd -Mode cycle -Bots -OwnArmorAbsorbPercent 50 -ReliableUDP -IdleHandoff
```

Для отдельной проверки позиции добавить `-ValidateMovement`. Не совмещать Bots иTarget; для broken0/1 можно добавить `-LootCatalog config\loot-broken-armor.json`. Проверять wear/HP, выкинуть/подобрать vest0, hand/ammo, обычный ход и сноуборд, краткий обрыв; glider/vehicle с новым флагом ещё не подтверждены. Новые флаги не считать nativeWindows-проверенными по Proton. Существующая runtime копия переиспользуется.

275source/207portable unittest OK; verify-only/.NET8 build OK,0warnings/errors. SOURCE-MANIFEST36совпадает с источником. Cold122..130 завершены, триoriginal/runtimeSHAequal/independent inode. Последние GUI/hardware tests не доказывают полный матч, исходный AI/host/мультиплеер/баллистику.

Пересчитанный CSV: core71.2%, весь целевой план47.4% — **этапы плана**, не доля восстановленной оригинальной игры. Актуальные ссылки/ограничения: [CSV](recovery/mechanics-2022.csv), [поручение](recovery/AGENT-START.md). Первичные отчёты и ограниченные фрагменты: [снимок](../snapshots/recovery-20261010-armor-movement-fall/README.md), MANIFEST содержит источник/SHA. Полного клиента, ресурсов, AUTH и ключей в снимке нет; изменённые modules не составляют самостоятельный полный дистрибутив.

[Карточка следующего опыта LOOT10](../snapshots/recovery-20261010-armor-movement-fall/task/handoff-next.md): preflight выполнен в source workspace. Карточка не запускает игру и не означает, что snapshot содержит клиент/все fixtures.
