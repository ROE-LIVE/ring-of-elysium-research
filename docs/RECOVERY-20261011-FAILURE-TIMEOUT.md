# Поражение, тайм-аут и итог при смене UDP-канала

EVAC08 baseline82.5; [первичный отчёт](../snapshots/recovery-evac08-20261011/report.md). Нативные2022 x64/map16010:174death UI,175alive UI,176два автоматических поражения50с,178два автоматических timeout120с. No survivors/Stats/ReturnLobby подтверждены изображениями. Первый timeout178 пережил12секунд C2S blackout и новый authenticated RELAY; gameplay не восстановлен.

177 — важный отрицательный контроль: deadline120 был верен, но oldchannel ответ не дошёл после новогоAUTH; NativeStats screenshot оказался обычнымHUD. Исправлен только frozen-result replay, ограниченный30с/identity/actor/IP/virtual destination. Игровые объекты/планы старой комнаты освобождаются; учёт фиксирован; новый поиск создаётновыймир. Нативный178 повтор доказалправильныйStats02:00/7M, затемвторой02:00/0M.

Сервер peer наш, original provider/награды/reason15 неизвестны. ICELAND_S.LUA10064 содержит2400, binding16010 не доказан; это выбранный локальный лимит. В Windows config/evacuation.json singleplayer_result_on_death=true/timeout2400, отключениеfalse/null; запуск `.\run-roe-2022.cmd -Mode cycle` (defaultwalk). Нужен Windows-повтор.

331source/281portabletests,verify0,.NET0warnings/errors. Оригинальные и независимыеruntime EXE/DLL174..178 неизменны;own процессы остановлены143. Следующий77DROP05: полёт/падение дропа;grounded501 не flight. Текущие очереди/проценты вdocs/recovery; процент — этапы плана.
