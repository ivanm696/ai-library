from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_repository_has_required_files():
    assert (ROOT / "README.md").exists()
    assert (ROOT / "pdf").is_dir()

    expected_pdfs = [
        "Kniga-0-Katalog-Biblioteki.pdf",
        "Kniga-1-Osnovy-Iskusstvennogo-Intellekta.pdf",
        "Kniga-2-Prompt-Inzhiniring.pdf",
        "Kniga-3-Arkhitektura-Neirosetey-i-Transformerov.pdf",
        "Kniga-4-Prakticheskoe-Primenenie-II.pdf",
        "Kniga-5-Etika-Bezopasnost-i-Ogranicheniya-II.pdf",
    ]

    for name in expected_pdfs:
        assert (ROOT / "pdf" / name).exists(), f"Missing required PDF: {name}"
