# M1 baseline test results

This file is populated only with tests that were actually run. Untested cases remain explicitly marked as such.

Tested artifact: CFRU SHA-256 `32136e7063ea8ea54eed429a4f311f3ae093037e4281cda00ee9618a353b52cc`.

## Automated mGBA 0.10.5 smoke test

| Check | Result | Evidence |
|---|---|---|
| ROM boots | PASS | Headless libmGBA framebuffer reached the FireRed title screen. |
| New game | PASS | Intro completed and player appeared in the bedroom. |
| Map transitions | PASS | Bedroom to downstairs, house to Pallet Town, and Pallet Town to Oak's lab were exercised. |
| Starter selection | PASS | Squirtle was selected and appeared in battle and as a follower. |
| Introductory rival battle | PASS | Battle against Bulbasaur completed; post-battle lab state was reached. |
| In-game save | PASS | Save menu wrote a 131,088-byte mGBA save container containing 128 KiB flash data; SHA-256 `cb19f54b26f918fc0f485c7bc32d650bf2478a0d1d7e6352b2f96456471cce6a`. The save is a disposable test artifact and is not tracked. |
| Full emulator restart/load | PASS | A new core process displayed `CONTINUE` with the saved player and loaded the post-rival lab state. |
| Wild encounter and catch | UNTESTED | Requires continued gameplay to obtain Poké Balls and reach grass. |
| Pokédex registration | UNTESTED | Depends on the catch test. |
| PC deposit/withdraw | UNTESTED | Depends on the catch test and reaching a PC. |
| Graphics corruption | PARTIAL PASS | Title, intro, indoor/outdoor maps, starter-selection graphics, front/back battle sprites, and follower display rendered correctly in captured framebuffers. |
| Audio corruption | UNTESTED | The headless harness has no audio output. |

The build candidate is therefore not yet eligible for the `gen9-engine-baseline` milestone tag. The remaining interactive and audio checks must pass before M1 is declared complete.

## Emulator method

The installed desktop mGBA could launch under Wayland. With temporary X11 display permission, its title frame was captured successfully, but the Qt frontend exited when synthetic key events were sent, before a reliable GUI gameplay run could be completed. Tests above therefore used the same installed mGBA 0.10.5 core through a small temporary harness, deterministic key schedules, framebuffer captures, and separate processes for save/reload. No BIOS was supplied; mGBA's HLE BIOS was used.
