# OPS04 — команды серверного состояния,12.10.2026

Билд2022 x64 0.2.989.0/map16010, SHA2562dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18; независимыйProton318/loopback. Это собственные административные действия диагностического peer, не найденная оригинальная console.

## Реализация

live-commands.json принимает три typedactions: set_own_health(hp), give_ammo(definition/quantity), damage_npc(damage). StateSceneActions обновляет WorldState/WeaponState/ActorState и формирует native1069/3E82/4A0/6F5/533, а не только выдаёт wireпакет. HP1..profileHP, ammo1..100 для30004/30001/30002/30005, NPCdamage1..1000. Нет оживления dead, общего roomadmin и произвольного actorMemorywrite. Старые rawcommands остаются; соседние rawгруппы отправляются одним batch с сохранением порядка относительно stateactions.

Парсер проверяет весь файл до применения, связывает optionalrecipient с AccountUID, ID подтверждается один раз после отправки/отказа. Идемпотентность действует в текущей сессии/процессе, не между перезапусками. Действие, отклонённое из-за текущего состояния, не повторяется автоматически; для новой попытки нужен новыйID. Неверный файл не останавливает обработку мира.

NPCdamage сначала готовиткопиюActorState/живогоинвентаря/DeathParcelState; malformedcorpse не оставляет половинуизменений. Перед смертью актуализируется остаточная прочность брони. Административная смерть не записывается как настоящий kill игрока. Giveammo требует вместить всю выдачу, сохраняет hand/clip/UID, не создаёт новоеоружие. tools/scene_action_2022.py добавляет действие через atomicreplace, сохраняет прежнюю очередь и отвергает другой запрос с тем жеID. Один писатель очереди; совместное одновременное редактирование не является поддержанным API.

## Native318

12:51:12UTC: set_own_health1000→425, give_ammo6→9, damage_npc1000→900. Native own425/Alive0 и NPC900/Alive0/Citori1e00000100100001 подтверждены выбранными срезами12:52:26. PNG318-state-actions:HUD42 иCitori2/9. Значение425 — rawHP, HUD показывает примерно42/100. Повторная запись тех жеID новых действий не дала; исходные ID по одному разу в318-state-events.json.

12:55:37 damage_npc1000 добивает оставшиеся900. Создан ровно один corpse с Citori clip2/темжеUID и6патронами. Native12:57:32 HP0/Alive1/позиция прежняяsafe, ownнеподменён.13:00:37 новый damage_npc наdead отклонён(active_npc_required); повторноголута нет. Выдача100патронов reserve9→109; следующая100 отклонена(insufficient_bag_capacity), clip2/hand сохраняются. PNG318-ammo-capacity-control показывает текущий результат. Исходная death/armor policy этим не восстановлена.

474source/434portable tests, verify-only -LiveControl и.NET8build прошли. Семь новых проверок: реальнаяWorldmutation/ownisolation/deadguard, ammo/capacity/currentclip, NPCdeath/currentinventory, rollbackbadfixture, recipient/ID/mixedwire, wholefilevalidation, atomicqueue/conflictingID.

Windows: `run-roe-2022.cmd -Mode cycle -Bots -BotGroundRoute -BotBehavior -ReliableUDP -IdleHandoff -LiveControl`; команды во втором PowerShell через .tools/python/python.exe иtools/scene_action_2022.py. Инструкция docs/STATE-CONTROL-20261012.md. Windows этого профиля ещё требует пользовательского прогона; Proton не его доказательство.

OPS04 baseline65% этапов(2/1/1/1/2/1). Это ограниченный controller из трёх действий. Zone/погода/предметныйspawn/vehicle/общийroom/restartpersistentID иUIпанель не закрыты. Следующий по таблице LOOK01; OPS02 ждёт новогоWindows run, MP01 требует первичногоwinterteamdamage материала.
