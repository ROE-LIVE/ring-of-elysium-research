"""Выдать поручение по ID/номерам CSV; проверить входы без запуска игры и сервисов."""

import argparse
import hashlib
import importlib.util
from pathlib import Path
import shutil

from recovery_status import ROOT, load_plan


EXPECTED_SHA = "2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18"
HOST = "research/builds/2022/host-console-20261007"


def select_tasks(rows, selectors):
    by_id = {row["id"]: row for row in rows}
    by_number = {int(row["sequence"]): row for row in rows}
    selected = {}
    for selector in selectors:
        for item in selector.split(","):
            item = item.strip()
            if item in by_id:
                matches = [by_id[item]]
            elif item.isdigit() and int(item) in by_number:
                matches = [by_number[int(item)]]
            elif "-" in item:
                limits = item.split("-")
                if len(limits) != 2 or not all(value.isdigit() for value in limits):
                    raise ValueError(f"Неверный диапазон: {item}")
                low, high = map(int, limits)
                if not 1 <= low <= high <= len(rows):
                    raise ValueError(f"Диапазон вне1..{len(rows)}: {item}")
                matches = [by_number[number] for number in range(low, high + 1)]
            else:
                raise ValueError(f"Неизвестная задача: {item}")
            for row in matches:
                selected[row["id"]] = row
    return sorted(selected.values(), key=lambda row: int(row["sequence"]))


def file_check(root, relative):
    path = root / relative
    return f"{'OK' if path.is_file() else 'MISSING'} file {relative}"


def preflight(root, selected):
    """Проверяет выбранные материалы и стенд; ключ не открывает, команды не исполняет."""
    checks = []
    references = dict.fromkeys(ref for row in selected for key in ("agent_context", "sources", "evidence", "edit_targets")
                               for ref in row[key].split("|") if ref)
    for reference in references:
        checks.append(file_check(root, reference))
    live_profiles = {row["run_profile"] for row in selected} - {"resources", "manual", "windows", "lan"}
    if live_profiles:
        required = [
            "runtime/client/Europa_Client.exe", "runtime/client/SFC/Common.sfc",
            "runtime/client/SFC/TableBin.sfc", "runtime/client/data_org_dyn.sfc",
            "runtime/client/Cache/Data/world/EU_IceLand_4096/EU_IceLand_4096.sfc",
            "runtime/proton-2022/pfx/system.reg", "tools/proton/GE-Proton11-7-x86_64/proton",
            "tools/vendor/dotnet/dotnet", "server/lobby/LobbyEmulator.Sdk/bin/Release/net8.0/LobbyEmulator.dll",
            "research/builds/2022/wine-preflight-20261004/nvidia_icd.json",
            "research/builds/2022/session-06-review/candidate-001.key",
            HOST + "/run_trial.py", HOST + "/run.sh",
            "research/builds/2022/iceland-gameplay-20261006/join-iceland16010.json",
            "research/builds/2022/iceland-gameplay-20261006/room-iceland16010.bin",
            "research/builds/2022/winter-kit-loot-20261007/scene-grounded.json",
            HOST + "/environment-winter-hour8-5c.json",
            "research/builds/2022/winter-kit-loot-20261007/preset-snowboard.json",
        ]
        if "world" in live_profiles:
            required.append(HOST + "/world-countdown-control.json")
        if "loot" in live_profiles or "full" in live_profiles:
            required.append(HOST + "/catalog-original-winter-h1.json")
        if "combat" in live_profiles:
            required.append("research/builds/2022/iceland-gameplay-20261006/actor-bot-basic.json")
        if "full" in live_profiles:
            required.extend([HOST + "/scene-combined-source-cadence.json", HOST + "/world-source-ai1-rebased.json",
                             HOST + "/parcels-grounded-multi-winter.json",
                             "research/builds/2022/iceland-gameplay-20261006/evac-ui-bridge-no-grace-20261007.json"])
        checks.extend(file_check(root, relative) for relative in required)
        commands = ["sudo", "unshare", "ip", "xvfb-run", "xdotool", "xwininfo"]
        if any(row["id"] in {"MOVE02", "ZONE02"} for row in selected):
            commands.append("gdb")
        for command in commands:
            checks.append(f"{'OK' if shutil.which(command) else 'MISSING'} executable {command}")
        # TGCP имеет собственный bounded LZ4 decoder; внешняя библиотека не нужна runner.
        checks.append("INFO TGCP LZ4: tools/roe_tgcp_2023.py, встроенный bounded decoder")
        for module in ("cryptography", "capstone", "PIL", "lz4"):
            checks.append(f"{'OK' if importlib.util.find_spec(module) else 'MISSING'} python-module {module}")
        runtime = root / "runtime/client/Europa_Client.exe"
        original = root.parent / "Ring of Elysium-2022/Europa_Client.exe"
        if runtime.is_file():
            with runtime.open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            checks.append(f"{'OK' if digest == EXPECTED_SHA else 'MISSING'} runtime EXE SHA-256={digest}")
            if original.is_file():
                a, b = runtime.stat(), original.stat()
                independent = (a.st_dev, a.st_ino) != (b.st_dev, b.st_ino)
                checks.append(f"{'OK' if independent else 'MISSING'} runtime EXE независим от оригинала")
        checks.append("MANUAL full runtime/resources; независимость остальных файлов; Vulkan/X11;16GiBfree; sudo/unshare; один исследователь; свободный prefix")
        checks.append("MANUAL ключ только проверить по доступности; его содержимое не выводить. Проверка не доказывает готовность runtime/драйвера")
    if any(row["run_profile"] in {"windows", "lan"} for row in selected):
        checks.append("MANUAL Windows11/клиент/локальный или LAN стенд: отдельная инструкция AGENT-START.md и RUNBOOK.md; Linux preflight не заменяет native запуск")
    return checks


def handoff(rows, selected, root):
    by_id = {row["id"]: row for row in rows}
    lines = ["# Поручение агенту: восстановление зимней сессии2022", "",
             f"Рабочий корень: `{root}`. План{rows[0]['plan_version']}; EXE2022 x64 0.2.989.0; map16010; SHA256 `{EXPECTED_SHA}`.",
             "", "Сначала прочитай ../AGENTS.md, AGENTS.md и docs/recovery/AGENT-START.md. Затем только выбранные строки CSV и их agent_context; не перечитывай всю историю.",
             "", "Архитектура: клиент→локальное.NET lobby→TCP bridge→TGCP/UDP Python endpoint→клиент. Peer — наша реконструкция. Native host не найден; Lua callbacks с заглушками не являются engine.",
             "", "Выдача этого поручения не запускает программу. Проверь действующие инструкции пользователя и стенд. Не меняй оригиналы; сервисы loopback; без Docker/дополнительных моделей, если отдельно не поручено. Не читай секреты/полные дампы.",
             "", "Берись только за выбранный объём; зависимости проверить по evidence и требуемой функции. baseline означает опору для опыта, а не закрытую механику. queued можно исследовать, но завершение зависит от указанных задач. external_blocked требует названного внешнего материала."]
    for row in selected:
        lines.extend(["", f"## №{row['sequence']} — {row['id']}: {row['mechanic']}", "",
                      f"Очередь: {row['work_state']}; фаза:{row['phase']}; этапы:{row['progress_pct']}%; fidelity:{row['fidelity']}; basis:{row['basis']}.",
                      "", row["agent_goal"], "", f"Ближайшее действие: {row['next_step']}",
                      "", f"Известные границы: {row['limitations']}", "", f"Сигналы: {row['signals'] or 'не установлены'}; первичная привязка: {row['primary_ref'] or 'ещё не установлена'}."])
        lines.extend(["", "Прочитать по порядку:", ""] + [f"- `{path}`" for path in row["agent_context"].split("|")])
        lines.extend(["", f"Источники: `{row['sources']}`.", f"Положительные/отрицательные доказательства: `{row['evidence'] or 'нет; задачу не считать подтверждённой'}`.",
                      "", "Зависимости:", ""])
        for ident in filter(None, row["depends_on"].split("|")):
            dependency = by_id[ident]
            lines.append(f"- №{dependency['sequence']} {ident}: {dependency['work_state']}, {dependency['progress_pct']}%; {dependency['limitations']}")
        if not row["depends_on"]:
            lines.append("- Нет формальных зависимостей; общий стенд проверить отдельно.")
        lines.extend(["", f"Точки изменения: `{row['edit_targets']}`; общие файлы не редактировать одновременно с другим опытом.",
                      "", "Проверка входов, без запуска клиента:", "", "```bash", row["start_command"], "```",
                      "", f"Профиль опыта: **{row['run_profile']}**, команда/ограничения — docs/recovery/RUNBOOK.md. Этот профиль проверяет исходную базу; новый feature сначала реализовать и проверить отдельно.",
                      "", "Проверки после изменений:", "", "```bash", row["verify_command"], "```",
                      "", f"Готово, когда: {row['acceptance']}", "", f"Сохранить: {row['deliverables']}",
                      "", f"Каталог результатов: `{row['result_dir']}`; новый run со свободным именем, старый не перезаписывать.",
                      "", f"Финал: обнови только связанные ID, источники, ограничения и этапы. Дата updated — дата опыта. Выполни `python -B tools/recovery_status.py --recalculate --write --snapshot --note \"{row['id']}: фактический результат и граница\"`. Затем progress/hypotheses и копия agents-context. Не объявляй100% по одному UI-событию."])
    lines.extend(["", "В ответе: что получилось, что не получилось, следующий опыт, пути evidence и новые этапы. Если входов недостаточно — конкретные отсутствующие файлы/SDK/трасса; полезный статический разбор допустим без запуска.", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=ROOT / "docs/recovery/mechanics-2022.csv")
    parser.add_argument("--workspace", type=Path, default=ROOT, help="Корень ROE_SERVER с исходниками и ресурсами")
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--task", action="append", help="ID, номер, диапазон5-6 или список5,INV02; флаг повторяемый")
    choice.add_argument("--next", action="store_true", help="Первый work_state=ready, не baseline")
    choice.add_argument("--list", action="store_true", help="Показать весь порядок без большого контекста")
    parser.add_argument("--preflight", action="store_true", help="Проверить входы/хеш runtime; без чтения ключа и запуска")
    parser.add_argument("--output", type=Path, help="Сохранить поручение в новый Markdown внутри workspace")
    args = parser.parse_args()
    if args.list and (args.preflight or args.output):
        parser.error("--list не совмещается с --preflight/--output")
    root = args.workspace.resolve()
    try:
        rows = load_plan(args.csv, root=root, check_references=False)
        if not all("sequence" in row for row in rows):
            raise ValueError("Нужен CSV плана2 с поручениями агенту")
        if args.list:
            for row in sorted(rows, key=lambda r: int(r["sequence"])):
                print(f"{int(row['sequence']):03} {row['id']:7} {row['work_state']:16} {row['phase']:2} {row['mechanic']}")
            return
        if args.next:
            selected = sorted([r for r in rows if r["work_state"] == "ready"], key=lambda r: int(r["sequence"]))[:1]
            if not selected:
                raise ValueError("Нет ready-задачи; пересмотри очередь, не пропускай blocker автоматически")
        else:
            selected = select_tasks(rows, args.task)
        report = handoff(rows, selected, root)
        checks = preflight(root, selected) if args.preflight else []
        if checks:
            report += "\n## Проверка входов\n\n" + "\n".join(f"- {check}" for check in checks) + "\n"
        if args.output:
            target = args.output.resolve()
            if not target.is_relative_to(root):
                raise ValueError("--output должен быть внутри ROE_SERVER")
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("x", encoding="utf-8") as destination:
                destination.write(report)
            print(f"Поручение сохранено: {target}")
        else:
            print(report)
        if any(check.startswith("MISSING") for check in checks):
            raise SystemExit(2)
    except (ValueError, OSError, ImportError) as error:
        parser.exit(1, f"Ошибка поручения: {error}\n")


if __name__ == "__main__":
    main()
