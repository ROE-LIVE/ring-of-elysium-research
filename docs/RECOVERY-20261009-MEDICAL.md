# 09.10.2026: INV02/INV08, лекарства и согласование после обрыва

Это промежуточный checkpoint текущей8-часовой работы, не окончание всего плана. Билд2022 x64 0.2.989.0, карта16010, EXE SHA256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`. Архитектура прежняя: Proton-клиент независимого runtime → локальный .NET lobby/TCP bridge → наш TGCP/UDP Python peer; собственный loopback network namespace. Встроенный host не найден.

Подтверждены три расходника70001/2/3: бинт10HP/3с, первая аптечка50HP/6с, полная100HP/8с, cap100HP. Первичная A81 исходного TableBin.sfc: block27927978, строки79/84/89, SHA `81f7e08d3af4e441fddccdae43184891c507630bde9db5105f7cd22204a94b4e`; веса2/12/20, расход1, stack999. UseCondition запрещает GetHP()>=1000; лимит75HP бинта в этом билде не подтверждён. Наша серверная политика списывает один предмет по завершении таймера; original backend/buffs/усилители не восстановлены.

Medicine record80B/category7; собственный3e82 delta91B. Decoder140bcf790→140bcf2f0→140bcefb0. Use3e80 action3 имеет container/BE16slot/extension_tag/union/own; tag0+BE32 через140c4af40→140c2fc20→140bcf170. U32 различается между сумкой иhotkey9; фиксированная маска была ошибочной гипотезой. Назначение U32 неизвестно, модель его не использует для выдачи предмета.

3e81 result0/definition запускает native animation через140e16690→own actor vtable+400→140d99fd0→140d91eb0→140f06aa0. После HP/delta нужен2b status27:140e88150 switch→140e88543→140f06f00 выводит из action8. Один537 оставлял F Cancel. Native F при закрытой сумке отправляет536/20: отмена сохраняетHP/стак. F внутри открытой сумки запроса не создала. Удержаниеhotkey9 на0.2с повторяет лечение; короткие автоматические нажатия иногда не породили запрос и не считаются protocol failure.

Cold55:5→4→3→2бинта,75→85→95→100HP, автоматическое завершение. Cold56: cancel при25HP/5бинтах; firstaid25→75/1→0/6с, medkit75→100/1→0/8с. Cold57 отрицательный OUTPUT/drop20с: сервер55HP/2бинта, native45HP/3бинта после reconnect — потерянные финальные RPC не восстановились.

Исправление переносит MedicalState с прежнимdeadline и однократно согласует известные slots/HP:3e82 current/clear,4a0 магазины, kit/вес,1069HP, при недавно завершённом леченииstatus27. НовыеUID/ground entities/5fb не выдаются. Cold58: pending use до20с обрыва; послеhandoff native35HP/4бинта иCitori2/6,M4 28/20 совпали ссервером. После этого новые heal/fire/reload/switch прошли:45HP/3бинта,Citori2/5,M4 27/20.

Cold58 выявил legacy5fb приобычном drop: activeM4 сбрасывался вslot1. Введён explicit inventory_update=delta. Cold59 gun/ammo/medicalpickup, drop/repick5бинтов сохраняют activeM4 29/20; armor201003 durable250, бинт25→35HP/5→4 возвращаетslot2. Windows materialize включает этот режим и12фиксированных ground items. Старый snapshot default сохранён для воспроизведения прежних опытов. Физический Windows-повтор новых возможностей ещё нужен.

Проверки:182main/108kit Python tests; verify-onlym4+armored; .NET8build0warnings/0errors. EXE/ProtocalHandler_x64.dll/Tenproxy64.dll original/runtimeSHA неизменны, inodeразные. Исходные изменяемые модули: weapon_probe_2022.py, medical_probe_2022.py, game_endpoint_probe_2022.py, loot_catalog_2022.py; Windows tools/windows_launch.py.

Следующий шагINV02 — native split/move/merge(IDINV05), затемpages/attachments иWindows. ОбщийINV02 остаётсяpartial; long/vehicle reconnect, originalarmor/raycast/AI иполныйmatch не закрыты. [CSV](recovery/mechanics-2022.csv) и[сводка](recovery/status.md) актуальны; проценты относятся кэтапамплана.

Переносимые первичные выдержки иотчёт: [snapshot](../snapshots/recovery-medical-20261009/report.md), [evidence](../snapshots/recovery-medical-20261009/evidence.json), [индексSHA](../catalog/recovery-medical-20261009.json). Бинарныеfixtures/rawAUTH/full dumps не включены; ониостаютсявисходномworkspace `ROE_SERVER/research/builds/2022/recovery/022-inv02/20261008T2310/` иown runs54–59.
