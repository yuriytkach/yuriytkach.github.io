from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def assert_exists(path: str) -> None:
    full = ROOT / path
    assert full.exists(), f"Missing required path: {path}"


def main() -> None:
    required = [
        "index.html",
        "resume/index.html",
        "volunteer/index.html",
        "calendar/index.html",
        "contact/index.html",
        "assets/css/styles.css",
        "assets/js/main.js",
        "assets/js/volunteer.js",
        "data/volunteer-posts.json",
    ]
    for path in required:
        assert_exists(path)

    posts_dir = ROOT / "volunteer/posts"
    assert posts_dir.exists(), "Missing volunteer posts directory"
    post_pages = list(posts_dir.glob("*/index.html"))
    assert len(post_pages) >= 20, "Expected at least 20 volunteer post pages"


if __name__ == "__main__":
    main()
