# Итог сеанса восстановления2022 — 12–13 октября

Поручение:9 часов,20:55UTC12.10→05:55UTC13.10. Корневой Europa_Client.exe2022 x64 0.2.989.0, SHA2562dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18; зимняя карта16010. Нативные проверки подGE-Proton11-7, оригиналы не менялись. Не встроенный сервер: наш реконструированный peer.

| ID | Результат | Где читать |
|---|---|---|
|LOOK01|Owned wardrobe8 категорий доступен через Appearance→Accessories→Character→Customize; автопервый экран отдельно|LOOK01-COLD-WARDROBE-20261012.md|
|LOOK02|Rainbow сохранён, cold native модель/slot/drop/repick; Default контроль|LOOK02-WEAPON-SKINS-20261012.md|
|LOOK03|Saki cold login→Training; сохранённый Walkie влобби, unequip/relogin; charm вматче отдельно|LOOK03-CHARACTER-ACCESSORIES-20261013.md|
|LOOK04|Все8 категорий одежды equip/replace/remove, cold+второйTraining|LOOK04-CLOTHING-20261013.md|
|LOOK05|Alice/Bob/Alice: отдельные durable cosmetics иUID; не сохранение всей боевой сессии|LOOK05-PROFILES-20261013.md|
|OPS03|Настоящий portableLinux peer / отдельный Proton namespace: движение/fire/reload, второйTraining; cycle доRescued1;hardTCP20s|LAN-SSH-20261013.md; OPS03-CYCLE-HARDCUT-20261013.md|
|HOST02|Опциональный DebugConsole helper, фиксированные публичные числовые HUD getters, безопасная уборка своихфайлов; gate0negative|DEBUG-SNAPSHOTS-20261013.md|

518 тестов source/479 переносимого комплекта прошли после удаления неудачного кандидата. verify-onlyOK; .NET8Release/PowerShellparser проверены в этом сеансе. Собственные клиенты/контроллеры остановлены; выбранные оригинальные/runtimeEXE/DLL hashes совпали.

Найдена ошибка NET06: hardTCP разрыв во времяreload — сервер2/5, nativegetter1/5; кандидатpoll-before-snapshot далnative0/5, отклонён и не включён в рабочийкод. РучнойRвозвращает2/5бездополнительногорасхода. Следующий опыт — decoder4A0 140C37130, применениеITEM_DATA иprediction counter приhandoff; getter послекаждогоэтапа. Нельзя считать серверныйтест подтверждением native.

Windows/SSH/LAN этой новой связки ещё не проверены. В notebook SSHdaemon отсутствует; Linuxpeer иsshd должны жить в одном networknamespace. Не объявлятьOPS03done. HOST01/03/04 без нового исполняемого provider/SDK остаются блокированными; наличиеимён вLuaне доказывает host.

Для текущего одиночногоWindows: gitpull вrun_roe_2022, `.\run-roe-2022.cmd -Profile alice -Mode cycle -DebugConsole`; игра G:\REsearch\Ring of Elysium-2022. Существующая независимаяruntime-копия используется повторно. Новые внешность/профили/helper на реальномWindows требуют проверки. РаздельныйLinuxзапуск — поLAN-SSHдокументу; однойWindowsкоманды недостаточно безподготовленногоLinuxpeer/SSH.

План:docs/recovery/mechanics-2022.csv. Этапы77.5%минимальнаязимняя сессия/70.1%целевойплан — это вес критериевтаблицы, не готовностьвсейигры. Следующий приоритет NET06; пользовательскаяприёмка OPS02/OPS03 отдельно.
