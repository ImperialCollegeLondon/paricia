"""Generate the code reference pages and navigation."""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

search = [
    "djangomain",
    "formatting",
    "importing",
    "management",
    "measurement",
    "sensor",
    "station",
    "utilities",
    "variable",
]

for app in search:
    for path in sorted(Path(app).glob("**/*.py")):
        module_path = path.relative_to(".").with_suffix("")
        doc_path = path.relative_to(".").with_suffix(".md")
        full_doc_path = Path("reference", doc_path)

        parts = list(module_path.parts)
        if ".array_cache" in parts:
            continue
        if "migrations" in parts:
            continue
        elif parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")
            full_doc_path = full_doc_path.with_name("index.md")
        elif parts[-1] == "__main__":
            continue
        nav[parts] = doc_path

        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            ident = ".".join(parts)
            print("::: " + ident, file=fd)

        mkdocs_gen_files.set_edit_path(full_doc_path, Path("../") / path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
