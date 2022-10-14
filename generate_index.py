import shutil
from io import StringIO
from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("index_folder")
parser.add_argument("package")
parser.add_argument("version")

args = parser.parse_args()
path = Path(args.index_folder)

LINE_TEMPLATE = """<a href="{package}/{version}/{wheel}">{wheel}</a><br />"""
output = StringIO()

package_path = Path(".") / args.package

dst_path = package_path / args.version
dst_path.mkdir(parents=True, exist_ok=True)

for wheel in path.glob("*.whl"):
    output.write(
        LINE_TEMPLATE.format(
            package=args.package, version=args.version, wheel=wheel.name
        )
    )
    output.write("\n        ")
    shutil.copy2(wheel, dst_path / wheel.name)

wheel_hrefs = output.getvalue()

index_path = package_path / "index.html"
index_content = f"""<html>
    <head>
        <title>Links for {args.package}</title><style type="text/css"></style>
    </head>
    <body>
        <h1>Links for scipy</h1>
        {wheel_hrefs}
    </body>

</html>
"""
index_path.write_text(index_content)
