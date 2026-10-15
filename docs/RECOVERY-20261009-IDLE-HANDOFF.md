# NET06: authenticated idle handoff,2022

09.10.2026, x64 0.2.989.0, зимняя карта16010. EXE SHA2562dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18. Proton GE11-7, независимый runtime, loopback namespace. Peer наш; исходный host не восстановлен.

## Исправления

`--idle-handoff` (требует`--reliable-udp`) разрешает перенос после новогоsynthetic AUTH иRELАY7082/payload00: тотжеidentity/actorUID, одинживой старыйpeer, неактивность5..30с. UID — C2Sheader+22, payload+34. НаAUTH без5001 перенос ещё не разрешён. Завершённаяэвакуация/другойUID/identity/слишкомсвежий илистарый/неоднозначныйpeer отклоняются. Старый транспорт retired, ledger очищен; ключ/frame/stream counters нового транспорта сохраняются. Инвентарь и мир переносятся однократно.

Для профиля безWorldState сохраняется последняя принятая2a-позиция; decoder140c56410. Восстановление27: decoder140c5a0e0/handler141185ee0. ПустойMOVE не придумывает позицию. Вcold80 запас sender увеличен с8до15повторов, maxinterval2с: собственнаяполитика, не оригинальнаяконстанта; 20сокно не должно исчерпать sender раньше окончанияпотери. Признак retry_limit уorphanSYN не считать отказом игрового транспорта.

## Cold79: инвентарь, C2S20с

Run: host-console-20261007/recovery-net06-idle-20261009-79. Native fullbag225/225, M4+магазин40403,5.56=50,12ga=160. Настоящийsplit12: reserve148+ground12+46; payload15B3e80/tag2 записан отдельно, PNG29 подтверждаетввод12. Hand2 автоматически началreload M4 до потери — это не отдельный послевосстановительныйreload.

DROP C2S14:59:35.741..14:59:55.741,32датаграммы. В14:59:56.099 `authenticated_idle_relay`, idle21.3447с; инвентарь/обаgun перенесены. Pendingreload применён одинразamount40: M440/10, Citori2/148, mountedmag, ground46/12. ПозднийR15:01:42 далamount0. Pickup70001/12 в15:03:18→reserve160,ground12удалён; fireM4→39/10, тотжеUID1e00000100000001. PNG34/36/38 иselected-events. Cold78 безфлага оставилновыйAUTH/7082 безигровогосостояния иfireeffect — отдельныйотрицательныйконтроль.

## Cold80: позиция/HP/оба направления

Run: recovery-net06-world-stage-20261009-80. Принятая позиция(365380,544000,259094), на280см отстарта. C2S20с далidlehandoff15:17:07,HP1000 ипозиция27 сохранены. S2C20с15:18:54.974..15:19:14.974,480датаграмм включаяretries: explicit5001→handoff15:19:18.069. В обоихпереносах точнототже world.started28298.649767531, stage_index2; world_startодин. PendingCitorireloadamount1 послеhandoff→2/5; следующийfire→1/5, движениеработает.

Планируемый переходстадииcold80 пропущен: DROP начался послеstage10. Его не засчитываем заcross-stage. HPfloor1000 исключаетпобочныйурон; исходныйdamage этим опытом не проверен.

## Cold81: реальный переход стадии в потерях

Run: recovery-net06-auto-stage-20261009-81. Scheduler targetworld+80с, отклонение0.1905с; DROP15:28:47.022..15:29:07.022,32датаграммы, перекрылstage10 приworld+90с. Handoff15:29:08.098 соstage_index1; затем единственныйstage10 сelapsed101.494с. World_startодин,HP1000,fireпосле работает. Движение20 иM21 сделаны во времяDROP, хотя label21 содержитbefore: не считатьихпредварительной принятой позицией; возвращена стартоваясервернаяпозиция.

Новыйпробел: WorldState.poll выдаёт отложеннуюстадию сelapsed_seconds0 изfixedpayload. Native140e74030 восстанавливает еёначало какclock−elapsed; срокможетсдвинуться на задержкуpoll. СледующийконтрольZONE02: корректироватьelapsed на lateness и снятьnativeсчётчик в заданноеworldвремя. Календарь90/60с собственный, не оригинальный.

226tests основного дерева/150Windows-kit проходят, verify-only сдвумяфлагами успешен. Windowsкомандаoptional: `.\run-roe-2022.cmd -WeaponProfile m4 -ReliableUDP -IdleHandoff`; новогоnativeWindowsподтверждениянет. NET06baseline70/NET04baseline60 не объявленыdone: seated/rope/combinedfault/Windows иflow-control остаются. Все3ownrunner остановленыexit143; SHAEXE/двухDLL совпадают, active_clients пуст. Секреты/сырыеAUTH/игровыеbinaryвGitне включаются.
