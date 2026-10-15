# ENV05: клиентское окружение и кандидаты влияния погоды2022

10.10.2026,2022 x64 0.2.989.0/map16010/SHA EXE `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`. Адресный разбор ресурсов и отдельная weather-последовательность в cold157 после ZONE08.

## Подтверждено

ClientTable/EnvrMapWeatherResourceTable связывает EDP_Day с LightSnow/Snow_Day_s,HeavySnow/Snow_Day_l,Blizzard/Blizzard_Day. Native setter140CD8000 получает13/15с,14/30с,27/1с,1/1с; final getter1413A032B и bounded resource names singleton143040750 подтверждают13→14→27→1. Новые PNG сняты **после20/35/5с**, соответственно выдержаны15/30/1с из EuIceLandTable:811–820. На heavy PNG видны частицы снега/смена видимости, на Blizzard метель; HP85 и+5°C остаются. Manual481 управляет только nativeweather контрольной последовательности; authoritative WorldState остаётся исходной all-safe стадией. Это изоляция окружения, не доказательство согласованной damage policy этих ad-hoc сообщений.

QSWeather XML содержит активные mWindElement/mWindConfig: Snow_Day_s angle/force0.5/0.5, Snow_Day_l иBlizzard1/1 (все:201). Blizzard включает lighting:85, lightingV1:141, viewdistance:72/far15000, snowparticles:237/count1500/wind9000 иветровые particles:244/count200/wind2300. Snow resources задают иные частицы/освещение; mWindDirection0/−1 вложен в wave config, не считать его автоматически вектором серверного движения. Некоторые rain/light элементы отключены: значение поля само по себе не означает активное воздействие. Полные выбранные атрибуты/SHA — resource-evidence.json. Динамически доказан выбор renderer resource, а не отдельный setter каждой wind/light float.

**Gameplay-кандидат найден отдельно:** AirDropTable ID2/model501:97–104 задаёт nWingForceMin/Max по weather:1→0..200,13/14→200..3000,26→3000..12200,27→10000..15000. Также mass316/gravity309800/dragA0.17/flyHeight301000. Это не только описание картинки: значения относятся к физическим силам дропа. Но их executable consumer/RNG/единицы и server применение ещё не подтверждены. Ветер не ограничивается snow particles как гипотеза; перенос этих чисел напрямую в полёт пули не обоснован.

## Не установлено

Исходная server wind simulation, аэродинамика дропа/планера, collision/LOS при тумане, wind/body temperature mapping. GUN08 native integrator140FC2430 использует drag/gravity; в выбранной функции нет отдельного weather wind input. Это локальная граница функции, а не доказательство отсутствия внешнего влияния при создании projectile.

Не изменялись renderer/resources/оригинальный клиент и правила peer для ветра. Array/string/enum bindings подтверждены по первичным XML и native weather snapshot; свет/растительность не выдаются за серверный расчёт.

Следующий адресный опыт: constructor/step дропа501 при weather1 и27 с одинаковым input, read-only hardware на consumer nWingForce, затем согласованная trajectory/654D. Эти поля переданы в DROP05 как новый первичный задел. Для original server нужен provider либо sanitized position/velocity/weather trace.

## Проверки

Weather hardware4points/code_patched=false/registers_written=false, source15/30/1с выдержаны. PNG просмотрены; cleanup157 timeout124, selectedSHA unchanged. До опыта312source/248portable/.NET passed; production weather code не менялся. ENV05 partial baseline; следующая по порядку DROP01.
