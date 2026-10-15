# NET04: входной stream/reorder,2022

09.10.2026, Proton GE11-7, карта16010, EXE x64 0.2.989.0 SHA2562dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18. Собственный namespace, независимый runtime. Cold78: research/builds/2022/host-console-20261007/recovery-net04-receiver-20261009-78.

## Реализация и первичные проверки

Opt-in `--reliable-udp` теперь содержит ReliableReceiver: непрерывный byte-stream/serial32, совпадающие перекрытия, отказ при конфликте без сдвигаACK, окно65535B/256несмежныхsegments. FrameStream выделяет frames3366 из нескольких UDP или нескольких frames в одном UDP; заголовок21..4096B, frame≤65535B. Это собственные пределы стенда, не оригинальные константы. При ошибке frame length stream явно отклоняется, произвольный resync не реализован.

Существующий gameplay handler выделен в process_frame без изменения его порядка. Legacy путь безфлага сохраняется. tools/udp_fault_proxy_2022.py — loopback proxy18001→endpoint18002. Сохраняет data/virtual ports/ACK/window/clock/extensions; при split изменяет толькоseq,PSH,packet_hash. Хеш primary: tools/roe_tgcp_2023.py, 0x141a5e700, header seq+4/ACK+8/dataoffset+12. Прокси не расшифровывает и не сохраняет payload.

220регрессий основного дерева прошли. Новые проверки: reverse+duplicate, gaps/overlap/conflict/wrap/window/segment cap, все разрезы TGCPframe, coalescedframes, неверные lengths; gameplay reload→fire сохраняет порядок.

## Положительный native контроль

Cold78 handshake/вход в зимнюю сцену прошли. Fire14:37:54.729: clip1/reserve6. Proxy reverse-001 выбрал C2Sframe data73B, seq1110545159, cut17: второй56Bфрагмент пришёл первым и дважды, первый17B — через50мс. Команда не задавалась proxy: endpoint после сборки зарегистрировал именно49c/application872 в14:37:56.149. ACK не перепрыгнул gap, затем подтвердил конец1110545232. Перезарядка amount1 завершилась14:37:57.972,clip2/reserve5, один effect. PNG23-receiver-after-reorder. Нет stream/receive/decrypt/frame errors; выбранные headers/events и proxy-events прилагаются.

## Отрицательный directional контроль

Затем proxy client→server DROP20с,154датаграммы; обратное направление пропускалось. После окна в14:39:59 новый TGCP1001/2001/AUTH успешно прошёл на новомtransport, затем7082/application4. Его выбранный35Bplaintext содержит actorUID22900292670268460 и payload00; это gameplay, AUTH/ключи не открывались.

Но handoff_pending/complete отсутствуют: старое5001 не принято, а resume_gameplay требует его marker. Поэтому новыйtransport room_sent не получает игрового состояния. В14:41:25 genuine11da зарегистрирован какapplication, но нет weapon_probe effect. PNG25 показывает всё ещёсцену/2/5: одного UI недостаточно для успеха. Другой orphanSYN transport исчерпал8повторов, udp_delivery_failed в14:40:12.878; этот event нельзя объявлять причиной отказа игровогоhandоff.

Факт: новыйAUTH/RELAY уже работают, переносмира не выполняется. Гипотеза для следующего опыта: bounded idle handoff послеAUTH+7082 с matchingactorUID/identity, уникальнымстарымpeer, неактивностью5..30с. Не переносить игрушечнуюsynthetic авторизацию вLAN.

NET04ready60%, NET06baseline70%, этапы не повышены. Исходное20сclient→server восстановление ещё не доказано. Свойtimeout24509 остановлен, exit143; proxy/ownclient завершены. EXE/двеDLL SHAдо/после совпадают, независимость подтверждена. Исторические captures/ключи/бинарники не передавалисьвGit.
