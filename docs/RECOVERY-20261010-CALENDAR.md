# №54/ZONE01 и№55/ZONE03: полный календарь2022 после position fix

EXE2022 x64 0.2.989.0, SHA2dca9b1e…6ba18, winter16010. Cold146 в независимом runtime/Proton, loopback namespace; no Docker/Ghidra/моделей. Основной источник календаря: SFC/TableBin ordinal2621 offset выбранного AI1, SHA09eefa8b…04fa7c; `DATA/TABLE/SHRINKMACHINETABLE.XML:82+`. PlaneTable_default row10 связывает16010 сAI1. Это источник чисел расписания, не найденный host.

**Проверено без ускорения:** стадии1/10/20/30/40/50 с durations230/420/300/240/210/540 и35warnings. Старт selection47+inventory3 учитывается elapsed50 вstage1; peer world начинает свой отсчёт один раз. Последняя стадия540сек выдержана полностью, UI финал0:00. stage lateness максимум0.738сек; каждый новый deadline вычисляется от world.started, а не от фактической выдачи предыдущей стадии. Повторный heartbeat не запускает старые стадии вновь.

**Потеря:** fault proxy C2S drop20сек воstage20; новый authenticated idle relay появился16:51:25, world_position365100/544000/259107, HP1000, stage_index3, warning_index16. Resume481 stage20 elapsed82.321907/remaining217.678093; последующий UI3:02 согласован с исходным дедлайном. world_start1, шесть примененийstage,35warnings всего — без нового календаря послеhandoff.

**Native UI:** `146-stage10-map.png` blue/6:24; `146-stage10-yellow-open.png` фактически уже red/1:47 (имя не является доказательством yellow); `146-stage30-map.png`,stage40 иstage50 показывают всё более закрытую карту; `146-calendar-final-zero.png` полная black и0:00. Yellow в данном полном прогоне пропущен снимком; прежнее подтверждение не расширяем новым именемPNG. Списки регионов собственные, вложенные, не исходный RNG. Серверные closed sets монотонны; защита новых native_fast configs отклоняет reopening/future outside safe. Kind1warnings не меняют closed set. ПолныйUI scan каждого пикселя/Windows/new multiplayer отсутствуют.

**Новый ресурсный факт:** прежняя4196002-byte grid SHAcfec…2ceb — `REGIONMASKTEXTURE.BIN`, а не fast index. Точный position lookup исследован отдельно в№56, `recovery/056-zone04/20261010T1646-region/`. Не выдаём UI-маску за authoritative границу.

**Проверки:**11world tests и полный source suite307/portable240 после изменения fast index. Original/runtime выбранные EXE/DLLSHA совпадают; cold146 остановлен, namespace завершён. Evidence содержит только выбранные игровые события, без AUTH/секретов/полных дампов. ИсточникиPNG вrun, JSONcalendar-public-events/evidence/cleanup-hashes рядом.

ZONE01 иZONE03 сохраняют baseline90% (действующий календарь/UI; новые Windows/исходный RNG отдельно). Следующий№56/ZONE04: native fast regions, live HP/death контроль.
