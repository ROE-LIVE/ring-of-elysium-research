# ENV01: исходные сутки и переходы

Билд2022 x64 0.2.989.0, map16010, EXE SHA2562dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18. Опыт154: research/builds/2022/host-console-20261007/recovery-env01-clock-20261010-154, 10 октября22:32–22:36UTC. Только независимая runtime-копия, own loopback/Proton, без изменения памяти/регистров клиента.

## Источник

DATA/TABLE/ENVRTIMETABLE.XML (TableBin95):720мин,24веса суммой10000; коэффициент4.32сек/единицу. Периоды7/8/15 имеют вес900, длительность3888с;16 вес400/1728с. Точная float32 runtime scale4.320000171661377. DATA/TABLE/ENVRMAPTIMETABLE.XML (TableBin140): map16010 допускает старт7/8/15/16 с равными весами10. SHA и24строки вresource-times.json. Равные веса не доказывают исходный RNG/seed.

## Нативный контроль

4816 = hourBE32 + UNIX secondsBE32, а не scene ticks. Consumer140CD80D0 задаётstart_hour+148 и baseline_seconds+150 относительно native UNIX clock; getter140CD8580/140CD85B0 проходит weighted durations. Аппаратные точки consumer140CD80D0, return140CD82FD, hour140CD86F1 (EBX и XMM2 fraction), finalweather1413A032B. Только публичный weather object143040750/+148/+14C/+150/+154/+160/+70, max128байт за чтение; script clock_watch_gdb.py.

Однократные4816, затем обычный ход часов без новых сообщений:7→8 через7.002с после near-boundary установки,15→16 через7.003с,16→17 через7.002с. Задавали начало периода на3882/1722с в прошлом; остаток номинально6с, наблюдаемая разница зависит от целых UNIX секунд/доставки/native time. Код скорости не менялся. Main_period dawn1→day2 при7→8 и day2→dawn1 при16→17. PNG154-hour7 показываетDawn,154-hour8-natural Morning,154-hour16-natural/154-hour17-natural Evening;15→16 оба day2, но HUD-label меняется. Первичные timestamps/fractions/аргументы вclock-observer.json иclock-actions.json.

## Перенос в Windows

Обнаружено отсутствие --environment-config в прежней endpoint-команде Windows launcher: модуль был в комплекте, но начальный час/температура не подключались. Добавленыconfig/environment.json, передача endpoint-флага и выбор -StartHour7/8/15/16; default8,temperature500=5°C. Lobby уже передавал --local-server-clock, сохранён. materialize валидирует выбранный час и EnvironmentFixture до запуска; исходный config не меняет. Исправлен устаревший текст о невозможности выбора клетки/комплекта: эти UI действия уже реализованы отдельными этапами.

Команда: .\run-roe-2022.cmd -Mode cycle -StartHour7 -ReliableUDP -IdleHandoff. Нативные переходы проверены Proton, новый настоящий Windows-повтор ещё нужен. Фиксированное начало не выдаётся за оригинальный случайный выбор. End-to-end проверка процесса Windows не выполнена в этом опыте; endpoint environment path и wire проверены материализацией/тестами.

## Отрицательные результаты и ограничения

ПрямойPE-offset для140CD8700 выдал данные вне raw части соответствующей packed .tp6: virtual section длиннее raw. disk-rva-negative-140cd8700.asm не является кодом функции; его нельзя использовать как доказательство. Рабочие адреса подтверждены live hardware наблюдением, исторический getterASM использован для выбора точки.

Не наблюдали непрерывные720мин, всю24часовую петлю и исходную стратегию RNG. Temp500 фиксирована, полный климат/холод отдельные механики.244 переносимых теста,verify-only7/16,.NETbuild0warnings/0errors иdiff-check прошли. Адресная остановка143 ожидаемая; контрольные SHA оригинала/runtime совпали до/после, безhardlink (cleanup.json). Следующая задача по порядкуENV03, передача signed температуры с погодой/часами.
