# MP01 — командный roster и границы режима,12.10.2026

2022 x64 0.2.989.0/map16010, SHA2562dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18. Read-only selectedcode независимого Proton317, без записи в процесс.

MATCHCFG.LUA:130..145 содержит Training16014/squad4 и single1.215..238 задаёт defaultsingle1/duo2/squad4 и override16021/squad3. Привязка исторической зимы16010 к действующему режиму в этом участке отсутствует. Выбор кнопкиTraining и замена адреса/карты нашим bridge не доказывают squad-зимнюю сессию. TEAMCFG/HUD дают UI, не authoritative damage policy.

Коллеги PACKET-DEFINITIONS.md:2580..2584 связывают0D70 с decoder140A14BA0/handler140C22F20, TEAMMEMBERstride303. Его адреса не совпадают с текущей распакованной картой нашего EXE: read-only фрагмент140C22F20 сейчас начинается внутри byte-reader, не командного handler;140A14BA0 не даёт заявленного decoder. Поэтому версия входного отчёта не считается установленной по словуx64, адреса не переносим автоматически.

Первичный сохранённый active-dispatch-tables.json этого2022 изautonomous-20261004: override0D70→140E58B50. В native317 подтверждён code140E58B50: аргументrdx+4 — структура тела; count[+0], члены начинаются+4, цикл шагает0x12F=303. Командный идентификатор берётся изструктуры+0x12F4=4852, резерв по16записей. Handler ищет собственный UID, связываетteam-manager+0xC8 и список+0xB8, затем140E57090. Это структура после unpacking, **не фиксированная длина wireпакета**. Точный wiredecoder/countlimits/переменные поляTEAMMEMBER ещё не подтверждены. Минимальный старый lobbyteam_body изroe_team_2022.py относится другому сообщению и не заменяет0D70.

104B/TEAMMATE_ATTACKED имеет имя во внешнемOpcodeDump/дваUID в отчёте коллеги; отсутствие nativehandler там не означает отсутствия serverfriendlyfire. Наличие уведомления не доказывает damageenabled/disabled. Исходный teamdamage, down/revive остаются неизвестны; код запрета/разрешения урона союзнику не добавлен. Общая MP03-комната пока не назначает доказанные команды.

MP01 external_blocked20% этапов(1/1/1/0/0/0). Нужен sanitized первичный обмен этогоEXE в winterduo/squad: выбранный mode/map,0D70/roster и парный shot/hit/HP при союзнике/противнике; AUTH/ключи не нужны. Альтернатива — точный decoder0D70 и executableauthoritative policy поteamID. Запуск двух наших free-for-all клиентов безпервичнойпривязки команды этого не установит.

Следующий OPS02 требует нового Windows11прогона, его нельзя заменитьProton. Затем OPS04: typedactions должны менять WorldState/WeaponState/ActorState, а не только отправлять готовый пакет.
