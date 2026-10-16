16.10: Windows150144 принят; fullR current17/capacity2 исправлен через ITEM_DATA+54. Native021 Glock/M4/AK/40mag и022smoke8/AOI подтверждены. Opt-in oneRock:023AKthrough/sourceenergy;024M4thickstop, M4through не подтверждён. Windows нового fix — W18 CSV. 10мишеней пока не реализованы. См.docs/SESSION-RESULT-20261016-AFTERNOON.md.

16.10: WindowsW17 20261016T134206-fafd00 принят: AKмодули/сохранениеоружия, штатныеотметки+audible/head/kill/Rescued1. ПолныйGlockR17/14 запускаетанимацию/звук, ammounchanged; открытGUN02. НовыетестыCSVW18послеисправления; не повторятьW17целиком. docs/WINDOWS-W17-REVIEW-20261016.txt.

# Состояние16.10.2026

Рабочая основа —2022 x64 0.2.989.0, карта16010. Windows starter-v1: подтверждены три слота, подбор, огонь/перезарядка, модули, мишень, двери/стекло по пользовательскому тесту, зоны и эвакуация. Последний матч по первичным events: Kill1/Rescued1/35937см/202с, совпадает с видео. [Разбор](docs/WINDOWS-RAW-REVIEW-20261015.md).

ПотерюHP возле троса вызывал учебный прямоугольник, а не закрытый регион. В новом launcher feedback-v2 он opt-in; согласованный CycleScale3 проверен в Proton. Новая публичная упаковка с внешним CK ещё не проверена запуском на Windows. Проценты CSV — выполненные этапы плана, не процент всей игры.

Новый этап16.10: INV07 прямой ground→gun и удаление82B подтверждены native004; GUN05 —11EB/штатные белые, оранжевые, красные и head-отметки со звуковыми событиями, native005/006.579source/551portabletests. [Разбор](docs/HIT-FEEDBACK-20261016.md), [W17 в launcher](https://github.com/ROE-LIVE/ring-of-elysium-local/blob/main/WINDOWS-TESTS-W17.md). Windows новой ревизии отдельно.

Приоритеты дальнейших работ:

1. OPS02: один Windows-повтор новой упаковки — вход, безопасный подъём, эвакуация. Пройденный W15 целиком повторять не требуется.
2. GUN07: producer/actor userdata/HEAD1 BODY2 LIMB3 установлены; исходный authoritative HP по-прежнему требует original hurt trace/provider. Найденная формула клиентской потери энергии на материале проверена M4/AK, не заменяет hurt. [Цепочка](docs/HIT-COLLISION-PRODUCER-20261016.md), [преграда и материалы](docs/PROJECTILE-MATERIALS-20261016.md).
3. NET06: не закрывать отрицательный Citori374 (peer2/5,HUD1/5) успешным опытом другого профиля.
4. LOOT01: карта8313точек/21группа — опора; исходный RNG/выбор групп полностью не восстановлен. [Пресеты](docs/LOOT-PRESETS-20261013.md).

Анимация полной R, cold Appearance, исходный AI/баланс/сетевая полноценная общая сессия остаются открытыми. Боты/транспорт содержат отдельные диагностические модели. В CSV сохраняются исторические детали; новая проверка должна явно указывать ревизию.

Дополнение16.10: Native009 AK directmount/UDP20s; GUN06 native Rock triangle/front/hidden/exposed + offline server guard. Новая геометрия opt-in и не включена в обычную Windows-карту. GUN06 этапы67.5; остальные оценки без повышения.

Проверки этапа:586source/558public/547legacy/2research;9public PowerShell skips выполнены отдельно. Оба verify-only passed; новая Windows-проверка остаётся W17.

## Новый этап16.10: source collision и extended hit

16.10 06:24UTC: Native017 genuine AKthroughRock energy47→27.25454,11DD144/count2 принят→HP900→800/11EB/UI/Wwise. Source RepX одного камня1623/3145/BVH и7точек; исходные serverHP/penetration иWindows пока открыты. docs/HIT-RECORDS-20261016.md, SOURCE-COLLISION-20261016.md.

Первый настоящий144байтный hit014 выявил ошибку strict106. Новый Native017 подтвердил исправление живым выстрелом; это отдельно от offline replay. Обычный Windows-пресет не получает solidmesh. См.[разбор пакета](docs/HIT-RECORDS-20261016.md) и[ресурс коллизии](docs/SOURCE-COLLISION-20261016.md).

16.10 07:16UTC: Native019 source heightfield2112²,49материалов; Linux/Win samplesSHA совпали. Reader безSDK:2genuineSnowfloorheight/normal/face совпали<=0.00718cm;12DLLoracle/6unit. tools/probe_iceland_heightfield_2022.py; defaultspawn не менялся. docs/TERRAIN-HEIGHTFIELD-20261016.md.

Текущие проверки:607source/579public/568legacy/8research. Высоты не заменяют верхние этажи/камни/charactercapsule. WindowsW17 остаётся отдельным контролем.
