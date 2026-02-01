from datetime import datetime
from pathlib import Path
import re
import shutil
import sys

post_slug = input("Post slug: ")
now = datetime.now()
post_filename: str = now.strftime("%Y-%m-%d") + "-" + post_slug + ".md"

post_draft_md: Path = Path(sys.argv[1])
resources_path: Path = Path.home() / Path(".config/joplin-desktop/resources")
post_imgs: Path = Path("./assets/img/posts") / post_slug
posts: Path = Path("./_posts")

post_imgs.mkdir(parents=True, exist_ok=True)

replacements: list[tuple[str, str]] = []

post_text: str
with post_draft_md.open() as f:
    post_text = f.read()
    img_matches = re.findall(r"(!\[(.*?)\]\((?:\:|resources)/([a-f0-9]+?)(?:\..+?)?\))", post_text)
    img_num: int = 0
    for img_ref, img_name, img_id in img_matches:
        extension: str = ""
        if "." in img_name:
            extension = "." + img_name.split(".")[-1]
        orig_filename: str = img_id + extension
        new_img_name: str = str(img_num) + extension
        new_img_ref: str = f"![{new_img_name}](/{post_imgs}/{new_img_name})"
        replacements.append((img_ref, new_img_ref))
        with (resources_path / orig_filename).open("rb") as img_src, (post_imgs / new_img_name).open("wb+") as img_dst:
            img_dst.write(img_src.read())
        img_num += 1

for orig, repl in replacements:
    post_text = post_text.replace(orig, repl)

with (posts / post_filename).open("w+") as f:
    f.write(post_text)
