# Контроль попаданий2022: ray/AABB,09.10.2026

GUN06 baseline57.5% этапов. [Первичный отчёт](../snapshots/recovery-gun06-los-20261009/report.md), [положительные и отрицательные доказательства](../snapshots/recovery-gun06-los-20261009/evidence.json). Это наши диагностические правила, не найденный встроенный host/коллизия исходной карты.

Принятый11DA хранит origin/aim/counter/tick;11DD содержит origin+25,actorposition+37,impact+50. Native140c3fe00→140bcd900 подтверждён адресно в собственном процессе. Проверка перед изменениемHP/брони: UID/acceptedshot/duplicate/range + начало100см,impact250см,конус10°, пересечение отрезка с явно заданными AABB. None отключает новый контроль,[] включает без преград.

Nativecold70 open: реальный M4hit1000→900, cache900/900/1000. Cold71 blocked: реальныйhit отклонёнline_of_sight,cache1000/1000/1000; W за объём +следующийhit снова900/900/1000. Преграда невидимая,движение не блокирует. 201 основных/129kitтестов,verify-only16loot,.NETRelease0warnings/errors. Оригинал/runtimeтриSHAсовпали,независимые;своиопытыостановлены143.

Windowsкомплект: `git/run_roe_2022`; команда `run-roe-2022.cmd -WeaponProfile m4 -Target plain -TargetLOS open`, затем отдельно `-TargetLOS blocked`. Новая Windowsпроверкаожидается; пользователь отдельно подтвердил базовые оружейные действия09.10безcommit/log. ОбычныйрежимLOSoff,новыепараметрыопциональны.

Нет collisionmesh/materialpenetration/gravity/lagcomp/authorityorigin; nativeCitori/AKсновымLOS отдельно. СледующийGUN06опыт — геометрия одного настоящего препятствия и nativeстена. Очередь далееGUN07: первичный базовыйурон/hitzone. Текущий damage100raw учебный.

Далее: [GUN07: первичные параметры и телеметрия](RECOVERY-20261009-DAMAGE.md).
