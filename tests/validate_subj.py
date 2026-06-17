"""验证主观题数据结构完整性"""
import json
import sys
import re

def validate(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        d = json.load(f)

    subj = d.get('subj', [])
    errors = []

    if len(subj) != 15:
        errors.append(f"应有15道题, 实际{len(subj)}道")

    for i, s in enumerate(subj):
        idx = i + 1
        required = ['q', 'a', 'keywords', 'short', 'mnemonic']
        for field in required:
            if field not in s:
                errors.append(f"第{idx}题缺少字段: {field}")
                continue
            val = s[field]
            if field == 'keywords':
                if not isinstance(val, list) or len(val) == 0:
                    errors.append(f"第{idx}题 keywords 应为非空数组")
                else:
                    # mnemonic 用分隔符的, 按分隔符拆分段数对比keywords长度
                    mn = s.get('mnemonic', '')
                    parts = [p for p in re.split(r'[；;、，,\s]', mn) if p]
                    expected_keys = len(parts) if len(parts) >= 2 else len(mn)
                    if len(val) < expected_keys - 1:
                        errors.append(f"第{idx}题 keywords({len(val)}) 与 mnemonic 不匹配")
            elif field == 'short':
                if not isinstance(val, str) or len(val) < 5:
                    errors.append(f"第{idx}题 short 太短: {val}")
            elif field == 'mnemonic':
                if not isinstance(val, str) or len(val) < 2:
                    errors.append(f"第{idx}题 mnemonic 太短: {val}")
            elif field in ('q', 'a'):
                if not isinstance(val, str) or len(val) < 3:
                    errors.append(f"第{idx}题 {field} 为空或太短")

    if errors:
        print(f"FAIL: {len(errors)} 个错误")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print(f"PASS: {len(subj)} 道主观题, 全部字段完整")
        return True


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'data.json'
    sys.exit(0 if validate(path) else 1)
