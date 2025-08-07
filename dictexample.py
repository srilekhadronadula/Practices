names={'srilekha','prani','pushpa','chinna'}
d={}
for i in names:
    d[i]=len(i)
print(d)
print({name:len(name) for name in names})
print({name:'even' if len(name)%2==0 else 'odd' for name in names if len(name)>5})
