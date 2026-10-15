# Ring of Elysium Research — restoration context

**English** | [Русский](README.ru.md) · [Discord](https://discord.gg/pD2Bj5kAxk)

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
