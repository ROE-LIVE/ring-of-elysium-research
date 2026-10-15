# Транспорт и вода2022: состояние11.10.2026

Рабочий EXE2022 x64 SHA2dca9b1e…6ba18, картаIceland16010. Переносимый комплект `run_roe_2022` commit f88d0de;301tests/verify/.NET8 Release0errors, source347tests. Адреса/пакеты V99/2018 сюда не переносить.

## Подтверждено и опубликовано

CAR01/CAR02 Proton190/191/193: исходные точки135009/type1001 и135004/type1005; Jeep102 на земле, F/W/F/W и FSM0→7→0. Точка1001 с identity quaternion упирается в ограду через7.4м, с диагностической интерпретацией Direction270 проезжает133.6м; точка1005 identity проезжает39м. Consumer Direction изXML, RNG, полная fleet, multiplayer authority и Windows повтор открыты. Серверный guard6543 отклоняет выход дальше10м от актуальной Jeep, не меняя занятое место;10м — наша граница.

Windows: `git pull --ff-only`, затем ` .\run-roe-2022.cmd -Mode cycle -OriginalJeeps -WeaponProfile m4`. Две машины дополнительные; исходный игрок не переносится. Полёт вертолёта из предыдущего опыта включается `-NativeEvacuation`; собственный20сек отлёт — `-DiagnosticDeparture`. Все три флага совместно проходятverify. Сначала проверить реальные машины/выход/трос/Stats на Windows, передать каталогruns сlaunch-summary иevents.

## Ограниченное подтверждение воды

MOVE06 Proton194/195: native swimming locomotion/FSM11, управление по двум направлениям около2.3м/с. Существующий C2S2a/body83 N2 несёт координаты воды; decoder140C56410. Отдельный swim opcode и имена неизвестных байтов не установлены.195 упёрся в каменный берег,196 с исходной суши дошёл только до мелководья/FSM0. Переход суша↔вода, Dive, воздух, drowning, лодка и Windows ещё не подтверждены. CSV baseline55 — этапы плана, не доля восстановленного сервера.

## Как исследовали

Независимый runtime, GE-Proton11-7/Xvfb, loopback namespace; обычные клавиши черезxdotool. Native XYZ известного vehicle UID читается position getter140B8F860, собственный FSM/позиция — адресным samplerKIT03. Нет изменения памяти/регистров для управления физикой и postspawn positionRPC. Игровыеcaptures сохраняются вROE_SERVER, сюда скопированы только selected public motion/позиции/UTC/ hashes, отчёты и код; ни ключей, ни auth, ни полных ресурсов/дампов. Timeout124 либо собственныйTERM143 — контролируемое завершение сhash-cleanup.

Начальные ошибки missing scene payload теперь отклоняются `run_trial.py` preflight до запуска клиента/сервисов. Следующая задачаKIT04/№83: проверить конкретную поверхностьClimbRock307 и raycast/native gate. Кирки enabled не означают рабочее лазание. После неё по очередиCAR03: исходные vehicle pools; не подменять ими произвольныйRNG.

Источники: выбранные отчёты/evidence в `../snapshots/recovery-vehicles-water-climb-20261011/`; актуальный план `recovery/mechanics-2022.csv`, исходник `ROE_SERVER/docs/recovery/mechanics-2022.csv`.

## KIT04: точная следующая проверка

PhysMaterialDesc307=ClimbRock; collision EU_rock_001 использует307/NotClimbable=false; instance27912 вIceland имеет548263.5625/483309.15625/253906.59375. MOVEABILITY5/6 требуетterrainCLIFF+abilityClimb. HUDABILITYPANELDATA81–108 привязываеткирки кINTERACT=F и getters `IsLookAtPlayerPickaxesAvailable/Active`. Новый отчёт083-kit04/20261011T0835-surface сselected primary/hash.

197 invalidZ провалился под землю,198 естественно приземлился/проверил верхний край (continuous297samples толькоFSM0),199 подошёл снизу, но упёрся в другую скалу28мдоцели. Лазание не доказано;47.5 сохранён. Нужны native registration/wrappers getters иreadonly hardware trace: bool, raycast hit material/NotClimbable, distance/normal, terrainCLIFF. Не подменять это включением ability, изменением порогов или очередным случайным spawn. Все197..199 собственные controlled cleanup143/124 иhashcheck прошли. Секреты/полныеcaptures/ресурсы здесь не хранятся.
