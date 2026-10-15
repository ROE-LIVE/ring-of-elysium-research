# HOST02: снимки состояния через клиентскую консоль2022

15.10.2026: ограниченный числовой снимок дополнен магазином слота3, запасами Glock/DE, количеством бинтов/аптечек и предметов трёх зимних наборов. Getter `qs.GetInventoryNumber` проверен native NET06; ранний UI кадр бинтов0 был временным, getter и финальный кадр показывали5. Поля собираются по той же одноразовой команде ниже. Ошибочный или недоступный API записывается как `unavailable`. Исследовательский протокол: `docs/SOURCE-CYCLE-20261015.md`.

13.10.2026; root Europa_Client.exe0.2.989.0 x64, SHA256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`, база140000000. Независимая runtime-копия, GE-Proton11-7, isolated loopback. Оригиналы не изменены. HOST02baseline90; Windows-повтор новой опции ещё нужен.

## Результат

Реализован ручной снимок числовых HUD-полей без отладчика. Добавлена опция `-DebugConsole` в Windows-комплект и `--debug-console` в research runner. Собственный `FileDriven/_GM_CONTROL_` создаётся до запуска. Имеющийся пользовательский marker сохраняется; новые Lua/TSV имеют уникальные имена. После штатного завершения числовой TSV переносится в журнал, собственные файлы/marker удаляются. Игровые setters, AUTH/globals dump и генерация сервера помощником не выполняются.

Native352: аппаратные точки, без patch/register writes, фиксируют parser140502520→event1418D53D0→Lua return1410030DD/R10B=1. Собственная команда через `assert(loadstring(assert(io.open(...)):read("*a")))()` исполняет Lua. Первый `dofile(...)` также вернул1, но файла результата не создал: return1 сам по себе не доказывает исполнение требуемого сценария.

Три снимка совпали с серверным журналом: magazine2/reserve6→fire1/6→timed reload2/5. Native353 — новый холодный запуск уже с тем же DebugConsoleSession, который используется Windows launcher: зимняя сцена/cycle; повтор2/6→1/6→2/5. GetGameTime≈0.333 соответствует заданным8:00 и увеличивается. Native354 безmarker: gate1430554F8=0; ввод собственной команды не вызвал parser/event/Lua return, числового TSV нет. GUI-путь ограничен этим опытом; не переносить результат на все другие консоли.

Все352–354 остановлены; selected original/runtime EXE/DLL SHA совпали. Marker и новые Lua-файлы удалены.518source/479portable testsOK; verify-only/verify-cycleOK, PowerShell parserOK, .NET8Release ранее0errors/0warnings.

## Первичные источники

Из повторной распаковки2022, SHA сверены с lua-index:

- `DATA/SCRIPT/LOGIC/GAMEPLAY/UI/EUCURWEAPONPANEL/EUCURWEAPONPANELLOGIC.LUA`:67 GetInventoryWeaponAmmoInBag(gun_id),73 GetInventoryWeaponAmmoLoaded(slot); SHAcfc74797…d88d.
- `DATA/SCRIPT/LOGIC/GAMEPLAY/UI/ICELANDNIGHT/GAMETIMEPANEL/GAMETIMEPANELLOGIC.LUA`:25 GetGameTime(),57 GetPlayerRawAttri(ATR_BODY_TEMPERATURE),92 GetFinalMapWeather(); SHA95963ab7…f77c.

Точный manifest `primary-getter-lua-provenance.json`; исходные54 archive SHA ранее проверены full-extraction-20261010/original-verification.json. Читаются только фиксированные публичные getters. Body temperature — отдельный атрибут персонажа, не заданная температура среды500.

Важный отрицательный контроль: `qs.GetCurrentMapId()` даёт10020 в этих опытах, а ENTER_ROOM profile.base.m644 wire+317 содержит16010. Регистрация строки14288E1E0 через pointer14261AF50 связывает getter с1418CCA10. При1418CCA2C инструкцияmovd читаетDWORD143040770; getter не обращается к текущему world. Найдены34ограниченных code refs, включая writers140D67504/140DEB03D/1410312B5; их полная семантика ещё не установлена. Поэтому поле названо `qs_current_map_id_unclassified`, не объявляется доказательством активной карты или host. qs.GetMapId — иной API с аргументом, не подмена этого getter.

## Как пользоваться на Windows

```powershell
git pull --ff-only
.
un-roe-2022.cmd -Mode cycle -DebugConsole
```

Путь игры по умолчанию `G:\REsearch\Ring of Elysium-2022`. В консоли launcher напечатан каталог `runs/SESSION`. Открыть `client-debug-command.txt`, скопировать единственную команду. В игровой сцене Enter→ввести команду→Enter. Повторять до выстрела, после него и после R. После закрытия игры посмотреть `runs/SESSION/client-state.tsv`; `client-debug-command.txt` остаётся для воспроизведения. Getters слотов1/2, запас Citori10402/M410201, weather ID, доля суток и body-temperature. Несуществующий API/нечисловой результат записывается unavailable; ошибки Lua не выводят произвольные значения аккаунта.

Контекст: `research/builds/2022/recovery/112-host02/20261013T0424-public-getters/`, native hardware watch, выбранные TSV/server events/cleanup. Lua-консоль исполняется в клиенте. Прежние AddNpc/AddGoods stubs и GM1330 серверный запрос остаются прежними границами; HOST01/HOST03/HOST04 требуют нового совместимого provider/SDK/runtime binding trace. Снимки помогают проверять восстановленные сигналы, но не заменяют генератор матча.
