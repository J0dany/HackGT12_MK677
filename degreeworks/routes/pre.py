import re
import requests
from bs4 import BeautifulSoup

def get_prereq_groups(course_code: str, term: str = "202402") -> list[list[str]]:
    m = re.match(r"\s*([A-Za-z&]+)\s*([0-9A-Za-z]+)\s*$", course_code)
    if not m:
        raise ValueError(f"Bad course code: {course_code!r}")
    subj, numb = m.group(1).upper(), m.group(2).upper()
    url = ("https://oscar.gatech.edu/bprod/bwckctlg.p_disp_course_detail"
           f"?cat_term_in={term}&subj_code_in={subj}&crse_numb_in={numb}")
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    resp.raise_for_status()
    html = resp.text
    lo = html.lower()
    start = lo.find("prerequisites:")
    if start == -1:
        return []
    stops = [x for x in (lo.find("restrictions:", start), lo.find("return to previous", start)) if x != -1]
    end = min(stops) if stops else len(lo)
    snippet_html = html[start:end]
    text = BeautifulSoup(snippet_html, "html.parser").get_text(" ", strip=True)
    parens = re.findall(r"\((.*?)\)", text, flags=re.DOTALL)
    code_re = re.compile(r"\b([A-Z&]{2,})\s+([0-9A-Z]{3,5})\b")
    groups = []
    if parens:
        for block in parens:
            opts = []
            for s, n in code_re.findall(block):
                code = f"{s} {n}"
                if re.match(r"^[A-Z&]+$", s) and re.match(r"^[0-9X][0-9A-Z]{2,4}$", n):
                    if code not in opts:
                        opts.append(code)
            if opts:
                groups.append(sorted(opts))
    else:
        opts = []
        for s, n in code_re.findall(text):
            code = f"{s} {n}"
            if re.match(r"^[A-Z&]+$", s) and re.match(r"^[0-9X][0-9A-Z]{2,4}$", n):
                if code not in opts:
                    opts.append(code)
        if opts:
            groups.append(sorted(opts))
    return groups