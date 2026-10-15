# Баллистика2022: проверенный клиентский расчёт

GUN08baseline67.5 этапов, следующая№52/GUN09. Citori/M4 native speed/drag/gravity/range; шесть измеренных20мс шагов побитно совпали с float32 модулем. Source295/portable227 tests, verify-only/.NET build проходят.

Результат и границы: [отчёт](../snapshots/recovery-ballistics-20261010/report.md), [evidence](../snapshots/recovery-ballistics-20261010/evidence.json). Cold140/141 завершены, SHA EXE/DLL совпали.

Модуль ballistics_2022 и replay tool позволяют считать полёт по явным параметрам. Правила HP/попаданий прежние; originalspread/collision/lag compensation и serverauthority не восстановлены. Citori native range30000 совпадает с QS Params.Range, speed36000 с A89, тогда как QS speed30000. Порядок override ещё открыт. Windows11 отдельно.
