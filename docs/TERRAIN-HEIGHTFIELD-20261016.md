# Исходная поверхность зимней карты2022: Native018/019

Корневой EXE2022 x64 SHA256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`, карта16010. Независимый runtime/Proton/loopback. Это найденные данные и точечный reader, не автономный исходный host и не замена всей коллизии.

## От файла до живой физики

`DATA/WORLD/EU_ICELAND_4096/SERVERDATA/RIGIDTERRAINLINUX.PXBIN` и соседний `RIGIDTERRAIN_WIN64.PXBIN`:17848756байт, SEBD, версияLE32@4=`03030400` (PhysX3.3.4.0), platform@16 L_64/W_64. Object count@32=52; manifest count@48=52, записи по8байт; импортов нет. Первый известный probe по SEBD —140A27950. Код десериализации найден **в EXE**, а не по экспортированному удобному API DLL:142200150, проверенные error-string refs14220021B/78D/7CC. Игровой loader140A27D8D вызывает его с128-byte aligned buffer, registry из global14302A898+18 и externalRefs0.

Native018/019 при входе в Training действительно выполнили этот вызов: W_64,52объекта, ненулевой collection. Getter count находится в `PhysX3Common_x64.dll` RVA DDA0 (collection+74), getter объекта DDB0 (array+48,index*16). Типы подтверждены constant type-name getters, а не догадкой по ID:

| TypeID | Количество | Native имя |
| --- | ---: | --- |
| 1 | 1 | PxHeightField |
| 8 | 49 | PxMaterial |
| 7 | 1 | PxShape |
| 6 | 1 | PxRigidStatic |

Heightfield:2112×2112 samples, по4байта `<hBB` (signed height, два material/flag bytes). Native getter rows/columns —Common RVA18F50/18F40, object+20/+24; sample pointer+38. Источник object data начинается с1952, samples с6464; размеры массивов17842176байт. Native019 shape geometry6: heightScale5,340657711029053, row/columnScale200см, local pose identity. Actor quaternion(.5,.5,.5,.5), translation192000/192000/175002,671875: localX→worldY, localY→Z, localZ→X. Эти параметры независимо совпали с полями **обоих исходных** PXBIN.

SHA Win64 `4e28f2c6654fb8643821a612ce102719f3e70150f0f730d9a42bcb43d882097c`; Linux `8332fe282b7949acbe717b256638543c6aa32398744b84cfdfe25d7735467d6f`. Полные массивы samples совпадают по SHA `e290b7fdde5a43215c4999142829db13858c2102c0ad20198bcdb8373c1e2ed1`; вычислялся потоковый хеш ресурсов, геометрия/массив в Git не копируется. Linux collection не исполнялась; её высоты прочитаны отдельно.

## Точечный reader без SDK

`tools/probe_iceland_heightfield_2022.py` проверяет SHA/размер/версию известного файла, затем для одной XY читает16байт samples, применяет диагональный флаг и выдаёт terrain_z/normal/material_pair. Используется **треугольная**, не билинейная интерполяция. Исходные функции Common RVA18B80/18C41; выбор клетки BDC50. Двенадцать синтетических контролей эмуляции исходного DLL-кода совпали с Python до0,00001 единицы raw height. Шесть независимых unit-тестов обходятся без игровых ресурсов.

Две настоящие Native019 точки Snow_Hard802 совпали с reader Linux-файла:

| Native XYZ, см | Reader Z | Ошибка Z, см |
| --- | ---: | ---: |
| 370481,0625 /544375,5 /258861,375 | 258861,382179 | 0,007179 |
| 370401,15625 /544473,375 /258874,796875 | 258874,795575 | 0,001300 |

Нормали также совпали в точности float; material_pair42/42. Это два разных соседних cell, не проверка каждого участка карты. Первый выстрел Native019 попал в Rock305 и из проверки высот исключён.

Пример **после извлечения собственного ресурса** (PXBIN не входит в репозиторий):

```powershell
python tools/probe_iceland_heightfield_2022.py --terrain-file "D:\ROE-extracted\DATA\WORLD\EU_ICELAND_4096\SERVERDATA\RIGIDTERRAINLINUX.PXBIN" --x 370481.0625 --y 544375.5
```

Нужен Python3.11+, дополнительные SDK/библиотеки для reader не нужны. Обрабатывается только подтверждённый ресурс2022; файл и клиент не меняются. CLI не встраивается автоматически в launcher.

## Применение и границы

Следующий полезный опыт — использовать terrain height как нижнюю поверхность для нового наземного loot/NPC участка и сравнить с клиентской коллизией. **Не заменять им верхние этажи/полы/мосты/камни и не присваивать actor Z напрямую:** смещение капсулы/ступени/динамические объекты отдельно. Обнаруженный hole127 только помечается possible_hole; выбор отверстия/материала конкретного треугольника не является готовым server raycast. Выход за внутреннюю область reader отвергает вместо native clamp. Terrain LOS, все материалы/holes, static-object transforms, навигация, origin authority и полный parser binary collection ещё не реализованы.

Отрицательные результаты сохранены: предположение count+38 было неверным; доказанный getter+74 исправил его. Чтение старого object pointer после продолжения018 дало EIO; поля019 сняты на остановке возврата, не используются как вечные адреса.

Доказательства: исходный `research/builds/2022/recovery/043-gun06/20261016T0300-native-obstacle/`: native019-terrain-metadata.json, terrain-source-poses.json, terrain-source-sample-match.json, heightfield-native-validation.json, selected header/manifest/code refs. В передаваемом research сохранены только выбранные параметры и числовые проверки, без sample array/ресурсов/дампов.

Дополнительный контроль исходного массива:4,460,544samples, все tessellation flags=0; material127 не встретился. Для этого варианта reader также возвращает face_index/material_index; оба native face7440249/7444472 совпали. Это не проверка всех карт/динамических отверстий. Для неустановленного tessellation1 face mapping reader оставляетnull.
