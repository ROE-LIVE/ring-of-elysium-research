# Семичасовая сессия восстановления2022 — 9 октября2026

Работа по плану2, окно14:26:30–21:26:30UTC. Клиент2022x64 0.2.989.0, зимняя map16010; независимая runtime-копия, Proton11-7/Xvfb, собственный peer/loopback. Оригиналы не менялись, git/network только чтение, Docker/дополнительные модели/Ghidra не использовались.

Последовательно выполнены проверки NET04/NET06/ZONE02, NET05, LOOT05, INV02/INV03, KIT01/KIT05/INV04, KIT02; текущая незакрытая задача KIT03. Baseline означает воспроизводимую опору, не полностью оригинальную механику.

Изменения peer: ограниченная сборка входного потока и outgoing ACK/retry; перенос idle authenticated peer с сохранением мира/позиции/HP/items/pending reload; восстановление текущей стадии зон с elapsed; serial32 guard пяти известных действий; общий codec известных ITEM unions/BE16ref; загрузка явно заданной прочности брони. Все эти правила — реконструкция, original server/provider не найден. Надёжный UDP и idlehandoff opt-in, default launcher legacy.

Native Proton: потерянные spawn/delta лута повторно доставляются; reverse/duplicate discard даёт одно выпадениеM4; helmet37 переживает drop/handoff/repick. Три зимних набора включают одну способность и capacity150/225/300 с непустым inventory. Два вида патронов частично подбираются у лимита; независимый ledger17 переходов сохраняет200x5.56 и108x12ga с одним выстрелом. Смена300→150 при212.5 сохраняет выданное. Сноуборд T включается/снимается, едет, raw3off запрещает активацию; без диагностического positionRPC.

KIT03: 16 коротких motion traces normaljump на реальном рельефе, FSM0/4/5/6 без9. Найден native GET_ON_GLIDER→140ec4bd0; live config5 200/450/450/600 и отказы front/near/offset ray подтверждены. Штатный полёт/посадка не получены, ready80 не повышен. Следующий опыт — резкий уступ с открытым смещённым лучом, затем allowed1/FSM9/посадка. KIT04 №83 пока queued: компонент кирок есть, лазание не доказано.

Проверки последнего изменённого кода:246 source tests,172 Windows-kit tests, verify-only passed. Новые read-only KIT03 scripts AST/preflight passed; cold101/103 exit124, выбранные EXE/DLL hashes до/после совпали, runner cleanup завершён. Native Windows повтор этой сессии не проводился. В run_roe_2022 commit27e4835 находится актуальная реализация; context дополняется отчётами и CSV. Новые проценты этапов нельзя выдавать за процент восстановления оригинальной игры.

План: `docs/recovery/mechanics-2022.csv`; подробные отчёты в `research/builds/2022/recovery/`. Текущая точка передачи: `028-kit03/20261009T2008-native-jump/report.md`. Отрицательные ошибочные fixtures/пустые observers/неудачный холодный запуск сохранены отдельно.
