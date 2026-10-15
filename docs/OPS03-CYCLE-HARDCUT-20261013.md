# OPS03/NET06 — cycle и полный разрыв TCP

2022 x64 0.2.989.0, корневой Europa_Client.exe SHA2562dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18, карта16010. Это реконструированный peer, не найденный встроенный host.

## Подтверждено

355: portable Linux `--services-only --lan-tunnel --mode cycle --profile ops03-control --reliable-udp --idle-handoff`, отдельный Proton network namespace. Связь через собственные loopback/Unix forwarders вместо SSH. Стадии1/10/20/30/40/50, дроп, вертолёт, F05:02:49→05:03:04 singleplayer_evacuation_finish, rescued1, native DIONE NEWS/Rescued1. Последняя безопасная клетка24. Учебный ускоренный календарь и диагностический preset, не исходный баланс.

356: hard TCP disconnect20с, живой backend. Первый handoff через21.85с сохранил позицию366022/544000/259058, комплект и1/6; последующие fire0/6→reload2/4 приняты. Второй обрыв во время reload показал сомнительный HUD; число магазина тогда не подтверждено getter. Не использовать это как положительное доказательство pending reload.

357: числовые публичные HUD getters перед выстрелом2/6, перед reload1/6, после hard disconnect20с1/5; сервер при этом2/5. Обрыв через~0.485с послеR, раньше deadline1.48с; handoff через23.41с. Это воспроизводимое рассогласование магазина.

## Отрицательный вариант исправления

В отклонённом кандидате game_endpoint_probe_2022.py restore_resume_inventory сначала вызывал weapon.poll(now), затем reconcile_inventory. Ранее snapshot1/6 отправлялся до завершения pending reload2/5; позднее применение inventory могло возвращать старый магазин. Семантика клиентской очереди — гипотеза, факт — различие числовых состояний. Кандидат завершал просроченную reload до snapshot, ещё не наступившую сохранял. Тест проверяет оба случая и однократность согласования. 519source/480portable testsOK (известные socket ResourceWarning в suite, failures0).

358: серверная очередь кандидата reload2/5→resume inventory; native getter после разрыва0/5. Кандидат НЕ исправил клиент и удалён из рабочей source/portable сборки. Patch и серверный regression сохранены только как исследовательский отрицательный материал.519/480 — проверки именно кандидата, не подтверждение native исправления. После ручногоR05:47:09 сервер ответил amount0,2/5; native snapshot4 тоже2/5 — магазин возвращается без повторного расхода резерва. Точная причина клиентской перезаписи/предсказания ещё не установлена. Следующий опыт: tracing handlers4A0/ITEM_DATA, локального prediction counter и повторной доставки после полного применения inventory, с native getter каждого шага. Не менять counter наугад.

## Источники и ограничения

Исходные355–358: research/builds/2022/host-console-20261007/recovery-ops03-split-20261013-NNN; серверные runs:355=20261013T045351-0f6abb,356=20261013T050638-06587c,357=20261013T052918-8e24ff,358=20261013T054208-bb8f72. Публичные события/геттеры приложены отдельно. Helper/getters: docs/DEBUG-SNAPSHOTS-20261013.md; транспорт: docs/LAN-SSH-20261013.md. Полный TCP-разрыв заменяет прежнюю buffered pause351; он не доказывает реальный Windows/SSH/LAN. Один клиент, head-of-line; следующая приёмка Windows→Linux с повторнымTraining. Native355–358 остановлены, выбранные оригинальные/runtime EXE/DLL hashes совпали.

4A0 decoder140C37130; поля UID_U64/slot_U32/clip_U32/prediction_counter_U32. Первичная проверка11DA→4A0: research/builds/2022/weapons-probe-20261005/report.md. Последний U32 не запас; самовольная подмена не обоснована.

После удаления кандидата повторено518source/479portable testsOK; verify-onlyOK. Рабочие source/portable endpoint и test byte-identical опубликованномуHEAD.

Полный локальный источник: `research/builds/2022/recovery/110-ops03/20261013T0540-cycle-hardcut/report.md`.
