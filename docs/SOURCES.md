**Актуально08.10, ночь:** [два слота, timed reload и пассивная мишень](RECOVERY-20261008-NIGHT.md). Следующий №22/INV02 — pages/consumables; две пушки уже работают. Новый Windows-повтор и dual-gun reconnect остаются открытыми. Учебная защита50% не является исходной формулой ROE.

Актуализация10.10: [own armor/MOVE03/native fall/death info](RECOVERY-20261010-ARMOR-MOVEMENT-FALL.md); текущая ready №49/LOOT10, оригинальные hurt/fall rules ждут named input. Источники и границы в этой странице и docs/recovery; старые поручения ниже не выбирать как текущую очередь.

# Источники и переносимость

[Индекс отчётов](../catalog/reports.json) содержит источник, копию, SHA-256 исходника/копии и число скрытых значений. Это индекс происхождения, а не новая проверка каждого вывода. Исторические и отрицательные результаты сохранены; текущая сводка — в docs. Копирование старого отчёта о Ghidra или модели не означает запуск этих инструментов при подготовке контекста.

Пути ROE_SERVER/... относятся к /home/jovyan/imported/REsearch; пути roe-server/... — к /home/jovyan/roe-server. При переносе заменить эти корни. Копии самодостаточны для чтения, но первичные JSON/ASM/PNG/resources остаются в исходном workspace. Локальные ссылки в snapshots представлены путями с явной меткой, чтобы не имитировать наличие доказательств в Git.

## Основные первичные каталоги

Все следующие пути относятся к ROE_SERVER:

| Тема | Каталог | Основные материалы |
| --- | --- | --- |
| Winter2022 | research/builds/2022/iceland-gameplay-20261006 | report/README, run_winter_demo.py, run_trial.py, run.sh, scene/actor/weapon/parcel/world JSON |
| Лут/таймеры/положительная газета2022 | research/builds/2022/winter-loot-20261007 | report/README, primary SFC verification, loot export/demo manifests, timing tree,101tests; игровые PNG/events остаются в соседних winter-*-20261007 RUN |
| HP/бот2022 | тот же/dione-regions-bot | bot-dead.json,55-bot-lethal-fire.png, events |
| Зоны/эвакуация2022 | тот же/dione-regions-evac | region-health.json,52-region-hp-floor.png, посадка/отлёт |
| Parcel2022 | тот же/dione-integrated-01 | 52-airdrop-take.png, game-endpoint/events |
| Outcome2022 | тот же/outcome-ordered-20261007, outcome-rescued-20261007, outcome-list-20261007 | газета/Stats/lobby, схемыD62, отрицательные флаги |
| СетьV99 | research/builds/v99/hosting-route-20261006 | повтор17/19, нативные кодеки, UDP peer |
| DLL/внешние описания | research/builds/v99/external-network-review-20261006 | .text identity, окна кода, opcode index, ограничения адресов |
| LAN V99 | research/builds/v99/windows-lan-20261006 | server-summary.json, переданный лог ПК |
| Ресурсы Steam2018 | research/builds/2018/steam-19sep-20261006 | manifest/inventory, Lua, server presets, world audit |
| Host Steam2018 | research/builds/2018/steam-19sep-host-20261006 | трассы старта, модульный манифест, наблюдатель |
| Ранний2018 | research/builds/2018 | initial-analysis, index-full, extracted, binaries/provenance |
| Pipeline2022 | server/directory, server/lobby, tools | endpoint, heartbeat proxy, протокольные кодеки |

Код индексирован отдельно в [catalog/code.json](../catalog/code.json): путь, размер, SHA-256. Исполняемые файлы не скопированы. Готовый переносимый код V99 находится в ROE-LIVE/roe-server; основной код2022 — в исходном ROE_SERVER, пока не упакован как автономный Windows/LAN продукт.

## Что исключено

Игровые бинарники, полные дампы, билеты/ключи, сырой авторизационный трафик, UserData, многогигабайтные извлечения и архивы запусков не копируются. Каталоги runtime-keys и отдельные отчёты анализа ключевых блоков исключены; см. индекс. Исторические 16-байтовые hex значения скрыты в копиях; исходники не менялись.

Для запуска нужны исходный workspace, ресурсы, малые fixtures, зависимости и отдельно разрешённый локальный session-key2022. Этот репозиторий — контекст исследований, не установочный архив. Полнота передачи означает охват тем и документированных результатов; не каждый сырой артефакт оказался в Git.

Если первичного файла нет в новой среде, запросить конкретный игровой JSON, ASM, PNG или сообщение успешного outcome. Не запрашивать полный дамп сессии ради одного поля. Отчёт с сохранённым SHA не означает независимую повторную проверку его выводов.


Новое дополнение: winter-inventory-20261007/report.md и README.md скопированы с SHA в catalog/reports.json; публичный код новых инструментов индексирован в catalog/code.json. Первичные PNG, ASM, native validation и собственные captures остаются в ROE_SERVER.

Вечерний этап наборов/лута2022: [сводка](WINTER-KIT-LOOT-2022.md), выбранные текстовые доказательства в snapshots/winter-kit-loot-20261007; источники/хеши в catalog/winter-kit-loot-20261007.json. Wire/game assets/дампы/ключи/сырыеcaptures/PNG не включены. Текущий кодpeer ипереносимые fixtures в отдельном run_roe_2022.


Этап08.10: [HOST-CONSOLE-20261008](HOST-CONSOLE-20261008.md); малые публичные сводки, код и контрольные суммы добавляются отдельным snapshot `host-console-20261008`, индекс `catalog/host-console-20261008.json`. Каталоги6843предметов/8313точек, бинарные ресурсы, PNG и авторизационные captures остаются в исходном workspace.


Адресный этап08.10 MOVE02/ZONE02: [manifest](../catalog/recovery-movezone-20261008.json), [актуальный вывод](MOVEZONE-20261008.md). Историческиеmanifest не переписаны; текущийrecoveryCSV и docs имеют приоритет перед старымhand-off005–006.
