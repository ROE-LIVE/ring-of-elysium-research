# 3B64 / 3E82: декодер → обработчик → инвентарь — 18.10.2026

**Корневой Europa_Client.exe2022 x64 0.2.989.0**, SHA256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`, Iceland16010. Это не xversion/V99. Native010/011 — независимый runtime/Proton, loopback. Только bounded code/selected table entry reads и аппаратные точки GDB; код/регистры клиента не менялись. Чтение `[rsp]` ограничено одним адресом возврата, не дампом стека.

## Подтверждённая цепочка

```text
application queue poll EXE:140BA9C80
  → wrapper140BB1770 (вызов140BA9DB5)
  → global decode dispatcher140CAA870 (вызов140BB1824)
  → group/union/body decoder
  → message dispatch140BAFC90 (вызов140BA9E10)
  → event dispatcher140BAF920 (вызов140BB0128)
  → callback registry140BAFBD0
  → callback3B64 / handler3E82
```

Промежуточные вызовы/выбранные switch-ветви сопоставлены статически; hardware подтверждены bodydecoder/его результат/callback/dispatcher return и delta decoder entry/handler/cache. Это путь после помещения прикладного сообщения в очередь; WinSock receive/TGCPdecrypt→queue в новом опыте не трассировался. **Найденные декодеры/обработчики находятся в EXE**, не в TenSafe/ProtocalHandler DLL. Остальные сообщения этим выводом не охвачены.

| Сообщение | Group / union dispatch | Body decoder | Обработчик/состояние |
|---|---|---|---|
|3B64 DROP_MSGID_RSP_PICK|140C6CB40 →140C6C730, case140C6C7BC|**140C69B00**|**140D629A0**; decoded command@0/dropID@4/qty@C/definition@11|
|3E82 item delta|140C4BD90 →140C4BC50, case140C4BCD5|**140C4BA10**|**140E162D0** →flag1 cache **140F48330** /user inventory+130|

Адреса — VA в базовом EXE0x140000000. Выбранные четыре байта таблиц140C6CAA4 и140C4BD6C дают caseRVA C6C7BC/C4BCD5. Чтение таблицы ограничено этими двумя элементами. Group dispatcher3B64 принимает диапазон3B61..3BC4; это не автоматически разобранные контракты всех соседних сигналов.

## Native010/011

Native010 настоящим drag/right-click подобрал M4(index190500/qty1/def10201),5.56(index190502/qty60/def30001), AK(index190501/qty1/def10202),7.62(index190503/qty60/def30002). Hardware callback3B64 получил соответствующие числа. Возврат callback140BAFBAD, возврат handler3E82 140BAFC77. Native010 также подтвердил delta count1/flag1/ownUID и cache-вызов140F48330, return140E16317. Матрица сообщений согласуется с серверными pickup, не только со статической регистрацией.

Native011 M4: body decoder140C69B00 вызван с reader_offset10/reader_length55; после возвратаresult0, drop190500/qty1/def10201, consumed55. Аргумент R8d=102 — внутренний параметр декодера, его полная семантика не установлена. Callback получил **тот же выходной объект**: callbackRDX+4 равен сохранённому decoderRCX. Затем аппаратно достигнут decoder3E82 140C4BA10 с reader_offset10/reader_length103, R8d135, return140C4BCE3. Это не сведения о размере всей TGCPрамки:55/103 относятся к reader данного прикладного сообщения.

Важно: первое слово callback содержит0x3B64, **не error**. Первый скрипт010 ошибочно печатал подписьerror=15204; исходный лог сохранён, подпись воспроизводящего скрипта исправлена, повторный011 явно показываетdecoded_command=3b64. Body decoder получает область после этого внутреннего четырёхбайтного discriminator, поэтому его drop@0/qty@8/definition@D соответствуют callback offsets+4/+C/+11.

Первичные материалы: `research/builds/2022/recovery/022-inv02/20261018T1230-pick-handler/`: `native010-{pick-chain,upstream,loop}.log`, `native011-decode-chain.log`, соответствующие `.gdb`, выбранные disassembly `.txt`, `selected-switch-entries.json`, filtered gameplay events и cleanup. `.pdata` содержит фрагмент140BAFDA7 с продолжением, это **не вход функции**; настоящий prologue140BAFC90 проверен отдельно. Нельзя определять все функции только по одному диапазону unwind.

## Что остаётся

[Flag0 отрицательный опыт](INVENTORY-BRANCH-CONTROL-20261018.md) сохраняет силу, flag1 не меняется. Периодическая задержка3D изображений оружия не исправлена. Теперь следующий адресный шаг — consumer/UI-model notification после cache/update на успешном и задержанном pickup с измерением времени; повторять слепые5FB или flag0 не следует. Это две подтверждённые цепочки, не полный SDK и не восстановленный исходный сервер.
