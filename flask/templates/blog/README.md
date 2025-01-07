
This page was created using
```bash
find . -type f | sort | grep /20 > blog_list.html
```

```bash
docker run -it -v `pwd`:/scratch -w /scratch/ --rm benislocated/data-science-jupyter python3 /scratch/convert_feedatom_from_google_takeout_to_flat_html_files.py
```
