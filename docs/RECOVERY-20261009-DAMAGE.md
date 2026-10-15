# Исходные параметры урона2022,09.10.2026

[Первичный отчёт](../snapshots/recovery-gun07-damage-20261009/report.md), [проверки и отрицательные результаты](../snapshots/recovery-gun07-damage-20261009/evidence.json). GUN07ready12.5% этапов: data1 уже существовал, новые параметры не увеличивают этап. Формула не восстановлена.

A89TableBin: nDamage M4=400,AK47=470,Citori=260,R700=1200,USP45=410; nDamageMin/nHitHeadRatio, speeds/cross, armorDEF/durable выбраны прямоизSFC. Consumer коэффициентов неизвестен; не подменять 130 множителем1.3/2.3 бездоказательства.

11DD106Bserializer140c3fb70←140c6e2e0(return140c70188)←140ca8a10(return140ca8b06)←140bb1350(return140bb13e5). HardwareGDB прочитал отдельные returnPC по известнымprologue, `.text`фрагменты bounded. Последний trace выше остановился наWineSIGSEGV до точки; новыхфактовнет,clientоставалсяживдоcleanup. Headshot83 гипотеза не подтверждена:4highM4hit+161..166см дали164/0, близкийстарыйhit142смдал650/1. Семантика78/83неустановлена.

Peerжурнал теперь хранит gun_definition принятогоfire, hit_tag62/hit_field71/hit_field78/hit_flag83/hit_field100. Cold73 реальныйM4 дваhit1000→900→800, nativecache800/800/1000. Это прежний учебныйdamage100raw,неоригинальный.202/130тестов,verify-only16loot,.NET8Release0warnings/errors,3SHAравныинезависимы,опыты124/143завершены. Windowsновойтелеметрииотдельно; базовыеоружейныефункцииподтвердилпользовательбезточногокоммита/лога.

Следующийопыт: producertraceвыше140bb1350,заполнение+78/+83,consumer nDamage/nHitHeadRatio. Нужен оригинальный расчёт либо originalhurt capture сknown weapon/hit-zone/armor/range/HPдо/после. Отправка собственного учебногоHP не подтверждает исходнуюформулу.

[Уточнение учёта этапов](../snapshots/recovery-gun07-accounting-20261009/stage-accounting.md): исходный снимок отчёта содержит ошибочную оценку20%; текущий CSV сохраняет12.5%, wire-семантика head/body ещё не установлена.
