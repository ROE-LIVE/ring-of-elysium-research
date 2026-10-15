# Два слота, перезарядка и мишень2022

Состояние08.10.2026, после cold46–51. Этот итог заменяет прежние ограничения одного gun slot и отсутствие расхода брони **для пассивной remote мишени**. Исходная защита собственного игрока всё ещё неизвестна.

Билд2022 x64 **0.2.989.0**, EXE SHA `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`, база140000000, зимняя карта16010. Runtime независим от оригинала. Архитектура прежняя: локальное.NET lobby → TCP bridge → TGCP/UDP Python peer → клиент под GE-Proton11-7/Xvfb; loopback namespace. Это реконструкция внешнего сервера. Нативный host не найден, серверная логика из EXE не извлечена. Docker/Ghidra/дополнительные модели в этом этапе не использовались.

## Что изменено и проверено

| Работа | Первичное подтверждение | Граница |
| --- | --- | --- |
| Два оружия | Registry slots1/2, устойчивые UID/definition/clip; native1/2, alternating fire/reload, drop/repick в cold46. Cold51 на итоговых materialized configs показывает M4A1 30/19+Citori2/5 | Citori/M4; pages, consumables, attachments и dual-gun reconnect ещё нужны |
| Перезарядка | A89 времена Citori2.130/1.480 и M4 2.567/2.083с. Server deadline, ammo3e82, clip4a0; без полного5fb/лишнего49f. Cold48 switch отменяет ожидание без расхода; cold51 обе пушки перезаряжаются отдельно | UI процесса и смена поз подProton видны; новый native Windows-повтор нужен |
| Пассивная мишень | Cold47 genuine Citori pellets: nativeHP1000→100→0, тело на снегу. Cold49 автоматически выдаёт remote жилет300 и HP1000 | Один actor; не AI, не самостоятельный bot server |
| Учебная броня | Cold49 M4 hits: durable300→250→100→50→0; HP1000→950→800→750→700; следующий hit→600 при durable0. UID жилета неизменен. Промах тратит ammo, но не HP/durable | Наш баланс50%, не исходная формула ROE; body/head и server LOS отсутствуют |

Правильный foreign armor RPC — **547**, тело82B: slot+24, durable+65, quantity+69. Native decoder **140c356b0→140c35320**, handler **140e7dbd0**; slot **140e7dd0a**, armor branch **140e7dd47→140fb1f20**, durable copy **140e7dcc2**, item+3c. Body actorQ/countI + defI/instanceQ/slotI/flagB + accessory countI +7gun-propertyI +4I(metadata,durable,quantity,unknown) +tailI/B.

Отрицательный контроль: **3e82 не обновляет чужого actor**, handler140e162d0 сравнивает ownUID в140e16317/23. `own=0` выбирает world inventory своего actor. Попытка547 с durable+33/slot+69 тоже неверна. Только corrected layout дал native slot12/durable300; холодный автоматический сценарий затем подтвердил уменьшение от настоящих выстрелов. Не повторять прежнюю гипотезу «own0 адресует другого игрока».

11dd106B: UID+4,point+37,counter+88,tick+96;11ea36B подтверждает hit,1069 передаёт HP,533 смерть. Наш hit требует принятого выстрела, правильной цели/позиции/дистанции и уникальной identity. Ограничение12 hits на shot пока общее, server raycast/LOS не восстановлен. Параметр pellet_damage не равен исходному weapon damage.

## Запуск пользователя и следующий агент

В приватном [run_roe_2022](https://github.com/ROE-LIVE/run_roe_2022):

```powershell
git pull --ff-only
.\run-roe-2022.cmd -WeaponProfile m4 -Target armored
```

Полный клиент — `G:\REsearch\Ring of Elysium-2022`. Первая установка создаёт независимую копию; последующие переиспользуют её. Training, клетка,47с; подобрать M4/5.56 и Citori около8м дальше;1/2/R. Мишень восточнее стартового лута около Jeep. Plain — контроль без брони. Target иBots вместе запрещены; новая мишень после смерти требует нового сеанса. Журнал: runs/<run>/scene/events.jsonl, события actor_probe/weapon_probe; HP/прочность отдельной полоской над мишенью не выводятся.

Предыдущий Windows-прогон пользователя подтвердил pickup/ammo/reload, но выявил1/2 и анимацию. **Новый профиль Windows11 в этом этапе не проверялся**: все новые игровые доказательства — Proton.97 тестов переносимого комплекта,171 основного дерева, verify-only m4/armored и citori/plain прошли; .NET8 Release0warnings/0errors; PowerShell parser0errors/BOM сохранён. SHA оригинальных EXE/двухDLL неизменны; свои процессы остановлены. Runs45/50 с ошибками подготовки исключены из positive evidence.

Очередь остаётся **№22/INV02**, теперь pages/consumable item union; отдельно dual-gun reconnect и Windows-повтор. [CSV](recovery/mechanics-2022.csv): INV02 50%, INV06 82.5%, GUN03 50%, HP03/04 50% **diagnostic**. Core65.7%/target40.4% — достижение этапов плана, не доля восстановленной игры. Исходные damage/armor/hit-zone нужны из authoritative hurt trace либо исполняемого оригинального расчёта; имеющийся50% preset их не заменяет.

Начало работы: `python -B tools/recovery_task.py --task INV02 --preflight` в полномROE_SERVER, затем карточка задачи и [RUNBOOK](recovery/RUNBOOK.md). Снимки кода здесь служат контекстом, для игрового повторения нужны исходный workspace/runtime/fixtures и текущее разрешение пользователя.

Первичный [отчёт](../snapshots/recovery-slots-target-20261008/report.md), [evidence](../snapshots/recovery-slots-target-20261008/evidence.json), [проверки](../snapshots/recovery-slots-target-20261008/checks.txt), [происхождение и SHA](../catalog/recovery-slots-target-20261008.json). Сырые AUTH, ключи, игровые бинарники и полные дампы в этот репозиторий не перенесены.
