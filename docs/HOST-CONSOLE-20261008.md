# Host/console и исходные пресеты зимы:08.10.2026

**Обновление11:51UTC:** [MOVE02/ZONE02](MOVEZONE-20261008.md) уточняет старую гипотезу ниже.27/2b не требуются для застыванияUI; достаточенM наstage50. Nativeclock и движение подтверждены; финальныйUI не исправлен. Следующая ready-задача№6/ZONE02.

Исторический этап до нового адресного контроля: `ROE_SERVER/research/builds/2022/host-console-20261007/report.md` и README. Финальное состояние06:10UTC: основной полный календарь/эвакуация и отдельные отрицательные контроли завершены. EXE2022x64 0.2.989.0 SHA256`2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`, база140000000, карта16010. Ниже не предполагается совместимость адресов с V99/Steam2018.

## Главный результат

Встроенный host **не найден в рабочем виде**. Естественная загрузка`NewObj/EuGameServerTable`, setting0/netitemloopback, установила Host1. И Train1, и отдельный Train0 привели к HMODULE0 по owner143040778+140; GetProcAddressInitServerModule1437750c0→return1437750c6RAX0. Нулевой call не обходился.223обычных PE export-directory не дали InitServerModule/ExecConsoleCmd/RegisterMapManager; динамически защищённые exports этим не исключены. Нужен совместимый server provider/его loader или серверный toolchain. Имя DLL неизвестно; не предлагать ещё один mapID как замену отсутствующего engine.

В V99 аналогичный задел ранее не дал provider. Steam19.09.2018 располагает host-строками, но игровой вход не достигнут. Выбранные зимние координатные SFC V99 и2022 совпадают побайтно, поэтому возвращение к V99 не даёт само по себе исходной server logic.

## Реальная консоль

FileDriven/_GM_CONTROL_ естественно включает1430554f8. Parser140502520→event1418d53d0→Lua141003000, success R10B при1410030dd. Файловая Lua-команда собственного diagnostic script проверена; semicolon разбивается UI. Есть FOV/camera/Record/ForceGC/Soaking/getters. EnterGmCommand14189c080/140fd0e80/send140baf300→1330 — запрос серверу. AddNpc/AddGoods заглушки, ExportLootArchetype141818a60 no-op; generation metadata не содержит рабочие GenericStartLoot/Shrink/AirDrop. Это клиентские debug-инструменты, не админ-панель серверной симуляции.

## Что вытащили из первичных ресурсов

- Common.sfc1499,offset11043320:8313исходных точек,7915типов1/3/5,148транспортных, cm/Direction/archetype. SHA2187235d2dfa8adaee356428725bcb8087c6dd03a38a2e5af4de8298a0107f3c. Type→Ctrl H1 не доказана.
- TableBin443/2673: loot control/пулы; catalogueH1 из6843поддержанных предметов, AOI/остатки без respawn. Полный native RNG/квоты и неподдержанные оружия отсутствуют.
- Vehicle control2108/vehicles421: winterCtrl1001/1005, вероятности60/100, Jeep102 входит в пул. Проверена машина на исходной точке135009 (XML9,360453/543119/259497): F/38кмч/F.
- Plane790:10→16010/AI1; Shrink2621:82:1/10/20/30/40/50 по230/420/300/240/210/540с,35warnings. OUT/MID/IN selection engine не найден.
- Common3391:86regiongroups,50layer1/36layer2, внутренний XMLmap_id10019; равенство16010 не заявлять.
- EuIceLandTable Common3673: Safe1/Frozen27, light13/heavy14, сроки предупреждений. Native closed-region reaction сама выбираетBlizzard после481; server temperature curve отсутствует.
- AirDrop1280:97/map2071:100: ID2,5дропов/230с/model501/состав/силы/высота. Пять наземных контейнеров с бронёй/шлемами реализованы; полёт/placement/RNG не восстановлены, первая задержка230 — предположение.
- Shrink2621:637/PlaneBattleEnd696:4..6:PlaneEnter1205, расчёт полёта≈120с даёт hover при1:15до конца210-секундной стадии. Реконструкция создаёт готовый hover на собственной точке, не воспроизводит траекторию.

Original server Lua`DATA/SERVER/SCRIPTS/10064/ICELAND_S.LUA`, VFSid57396/offset5006417920, SHA8a3108c59f0732fbf44104ee44018172f7f3c621c897319b2996d24d9393a208: StartLoot115, selection47с308/StartShrink323, Official433/InitItems440, temperature459/AirDrop462/vehicles464.41вызов callback исполнен в liblua5.4 с явными собственными заглушками47Generic bindings. Это доказательство сценария вызовов, не запуск оригинального engine. Script10064→plane10120 binding не найден; designer aliases16007/08/09 не доказывают связь16010.

## Критическое исправление времени

4816 = **BE32индекс суток + BE32UNIX server seconds**, не scene ticks. Handler140d6b500→140cd80d0 вычитаетGetServerTime140d7d880/140d7d8a0: epoch+GetTickCount delta/1000. Первое lobby1f5f ставило архивный1698070099; setter140d7f190 допускает только initial_gate1/epoch0, поэтому поздний scene1f5f игнорировался.

Опция bridge`--local-server-clock` меняет только epoch первого lobby1f5f с корректной TCP-сборкой/перешифрованием; остальные кадры побайтно сохранены. Холодный опыт подтвердил первое1791432073, затем4816[8,1791432160]/native1791432159. TableBin95EnvrTimeTable:720мин/24неравных периода, сумма10000, scale4.32с/вес. MapTime140winter допускает7/8/15/16; UI7=Dawn,8=Morning,16=Evening подтверждены. Прежний вывод8=Dawn от неправильного ticks-пакета отвергнут.

Температура10d0(attr5,signedraw):500=5°C,−2000=−20°C. Начальные500 — собственная политика; исходные GenericStartInstanceTempe/RNG/cadence ещё не найденные. Не превращать предупреждения из таблицы в неподтверждённую native температурную формулу.

## Архитектура и проверка

Лобби.NET→TCP bridge→synthetic JOIN route→Python TGCP/UDP endpoint→нативный клиент2022. Выбранные SFC/VFS→собственные генераторы каталогов/расписания; native-клиент обрабатывает ground821, vehicle654b, containers3b61/3b63, weather481/4816/10d0. Его графика/физика не заменяют server raycast/AI/ownership.

Под Proton/GE11-7,Xvfb/NVIDIA3060, independent runtime, sudo unshareloopback проверены реальные pickup по исходной точке (5→15ammo), выгрузка/возврат без respawn, несколько ящиков/шлем/жилет, шесть стадий с исходными интервалами, естественная Blizzard-реакция, Jeep, подъём/посадка→газетаLOCAL. Завершение15с после посадки, HPfloor10/регионы/Stats остаются диагностическими. Новые модули: loot_catalog_2022,parcel_catalog_2022,environment_probe_2022,roe_clock_2022; Endpoint, WorldState и scene elapsed обновлены.137тестов прошли в заключительной проверке; шесть контрольных EXE/DLL совпали с прежними SHA.

Для повторения — README нового этапа и свободное имя run; profile требует подготовленных ресурсов/ключа/старых packet-fixtures в workspace. Внешний endpoint стал значительно ближе к воспроизводимой сессии; встроенный native host не стал«почти готов». Новый совместный профиль пока только Proton, Windows отдельно не проверен.

Следующая задача: восстановить расширенную инвентарную сериализацию/Type→Ctrl/квоты по первичным server данным, либо получить provider с47Generic implementations. Не повторять пустые hostCLI и не считать запуск Lua с заглушками доказательством оригинальной генерации.


V99: отдельный актуальный отчёт `ROE_SERVER/research/builds/v99/host-console-20261007/report.md` проверяет debug gate, два реестра, `.fcf` loader, Lua и no-op wrappers. Его HMODULE+0x138 и ExecConsoleCmd+0x148 равны0. Не переносить2022 +0x140/+0x150 на V99.


Уточнение05:54UTC: полный no-GM профиль показал6стадий,5дропов и UI2:46/6:47/7:43; после диагностического27/2b к тросу UIзастыл5:38. Native elapsed499.863→517.885 продолжает идти. GMне является необходимой причиной. F в этом повторе не дал native geton; не переносить успешную посадку из первого опыта на второй. Источник `no-gm-position-timer-followup.json`; position-only контроль выполняется отдельно.


Финальный position-only контроль: native elapsed73.243→91.267 приduration180, ноPNGсделаны доreceipt и послеконца нового таймера; UIпричинность не доказана. Decoder27=140c5a0e0; movement_status→141185ee0/140e88150. Приstatus<=2 записьactor+1e4=2 (141185f6f); смысл неизвестен. Следующий опыт:180с, PNG10/30с после27 и отдельно2b, аппаратный observer141185f5e и адресное полеactor+1e4. Не внедрятьenum3 как исправление без подтверждения.

Игровые/GDB процессы остановлены, proxy stopped/inspection_errors0.2022удалено10собственныхLua/metadata файлов и ранее2GM-маркера; V99удалено10fixtures по SHA.2022шесть иV99восемьконтрольныхфайлов неизменны. Windows-комплект не обновлялся этим этапом.
