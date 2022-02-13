import pathlib

path = pathlib.Path('')
total = ''
map = {'内幕': '', '信息披露': '', '操纵': '', '其他': ''}
for it in sorted(path.iterdir(), key=lambda s: s.stat().st_mtime):
    if it.suffix != '.txt':
        continue
    titles = it.stem.split('-')
    lis = ['内幕', '信息披露', '操纵']
    with it.open('r') as fp:
        flag = False
        for l in lis:
            if l in it.stem:
                map[l] += 'zjh' + f'{titles[1]}（{titles[2]}）' + 'zjh' + '\n' + fp.read() + '\n'
                flag = True
                break
        if not flag:
            map['其他'] += 'zjh' + f'{titles[1]}（{titles[2]}）' + 'zjh' + '\n' + fp.read() + '\n'

total += map['内幕'] + '\n' + map['操纵'] + '\n' + map['信息披露'] + '\n' + map['其他'] + '\n'
with open('res.txt', 'w') as fpc:
    fpc.write(total)