"""全站端到端测试"""
import urllib.request, json, sys

BASE = sys.argv[1] if len(sys.argv) > 1 else 'https://565733.xyz'
fail = 0

def check(label, ok, detail=''):
    global fail
    if ok:
        print(f'  [PASS] {label}')
    else:
        print(f'  [FAIL] {label} {detail}')
        fail += 1

# 1. Routes
print('--- Route Checks ---')
routes = [
    ('/',       '马克思主义基本原理'),
    ('/bingli', '病理学重点复习'),
    ('/mianyi', '免疫学与病原生物学'),
    ('/yiyongxinli', '医学心理学'),
]
for path, expected in routes:
    try:
        resp = urllib.request.urlopen(f'{BASE}{path}', timeout=10)
        html = resp.read().decode('utf-8')
        check(f'GET {path} → {expected}', expected in html)
    except Exception as e:
        check(f'GET {path}', False, str(e))

# 2. data.json
print('\n--- data.json ---')
try:
    resp = urllib.request.urlopen(f'{BASE}/data.json', timeout=10)
    d = json.loads(resp.read().decode('utf-8'))
    check('JSON valid', True)
    check(f'topics=7',   len(d.get('topics',[])) == 7)
    check(f'single=120', len(d.get('single',[])) == 120)
    check(f'multi=45',   len(d.get('multi',[])) == 45)
    check(f'subj=15',    len(d.get('subj',[])) == 15)
    check(f'knowledge=7',len(d.get('knowledge',[])) == 7)
    check('formulas',    'formulas' in d and 'core' in d['formulas'])
    check(f'errors=10',  len(d.get('errors',[])) == 10)
except Exception as e:
    check('data.json load', False, str(e))

# 3. Subjective questions
print('\n--- Subjective Questions ---')
for i, s in enumerate(d['subj'], 1):
    for f in ['q','a','keywords','short','mnemonic']:
        check(f'第{i}题.{f}', f in s and bool(s[f]))

# 4. Static resources
print('\n--- Static Resources ---')
for res in ['/styles.css', '/data.json']:
    try:
        resp = urllib.request.urlopen(f'{BASE}{res}', timeout=10)
        check(f'{res} loadable', resp.status == 200)
    except Exception as e:
        check(f'{res} loadable', False, str(e))

# 5. Index page features
print('\n--- Index Page Features ---')
resp = urllib.request.urlopen(f'{BASE}/', timeout=10)
html = resp.read().decode('utf-8')
check('nav btns',       'showSection' in html)
check('loadData()',     'loadData()' in html)
check('timer',          'POMODORO' in html)
check('knowledge',      'renderKP' in html)
check('single quiz',    'initSingleQuiz' in html)
check('multi quiz',     'initMultiQuiz' in html)
check('formula',        'renderFormula' in html)
check('error analysis', 'renderErrors' in html)
check('subj 3-tab',     'switchSubjTab' in html)

print(f'\n=== Result: {"PASS" if fail==0 else "FAIL"} ({fail} failures) ===')
sys.exit(0 if fail == 0 else 1)
