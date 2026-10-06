"""Mở 2 cửa sổ game song song: tournament vs roulette."""
import subprocess
import sys

LEFT_POS = "50,80"
RIGHT_POS = "900,80"


def main():

    p1 = subprocess.Popen(
        [sys.executable, "-u", "flappy_bird.py",
         "--selection", "tournament", "--pos", LEFT_POS]
    )
    p2 = subprocess.Popen(
        [sys.executable, "-u", "flappy_bird.py",
         "--selection", "roulette", "--pos", RIGHT_POS]
    )

    try:
        p1.wait()
        p2.wait()
    except KeyboardInterrupt:
        print("\nDang dong 2 cua so...")
    finally:
        p1.terminate()
        p2.terminate()


if __name__ == "__main__":
    main()
