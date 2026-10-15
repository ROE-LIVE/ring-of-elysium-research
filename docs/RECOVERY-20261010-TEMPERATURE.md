# ENV03 — signed температура и независимость часов

Билд2022 x64 0.2.989.0, map16010; EXE SHA2562dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18. Run research/builds/2022/host-console-20261007/recovery-env03-temperature-20261010-155, 10 октября22:43–22:46UTC; own loopback/Proton, независимыйruntime.

Пакет10D0 — attrBE32=5 и signedint32BE температура, единица0.01°C. Проверены500→+5°C,0→0°C,−2000→−20°C,−5000→−50°C. Ноль/минус20 при ясной погоде и минус50/плюс5 при метели видны в155-*.png. Метель вызвана только481 с current-safe14/future-safe14 при положении24.10D0 сам не переключает погоду. HP-floor1000 делает этот опыт непригодным для вывода об уроне холода.

Часы наблюдались four hardware points script060-env01/clock_watch_gdb.py:140CD80D0/140CD82FD/140CD86F1/1413A032B. В период155 нет новых вызовов4816 consumer; start_hour8,baseline_seconds,weight_scale,day_scale иmain_period неизменны. Все PNG сохраняютMorning. То есть изменение температуры не переинициализирует часы в данном опыте. Данные clock-observer.json,temperature-actions.json.

Два20с обрыва client→server. Первый послеtemp500 дал сохранение5°C, но значение совпадало сdefault и не доказывало отсутствие сброса. Поэтому отдельно установили0, дождались155-zero-before-second-handoff.png, повторили20с drop, после подтверждённого gameplay_handoff_complete получили155-zero-after-second-handoff.png с0°C/Morning. environment_initialized вpeer ровноодин, handoff_complete два; selected-events.json. Проверка отрицательного сброса отделена от первого неоднозначного контроля.

При handoff собственный календарьworld1200с/all-safe восстановил ясную погоду вместо вручную заданной481 метели. Это ожидаемое восстановление конфигурацииWorldState, а не доказательство сохранения произвольных live команд погоды. Температура сохранилась при том же клиентском процессе; новый cold reconnect/новый игрок не проверены.

Windows materialize/bootstrap получили -TemperatureRaw−5000..500; default500. Тело10D0 остаётсяsigned, час/epochне меняются. Пример .\run-roe-2022.cmd -Mode cycle -StartHour7 -TemperatureRaw -2000 -ReliableUDP -IdleHandoff. Это фиксированное значение для контроля; originalтемпературнаякривая и физиология не восстановлены.245 переносимых тестов иverify-only прошли;C# неизменен после предыдущей успешной.NETсборки. Адресная остановка143, выбранныеEXE/DLL хеши неизменны (cleanup.json). НовыйWindowsповтор отдельно.

СледующийENV04: первичныеColdDamageTable/ColdPowerTable различаютHP иcold reserve; OutSideTempeTable содержит толькоmap16011 иошибочный closingtag, нельзя прикладывать его к16010. AI1 ShrinkMachine имееттемпературныепараметры, нониисполняемыйserverprovider, ниoriginalcadence пока не установлены.
