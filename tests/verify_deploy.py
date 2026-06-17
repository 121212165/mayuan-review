"""部署验证：检查线上 data.json 和 index.html 是否已部署新功能"""
import json
import sys
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else 'https://565733.xyz'
fail = 0

# 1. data.json
try:
    resp = urllib.request.urlopen(f'{BASE}/data.json', timeout=10)
    d = json.loads(resp.read().decode('utf-8'))
    subj = d['subj']
    print(f'[data.json] OK - {len(subj)} 道主观题')
    new_fields = ['keywords', 'short', 'mnemonic']
    for s in subj:
        for f in new_fields:
            if f not in s:
                print(f'  FAIL: 缺少字段 {f}')
                fail += 1
                break
        else:
            continue
        break
    else:
        print(f'  [data.json] 新字段(keywords/short/mnemonic): 全部存在')
except Exception as e:
    print(f'[data.json] FAIL: {e}')
    fail += 1

# 2. index.html - 检查 renderSubj 包含三栏标签逻辑
try:
    resp = urllib.request.urlopen(f'{BASE}/', timeout=10)
    html = resp.read().decode('utf-8')
    checks = [
        ('switchSubjTab', '三栏标签切换函数'),
        ('subj-tab active', '默认激活"全文"标签'),
        ('data-mode="quick"', '速记模式'),
        ('data-mode="mnemonic"', '口诀模式'),
        ('mnemonic-display', '大号口诀展示'),
        ('kw-chips', '要点关键词标签'),
    ]
    for snippet, label in checks:
        if snippet in html:
            print(f'[index.html] OK - {label}')
        else:
            print(f'[index.html] FAIL - 缺少: {label}')
            fail += 1
except Exception as e:
    print(f'[index.html] FAIL: {e}')
    fail += 1

if fail:
    print(f'\n结果: FAIL ({fail} 项失败)')
    sys.exit(1)
else:
    print('\n结果: PASS - 所有部署验证通过')
