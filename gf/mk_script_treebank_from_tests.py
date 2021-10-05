print("echo '")
for line in open('../tests/fixture/gf.txt'):
    if '=' not in line:
        continue
    line = line.strip()
    expr = line.split('=', 2)[1].strip()
    if expr.startswith('$'):
        continue
    print(f'ps "{line}"')
    print(f'linearize {expr}')
print("' | gf --quiet dist/Mnlg.pgf")
