from __future__ import annotations

from .scraping import write_scraped_snapshots


def main() -> None:
    paths = write_scraped_snapshots()
    print("Scraped sample marketplace pages into JSON snapshots:")
    for path in paths:
        print(f"- {path}")


if __name__ == "__main__":
    main()
