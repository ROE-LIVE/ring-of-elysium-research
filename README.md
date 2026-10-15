# Ring of Elysium Research — restoration context

[English](#english) | [Русский](#russian) · [Discord](https://discord.gg/pD2Bj5kAxk)

<a id="english"></a>

## English

### Demo use and disclaimer

- **This is an experimental demo intended only for personal home use and research.** It is not an official ROE service or a production-ready game server.
- You install, configure, run, and experiment with the project **entirely at your own risk**. You are responsible for your actions and for checking whether the project is suitable for your environment.
- The code, tools, and research materials are provided **as is, without warranties** of functionality, safety, reliability, or suitability for any particular purpose.
- **To the maximum extent permitted by applicable law, the repository owner, authors, maintainers, and contributors accept no liability** for damage, data loss, malfunctions, changes to system or network settings, or other consequences arising from use of, or inability to use, this project.

This notice does not exclude liability that cannot lawfully be excluded, and it does not change the licenses of third-party components.

Research context for contributors and new AI agents, as of **October 15, 2026**. The launcher, emulator, and gameplay regression tests live in [ring-of-elysium-local](https://github.com/ROE-LIVE/ring-of-elysium-local). This repository documents builds, architecture, protocol signals, and the mechanics recovery plan. It contains no game client, keys, large dumps, or private Git history. Most supporting reports and CSV descriptions are currently in Russian.

## Getting started

1. [Identify your build](docs/BUILDS.md). The main target is the **2022 x64 client**, root `Europa_Client.exe`, SHA-256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`. V99 and Steam 2018 use different addresses and structures.
2. Read the [current status](STATUS.md), [architecture](ARCHITECTURE.md), and [research method](METHOD.md).
3. Choose a stable task ID from [mechanics-2022.csv](docs/recovery/mechanics-2022.csv) and request its task card:

   ```bash
   python -B tools/tasks.py --task GUN07
   python -B tools/tasks.py --list
   python -B tools/tasks.py --next
   ```

   These commands only read the CSV; they do not launch the game. They require Python 3.11+ with no third-party dependencies. An empty ready queue means there is no ready task; it does not automatically unblock other tasks.

4. Consult the [signal registry](docs/signals-2022.csv) and [source index](SOURCE-INDEX.json). Historical paths in the CSV refer to **ROE_SERVER in the original workspace**. Some evidence is not included in this publication; a listed path does not guarantee that the file is available. Adapt historical commands to your own environment before running them.
5. Read [CONTRIBUTING.md](CONTRIBUTING.md) for contributions and [AGENT-START.md](AGENT-START.md) when handing a task to an AI agent.

## Contents and evidence

The repository includes **115 recovery tasks** with stable IDs and evidence-based stage estimates, **101 signal entries**, the textual agents-context reports on loot, host/debug paths, hits, bots, vehicles, and networking, plus hashes and selected evidence from the latest Windows test.

Historical reports retain their dates, so their proposed next steps may be outdated. Use `STATUS.md` for the current summary and primary data to establish facts. Progress percentages measure stages of the recovery plan, not the percentage of the original game restored.

Full historical snapshots are not included: some contain extracted game materials, machine-specific paths, and obsolete tools. If an experiment needs a missing file, request the **specific source** listed in the index or obtain it from your own client. A written report does not replace primary code or logs.

Selected hit-field and replay evidence is available under [evidence/windows-feedback-20261015](evidence/windows-feedback-20261015). The fixed local handshake files are documented in [LOCAL-HANDSHAKE](docs/LOCAL-HANDSHAKE.md) and distributed with the local game repository.

## Project scope and community

This work reconstructs an external scene peer. Strings such as `UseListenServer`, `Generic`, or `Console` do not prove that a working built-in host exists. The complete original server has not been recovered.

Join the [Discord community](https://discord.gg/pD2Bj5kAxk) to discuss findings and coordinate tests. To run the current game scenario, use [ring-of-elysium-local](https://github.com/ROE-LIVE/ring-of-elysium-local).

See [provenance](PROVENANCE.json), [rights](RIGHTS.md), and the [sharing checklist](SHARE-CHECK.md).

---

<a id="russian"></a>

## Русский

### Демонстрационное использование и отказ от ответственности

- **Это экспериментальный демонстрационный проект только для личного домашнего использования и исследований.** Он не является официальным сервисом ROE или готовым сервером для эксплуатации.
- Все действия по установке, настройке, запуску и исследованию вы выполняете **добровольно, на свой страх и риск**. Вы самостоятельно отвечаете за свои действия и проверку пригодности проекта для вашей системы.
- Код, инструменты и исследовательские материалы предоставляются **«как есть», без гарантий** работоспособности, безопасности, надёжности и пригодности для конкретных целей.
- **В максимально допустимой применимым законодательством степени владелец репозитория, авторы, сопровождающие и участники проекта не несут ответственности** за ущерб, потерю данных, сбои, изменения системных или сетевых настроек и другие последствия использования либо невозможности использования проекта.

Это уведомление не исключает ответственность, которую нельзя исключить по закону, и не меняет лицензии сторонних компонентов.

Полный текстовый контекст для исследователя или нового ИИ-агента. Состояние15.10.2026. Запуск, эмулятор и регрессии находятся в соседнем [ring-of-elysium-local](https://github.com/ROE-LIVE/ring-of-elysium-local); здесь — версии, архитектура, протокол и план механик. Клиента, ключей, больших дампов и приватной Git-истории нет.

## Порядок входа

1. [Идентифицировать билд](docs/BUILDS.md): основной2022 x64, корневой Europa_Client.exe, SHA-256 `2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18`. V99/Steam2018 имеют другие адреса и структуры.
2. Прочитать [текущее состояние](STATUS.md), [архитектуру](ARCHITECTURE.md) и [метод работы](METHOD.md).
3. Выбрать конкретный стабильный ID из [mechanics-2022.csv](docs/recovery/mechanics-2022.csv), получить карточку:

   ```bash
   python -B tools/tasks.py --task GUN07
   python -B tools/tasks.py --list
   python -B tools/tasks.py --next
   ```

   Команды только читают CSV и не запускают игру. Нужен Python3.11+ без сторонних зависимостей. Пустая очередь ready означает отсутствие готовой задачи; заблокированную задачу это автоматически не разрешает.

4. Открыть [CSV сигналов](docs/signals-2022.csv) и [источники](SOURCE-INDEX.json). Исторические пути в исходных CSV относятся к **ROE_SERVER исходного workspace**. Не все доказательства включены в эту компактную публикацию; наличие пути не подтверждает доступность файла. Исходные команды из CSV следует адаптировать к своему стенду.
5. Для участия использовать [CONTRIBUTING.md](CONTRIBUTING.md), для передачи агенту — [AGENT-START.md](AGENT-START.md).

## Что включено

115 задач восстановления со стабильными ID и оценкой этапов;101 строка сигналов; текстовые отчёты agents-context по луту, host/debug, попаданиям, ботам, транспорту и сетевым механизмам; хеши и выборка доказательств последнего Windows-теста. Старые docs сохраняются как датированные исследования: описание «следующей задачи» в них может устареть. Текущий STATUS имеет приоритет для сводки, первичные данные — для фактов.

Полные исторические snapshots не включены: часть содержит извлечённые игровые материалы, рабочие пути и устаревшие инструменты. Если для опыта нужен отсутствующий файл, запросите **конкретный** источник из индекса либо получите его самостоятельно из своего клиента. Не считайте текстовый отчёт заменой первичному коду или журналу.

Это реконструкция внешнего peer. Наличие строк UseListenServer/Generic/Console не доказывает работающий встроенный host. Исходный сервер целиком не найден. [Происхождение](PROVENANCE.json), [права](RIGHTS.md), [контроль состава](SHARE-CHECK.md).

Выбранные первичные материалы попаданий и replay: [evidence/windows-feedback-20261015](evidence/windows-feedback-20261015). Происхождение локальной пары — [LOCAL-HANDSHAKE](docs/LOCAL-HANDSHAKE.md).

## Сообщество

Присоединяйтесь к [Discord](https://discord.gg/pD2Bj5kAxk), чтобы обсудить исследования, согласовать проверки и поделиться результатами.
