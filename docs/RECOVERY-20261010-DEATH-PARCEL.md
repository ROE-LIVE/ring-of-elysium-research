# Контейнер смерти: результат10.10

LOOT10 baseline82.5% этапов, не done/не процент игры. [Первичный отчёт](../snapshots/recovery-death-parcel-20261010/report.md), [evidence](../snapshots/recovery-death-parcel-20261010/evidence.json).

821/subtype1 создаёт исходный30201002/E_EU_KILL_LOOT; BCE→3B61→3B63→3B64. Cold137: genuinekill/passive-target inventory→gunclip2/ammo7/vestdurable50, nativepickup2ndgun/reserve13/UI5. Cold138: reverse/duplicateC2Ssegment приводит к одномуpickup,20сS2Chandoff сохраняет остатки. Cold139: own HP0/533 переноситactualinventory один раз и очищает источник; dead flags/XYZ/emptyinventory сохраняются послеhandoff.

Модули/тесты с конкретными источниками вsnapshot/source; основная разработкаROE_SERVER. Windows-комплектrun_roe_2022 переносит это поведение; Targetplain/armored включают отдельный контролируемыйinventory. Не выдавать его заoriginalAI; kit11exclusionpolicy наша. Windows/multiplayer/полныйnativepickmedical/throwable/modules отдельно.

Следующий №51/GUN08: полябаллистики→nativeconstructor/update. OriginalhurtGUN07 иfallMOVE05 ждутсанитизированнуюauthoritativetrace/provider; не превращать найденныйtablevalue внеподтвержденнуюHPформулу.
