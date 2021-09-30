print("echo '")
for l in open('../tests/fixture/gf.txt'):
    if '=' not in l:
        continue
    l = l.strip()
    expr = l.split('=', 2)[1].strip()
    print(f'ps "{l}"')
    print(f'linearize {expr}')
print("' | gf dist/Mnlg.pgf")
