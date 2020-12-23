import requests

html_body="""<!DOCTYPE html>
<html>
<body>
{}
</body>
</html>
"""

wheels_indices = []

release_dict = requests.get("https://api.github.com/repos/suquark/pickle5-backport/releases/latest").json()

for asset in release_dict['assets']:
    wheels_indices.append(f'<a href="{asset["browser_download_url"]}" data-requires-python=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*">{asset["name"]}</a>')

wheels_indices_html = html_body.format('\n<br>'.join(wheels_indices))
with open("package_indices.html", "w") as f:
    f.write(html_body.format('<a href="wheels_indices.html">pickle5</a>'))

with open("pickle5/index.html", "w") as f:
    f.write(wheels_indices_html)
