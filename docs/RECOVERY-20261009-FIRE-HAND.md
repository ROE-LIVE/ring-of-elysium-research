# NET05: fire/hand и новая граница после AUTH

09.10.2026, билд2022 x64 0.2.989.0, карта16010, SHA256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`. Наш peer, независимый Proton runtime, loopback namespace. [Evidence](../snapshots/recovery-20261009-fire-hand/evidence.json), [native application-id](../snapshots/recovery-20261009-fire-hand/cold88-application-sequences.json), [события](../snapshots/recovery-20261009-fire-hand/cold88-selected-events.json).

Три красные регрессии воспроизвели реальные ошибки peer: старый49e отменяет последующую timed reload; старый11da после вытеснения counter из64-элементного кеша расходует уже новый магазин; старыйhand после serial32 wrap возвращает прежний слот. Это новые TGCP рамки с прежним application-id; точный транспортный дубль уже отсекается receiver.

Первое BE32 C2S application,+0, — наблюдаемый общий sequence; opcode+8, payload+34. Предыдущий primary trace917 последовательных сообщений сохранён в отчёте NET05 от08.10; cold88 даёт дополнительные настоящие49e/49c/11da. Endpoint.accept_inventory_action теперь проверяет serial32 пяти известных действий: pickup/discard/reload/fire/hand. Равный/старый id получает только transportACK, без повторного effect или старого snapshot. Новый id проходит guard; fire дополнительно проверяет свой counter. Граница application-id остаётся у текущего транспорта, не переносится между AUTH.

Cold88: genuine pickup M4/40403/5.56×50, установка магазина, held2/held1. Hand0→2 начинает M4 reload; hand0→1 отменяет её. Следующий выбор M4 завершает40/10, firecounter1 даёт39/10. Citori firecounter2 даёт1/6; R→hand2 отменяет её reload. Inventory подтверждает1/6 и39/10, обе брони80/200. Ранние короткиеkey1/2 не дали запросов; эти попытки не являются проверкойhand.

C2S20 DROP→authenticated_idle_relay в16:41:05UTC сохраняет обе guns/parts/HP/world.started. Native после AUTH выдаёт меньшие application-id; свежая граница принимает hand/reload/fire. Citori reload→2/5 и firecounter3→1/5; M4 firecounter4→38/10. Финальный inventory PNG совпадает, mounted40403 и два вида ammo сохранены. World_start1; повторных эффектов и inventory_action_rejected в genuine пути0. Сохранённые shotcounter продолжаются1..4; сброс native firecounter этим опытом не проверялся.

3новые регрессии зелёные,234main/163kit tests и verify-only прошли. Проверка coalesced frames теперь ожидает границу последнего mutating fire101 после reload100; ammo-эффект прежний. Windows-комплект обновлён, реальный Windows-повтор отдельно. Клиент завершён своим timeout900с, exit124; выбранные3EXE/DLL SHA до/после совпали, inode независимые. Оригиналы не изменены.

NET05 baseline82.5%, без повышения этапов. Нативный старый application-id в новом зашифрованном envelope моделируется регрессиями, не вводом игрока; genuine/native newAUTH подтверждён отдельно. Vehicle/medical/rope и весь originalпротокол не объявляются идемпотентными. Следующая readyLOOT05: адресная потеря821/82b с надёжной доставкой.
