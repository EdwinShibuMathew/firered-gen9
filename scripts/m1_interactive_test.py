#!/usr/bin/env python3
"""
M1 Interactive Test Harness for FireRed Gen 9

Completes the remaining M1 gates:
1. Wild encounter and capture
2. Pokédex registration (save/reload)
3. PC deposit/withdraw (save/reload)
4. Audio playback verification
5. Graphics corruption check

This harness uses mGBA SDL frontend with X11/Wayland support for interactive gameplay.
Tests are manually observed and results documented in docs/TESTING.md.
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


def find_mgba():
    """Locate the local mGBA SDL binary."""
    mgba_path = Path(".tools/mgba-sdl/usr/games/mgba")
    if mgba_path.exists():
        return mgba_path.resolve()
    
    # Try system mGBA
    result = subprocess.run(["which", "mgba"], capture_output=True, text=True)
    if result.returncode == 0:
        return Path(result.stdout.strip())
    
    raise FileNotFoundError(
        "mGBA not found. Expected at .tools/mgba-sdl/usr/games/mgba or in PATH"
    )


def load_build_lock():
    """Load build-lock.json to verify ROM artifact."""
    lock_file = Path("build-lock.json")
    if not lock_file.exists():
        raise FileNotFoundError("build-lock.json not found")
    
    with lock_file.open() as f:
        return json.load(f)


def verify_rom_hash(rom_path: Path, expected_sha256: str) -> bool:
    """Verify ROM SHA-256 matches expected value."""
    import hashlib
    
    sha256_hash = hashlib.sha256()
    with rom_path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            sha256_hash.update(block)
    
    actual = sha256_hash.hexdigest()
    match = actual.lower() == expected_sha256.lower()
    
    print(f"ROM SHA-256: {actual}")
    if not match:
        print(f"Expected:   {expected_sha256}")
    
    return match


def launch_interactive_mgba(rom_path: Path):
    """Launch mGBA SDL frontend for interactive testing."""
    mgba = find_mgba()
    print(f"\n{'='*70}")
    print(f"Launching interactive mGBA SDL")
    print(f"ROM: {rom_path}")
    print(f"mGBA: {mgba}")
    print(f"{'='*70}\n")
    
    print("M1 Interactive Test Script")
    print("-" * 70)
    print("\nTest sequence (manual observation):")
    print("  1. Obtain Poké Balls")
    print("     - Talk to Mom → Get money")
    print("     - Go to Pallet Town shop")
    print("     - Buy Poké Balls (should have funds from start)")
    print()
    print("  2. Capture a wild Pokémon")
    print("     - Go to Route 1 or grass area")
    print("     - Enter tall grass")
    print("     - Weaken a wild Pokémon (use Squirtle's water moves)")
    print("     - Throw Poké Ball and capture")
    print("     - SAVE after capture (Menu → Save)")
    print()
    print("  3. Verify Pokédex")
    print("     - Open Pokédex (menu)")
    print("     - Check captured species is registered")
    print("     - Check stats/data")
    print()
    print("  4. Test PC operations")
    print("     - Find a PC (house, Pokémon Center, etc)")
    print("     - Deposit captured Pokémon")
    print("     - Withdraw captured Pokémon")
    print("     - Return to party")
    print("     - SAVE (Menu → Save)")
    print()
    print("  5. Reload save")
    print("     - Close emulator")
    print("     - Relaunch this script")
    print("     - Select 'Continue' when prompted")
    print("     - Verify captured Pokémon persists in party/PC")
    print()
    print("  6. Audio check")
    print("     - While playing, listen for:")
    print("       • Title screen music")
    print("       • Battle music")
    print("       • Wild Pokémon cry")
    print("       • Menu/interaction sounds")
    print()
    print("Once you've completed all tests above, document results in:")
    print("  docs/TESTING.md")
    print()
    print("Press Enter to launch mGBA, then close the window when tests are done.")
    input("> ")
    
    try:
        subprocess.run([str(mgba), str(rom_path)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"mGBA exited with code {e.returncode}")
        return False
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        return False
    
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Complete M1 interactive tests on FireRed Gen 9 ROM"
    )
    parser.add_argument(
        "--rom",
        type=Path,
        default=Path(".upstream/cfru/test.gba"),
        help="Path to ROM (default: .upstream/cfru/test.gba)",
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip ROM SHA-256 verification",
    )
    args = parser.parse_args()
    
    # Verify ROM exists
    if not args.rom.exists():
        print(f"Error: ROM not found: {args.rom}", file=sys.stderr)
        return 1
    
    # Load build lock and verify ROM hash
    try:
        lock = load_build_lock()
        expected_sha256 = lock["artifacts"]["cfru"]["sha256"]
    except (FileNotFoundError, KeyError) as e:
        print(f"Error loading build lock: {e}", file=sys.stderr)
        return 1
    
    if not args.skip_verify:
        if not verify_rom_hash(args.rom, expected_sha256):
            print("ROM hash mismatch! Verify your build is current.", file=sys.stderr)
            return 1
    
    # Launch interactive test
    if not launch_interactive_mgba(args.rom):
        return 1
    
    print("\n" + "=" * 70)
    print("Interactive tests completed!")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Update docs/TESTING.md with:")
    print("     - Test results (PASS/FAIL) for each gate")
    print("     - Observed evidence (screenshots, descriptions)")
    print("     - Any graphics/audio issues noted")
    print()
    print("  2. Once all M1 gates pass, tag the commit:")
    print("     git tag -a gen9-engine-baseline")
    print()
    print("  3. Begin M2 (species audit) when ready:")
    print("     python3 scripts/m1_interactive_test.py --help")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
