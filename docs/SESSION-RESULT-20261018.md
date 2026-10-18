# Продолжение плана — 18.10.2026

Основной2022 x64 0.2.989.0, **корневой EXE**, Iceland16010, SHA256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`. Начало09:14UTC, бюджет до14:14UTC. Независимый runtime/Proton и loopback namespace; оригинальные EXE/DLL не изменяются. Финальные проверки и передача перечислены ниже.

- [NET06/GUN03](NET06-CAPACITY-HANDOFF-20261018.md): три pendingR/C2S UDP20s в одном процессе с WorldState, M4/Glock/AK30/17/30 и следующийfire/R. Native prediction capacity30/17 у M4/Glock; HP1000/календарь сохранены. Раннийfire не отменяетpartialR, переключение руки отменяет без расхода. Citori374 остаётся открытым.
- [GUN05/LOOT10](PASSIVE-TARGETS-20261018.md): параметр `-PracticeTargets 1..10`, независимые UID/HP/броня/инвентари. Native002 два genuine M4kills/две разные сумки12ga6+6; сохранность HP600 после обрыва. Native005 десять admin deaths/две потери связи/обычная эвакуация/StatsKill0Rescued1. Исправлено копирование начальных вещей игрока в NPC. Это пассивная группа, не AI.
- [INV02](INVENTORY-BRANCH-CONTROL-20261018.md): первичные3E82handler140E162D0/nativeflag1/cache140F48330 и3B64callback140D629A0. Отрицательный flag0 prototype ухудшил состояние M4/AK, полностью отменён. Задержка3D изображений оружия не исправлена.
- [OPS04](LIVE-COMMAND-LIFETIME-20261018.md): optional `damage_npc --npc-uid`, ledger подтверждённыхID peractor до остановки peer. Для повторного действия нужен новыйID; инструмент генерирует его автоматически без --id. Модельный lifecycle прошёл, native повтор фиксируется отдельно.
- OPS01: отсутствовавший lz4 установлен pinned4.4.5; persistentrequirements/check добавлены в jupyterROE. Bash syntax/dry-run/check прошли; Docker-образ не собирался.

Новые проверки — [CSV W19](recovery/windows-tests-20261018-w19.csv), в launcher **WINDOWS-TESTS-W19.csv**. W17/W18 пользовательские результаты не переписывать. Training, клетку для фиксированного стенда не менять. M4/AK на земле; десять NPC двумя рядами впереди, часть закрывается Jeep/другими моделями.

```powershell
git pull --ff-only
.\run-roe-2022.cmd -Mode cycle -CycleScale 3 -Duration 1800 -ReliableUDP -IdleHandoff -Kit glider -Target armored -PracticeTargets 10 -LootCatalog ".\config\windows-smoke-20261015.json" -LiveControl
```

Public `play.cmd` уже задаёт Target/Mode/CycleScale/LootCatalog; достаточно `play.cmd -Client "G:\REsearch\Ring of Elysium-2022" -PracticeTargets 10 -LiveControl`. После игры `export-report.cmd`, передать reports/ID и заполненныйW19CSV. Основное: полнаяR, триоружия, два настоящих убийства/раздельныйлут, Stats, второйTraining. Windows новой ёмкости/группы ещё ожидается.

Этапы/проценты плана не повышаются: новые контроли укрепляют baseline, не закрывают исходные balance/RNG/AI/host/Windows. GUN07 требует совместимого первичного материала/адресногоtrace; Citori374 и Appearance cold-preview остаются открыты.

Дополнительный [Native007 BOT05](BOT-CONTROLLER-HANDOFF-20261018.md): послесамостоятельного подбора/выходаsafe и20сC2Sобрыва nativeNPC сохранил тотжеactor/оружие/HP/позицию; controller не началподборзаново. Deathbagпослеhandoff получилегоCitori2+6, безplayerstarter.

Native006: реальнаяэвакуация/Stats/ReturnLobby→повторныйTraining;10свежихNPC HP1000, старыйID не выполненснова, новыйIDработает послеещёодногообрыва. ОшибкаUI-helperслишкомчастаяF исправлена; итоговыйподъёмобычнымвводомуспешен.

[GUN06 Native009](M4-THROUGH-ROCK-20261018.md): первый подтверждённый M4 through24,04757см Rock305/count2; nativeHP700 и11EB. Meshточки совпали сnative≤0,04128см, расчётE40→8,63385. Это одинopt-inmesh, не исходнаяHPформула/всякарта.

Актуализация18.10: [Native010/011 decoder→handler цепочки](PICK-DECODE-CHAIN-20261018.md). Для3B64 bodydecoder140C69B00/handler140D629A0 и3E82 decoder140C4BA10/handler140E162D0 полученоhardwareподтверждение. Старое«decoderнеизвестен»выше относитсяк этапудоэтогоконтроля; UI-model задержка остаётсяоткрытой.

## Проверки и передача

Финальные наборы:637source,600run_roe_2022,611publiclauncher (финальный повтор с portable PowerShell — без пропусков),8research — успешно. Оба launcher verify-only принимают10targets/8smokeitems; .NET8 lobby Release собран без ошибок/предупреждений. Jupyter install --analysis --dry-run и bash syntax прошли; Docker-образ не собирался. Windows-физический запуск этой новой ревизии не выполнялся.

Все11Proton-прогонов остановлены:001/003/004/006/007/008/009/011 завершены намиTERM143,002/005/010 — ограничениемtimeout124.008 — неверныйfixturestartup, не отрицательныйпрострел. До/после во всех11совпадают выбранные EXE/ProtocalHandler_x64.dll/Tenproxy64.dll, runtime независим. Свояигра неосталасьзапущенной. Сводка: `research/builds/2022/recovery/037-gun05/20261018T0920-target-roster/final-cleanup.json`. Это проверка3файлов, не fullhashвсехресурсов.

Действующий план115строк/версия3; изменены доказательства/следующие шаги11ID, этапы и проценты без повышения. Реестр102сигнала обновлён по14строкам; native_decoder_va для3B64/3E82 теперь заполнены подтверждёнными адресами. Всеbaseline/external_blocked: --next не выдаётready; следующий контроль — WindowsW19, затемINV02 UI-model notification иGUN06mixed materials по явномуID. Исходныйhost/AI/HP/RNG не объявленывосстановленными.

Дополнительный контроль PowerShell: в PATH команда отсутствовала, но найден ранее установленный `ROE_SERVER/tools/powershell-7.6.6-linux/pwsh`. С `ROE_TEST_PWSH` весь публичный набор611 пройден без пропусков; reset-проверки используют временные фиктивные каталоги и mock firewall, настоящий Windows firewall не менялся. AST всех7PowerShell-скриптов private/public разобран без ошибок; реальные ValidateRange/parameter binding принимают PracticeTargets10 и отклоняют0/11. Это не запуск игры на Windows. Первичные `release-tests-public-pwsh.log`, `release-powershell-parse.log`, `parse-launchers.ps1` в каталоге037-gun05/20261018T0920-target-roster.
