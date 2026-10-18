# BOT05: сохранение контроллера при handoff — 18.10.2026

Корневой2022 x64 0.2.989.0, Iceland16010, EXE SHA256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`. Native007, независимый runtime/Proton, loopback namespace. Это одиночный собственный loot/safe controller, не исходный AI и не десять активных ботов.

## Исправление и проверка

`resume_gameplay` теперь переносит **тот же BotController** вместе с actor, инвентарём и TargetRoster; `finish_gameplay` удаляет его. Ранее после переноса actor/инвентаря поле controller не переносилось, что позволяло создать пустой новый контроллер. Unit проверяет идентичность объектов, phase и потраченные патроны, а не только совпадение числа целей.

В Native007 materialized Windows `-Bots -BotGroundRoute -BotBehavior` NPC0x2040000123460 сам подобрал Citori10402 и12ga×6, прошёл измеренный граф до safe370668/543184/258712. Это прежний ограниченный маршрут, не navmesh всей карты. После этого выполнен настоящий20секундный обрывC2S UDP и handoff.

Адресный read-only снимок native actor до/после: **тот же actor0x64CDEAB8, Citori instance0x1E00000100100001, HP1000, позиция safe**, оборудование и FSM сохранены. Скрипт `sample_target.py` читает только выбранный UID/ограниченные поля через `/proc/PID/mem`; полный дамп не снимался, память не изменялась. Первый запуск чтения без прав дал PermissionError, повтор с sudo-n выполнил только этот bounded reader.

В журнале за весь прогон ровно один bot_behavior_begin и два bot_loot_pickup; после handoff фаза подбора не началась заново. Затем административный damage_npc завершил жизнь NPC: контейнер получил **тот же Citori сclip2 и ровно6патронов**. Стартовых9mm/бинтов/способности игрока в NPC не было. Это проверка текущего инвентаря и смерти после handoff, не убийство выстрелом и не AI combat.

Первичные данные: `research/builds/2022/recovery/101-bot05/20261018T1145-controller-handoff/native007-{before,after,result}.json`, `exercise.py`, `exercise007-retry.log`, `source-hashes.json`, `cleanup007.json`. Full-run локально: `host-console-20261007/recovery-bot05-handoff-20261018-007`. Начальная ошибка параметра room была остановлена preflight до запуска клиента; использован проверенный бинарный room fixture.

Эвакуация NPC по-прежнему недоступна: outside_verified_graph/rope_and_boarding_unimplemented. Атака после самостоятельного подбора, HP от зон, полноценная навигация и Windows нового исправления не проверены. Для статичных мишеней используется отдельный -PracticeTargets; сочетать его с Bots нельзя. ОценкаBOT05 остаётся55% этапов плана, а не55% исходного AI.
