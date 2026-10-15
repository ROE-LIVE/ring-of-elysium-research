# NET06: магазин после перезарядки и переподключения

2022 x64, корневой Europa_Client.exe0.2.989.0, база0x140000000, SHA256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`, map16010. Два холодных Proton-запуска, независимая runtime-копия, собственный loopback namespace. Это реконструированный peer.

Native361 воспроизвёл расхождение: Citori2/6→выстрел1/6→R→обрыв исходящего UDP20с через≈0.45с послеR→handoff. Сервер2/5, числовой HUD getter1/5. Native362 с исправлением: после такого же обрыва сервер/HUD2/5; следующий выстрел и обычнаяR возвращают2/4. Резерв расходуется один раз. Это UDP-контроль; прежние hardTCP357/358 остаются отдельными отрицательными опытами.

## Первичная цепочка

Сохранённая native-таблица `weapons-probe-20261005/weapon-handlers.json` связывает4A0/SCENE_MSGID_EQUIP_BULLET_SYNC с140E7DEC0. Архивный decoder140C37130 читает20байт `>QIII`: actorUID,slot,clip,counter. Handler получает decoded object с префиксом4байта: UID+4,slot+C,clip+10,counter+14. Эти смещения не являются wire offsets.

Четыре аппаратные точки361/362, без изменения кода/регистров, подтвердили:

- 140E7E04B: handler вызывает виртуальный метод оружия+1E0; цель140D032D0, EDX=clip/R8D=counter.
- 140D032D0: локальная ветка использует prediction object оружия+E58 и вызывает141323390; архивный ASM и свежие96байт начала совпадают по показанным инструкциям.
- 141323390: authoritative clip+20; список с sentinel+8/count+18. Узлы содержат counter+10,kind+14,predicted clip+18. В361 после выстрела counter1/kind0/clip1; после локальной reload counter0/kind1/clip2.
- 1413235F1: публикация через virtual+1D8, цель140D032C0. Свежий код: `mov DWORD PTR [rcx+90],edx; ret`. Это отображаемый магазин оружия+90.

После handoff старый snapshot4A0(clip1,counter0) публикует1 и сохраняет reload prediction. Финальный4A0(2,0) совпадает с predicted2, удаляет узел и обновляет authoritative2 **без вызова публикации**. Поэтому экран остаётся1. В362 следующий4A0(2,0) при пустой очереди публикует2. Эта последовательность зафиксирована аппаратными точками и числовыми getters; связь DLL receive→decoder по-прежнему не установлена.

## Исправление

`game_endpoint_probe_2022.py` помечает pending reload при однократном restore inventory. Когда штатный poll завершает именно эту reload и создаёт финальный4A0, peer добавляет **один новый application** с тем же актуальным магазином/counter0. Только существующий тот же UID/slot; отмена/замена не получает повтор. Ранний poll перед snapshot из отклонённого358 не возвращён. Повтор не вызывает reload, не расходует резерв, не создаёт предметы; transport duplicate с тем же id здесь не подходит.

Это ограниченное согласование нашего peer, оригинальная серверная политика пока неизвестна. Повтор для M4/пустого магазина/slot2, hardTCP20с и реальногоWindows ещё нужен. NET06 остаётсяbaseline70, проценты этапов не подняты.

## Воспроизведение и материалы

`research/builds/2022/recovery/011-net06/20261013-native-magazine/`: команды361/362, watch_magazine.py, primary-provenance.json, выбранные ASM, native-magazine.json и362/native-magazine.json, числовые *public-getters.tsv, public events, proxy control/events, evidence.json, cleanup. Данные AUTH/ключи/полные дампы не включены.

527source/483portable testsOK, verify-onlyOK, .NET8Release0warnings/0errors. Regression проверяет два финальных4A0, однократный расход/повторный heartbeat и отказ для заменённогоUID. Оба клиента остановлены; выбранные original/runtime EXE/DLL SHA совпали, независимость сохранена.

Windows: `git pull --ff-only`, затем `run-roe-2022.cmd -ReliableUDP -IdleHandoff -DebugConsole`. Обычный одиночный запуск не воспроизводит обрыв автоматически. Не требуется проверять фаервол или читать ключ; отчёт иclient-state.tsv сохраняются вruns/SESSION. Для контролируемого обрыва нужен отдельный согласованный стенд.
