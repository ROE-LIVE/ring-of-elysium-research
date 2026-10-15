# Транспорт и спорные сетевые выводы

Различать lobby TPDU, игровой UDP3366/TGCP, наружную датаграмму, расшифрованное приложение и native структуру. Клиентский игровой 4013 использует проверенный 34-байтовый BE header; server message —10-байтовый header. Внешний RFC с 8-байтовым LE header/body+10 может описывать другой тракт и не заменяет рабочий парсер.

## DLL и EXE LWIP

У ProtocalHandler_x64.dll V99 и 2022 SHA целого файла отличается, но **.text833536 байт при RVA1000 совпадает**: SHA256 `8ada98a8880f0acb0a46e7a1dce29238d566938cf32f0d36fdb48acd9163f04e`. DLL preferred base180000000: recvfrom `180048184` в функции `180047f80`, sendto `180048a2a` в `1800486f0`, dispatch vtable+18 по `18004797d`.

Это общий DLL код, а не доказательство, что игровой LWIP3366 находится в DLL. Динамика V99 доказала EXE LWIP/TCP PCB поверх UDP. Полную обработку потерь и перестановок собственный peer не повторяет.

## Четыре байта extra header

В 2022 serializer `141a48d20` третий байт выбирает union через `141a47c30`; для version10 далее пишутся count и count×BE16 длин. Прототип batch задаёт extra[3]=N−1 и BE16 длины предшествующих сообщений. Гипотеза «средние байты — неочищенный мусор» не подтверждена; происхождение второго байта не прослежено. Эти VA нельзя переносить на V99 без сверки.

## Вопрос об античите

В OpcodeDump2666 уникальных кодов найдены `0x3783 ANTIBOT_MSGID_DPDATA`, `0x37AA ANTISAFE_MSGID_EVENT_NOTICE`, `0x37AB ANTISAFE_MSGID_STAT_NOTICE`. Ни decimal3879, ни hex3879 не найден. Pack2022 `140c67ef0` обрабатывает 3783: ограниченная U32 length≤65535 и byte array. Внутренняя структура и маршрут в TerSafe/tensafe не доказаны. Anti-bot название не означает игровых NPC.

## Применимость внешних материалов

PACKET-DEFINITIONS.md, ROE_Protocol и external/v99 полезны как кандидаты. Их EXE адреса не совпали в выбранных проверках с нашими EXE; нужен исходный SHA. Пометка no-native-handler не доказывает отсутствия обработки: живые V99 таблицы имеют 821/4A0 и другие handlers; схемы 11DA/821 также требуют сверки. Общие DLL точки переносимы только после сравнения секции и окон.

Инструменты: `tools/roe_protocol_2022.py`, `roe_tgcp_2023.py`, `roe_scene_2023.py`, `roe_room_2023.py`; `server/directory/game_endpoint_probe_2022.py`; V99 `hosting-route-20261006/public_game_codec.py`, `lwip_preset_peer.py`; переносимый `roe-server/server/v99_remote`. Название инструмента 2023 само по себе не определяет билд сообщения.

Источники: V99 external-network-review/report.md;2022 message-structure/report.md; `research/external/shy_roe_caps/analysis/hour-20261004/functions/141a48d20.asm`;2022 iceland outcome/report/schema. Секретные handshake bodies и ключи не включены.
