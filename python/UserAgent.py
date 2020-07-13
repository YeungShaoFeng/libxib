from re import sub as re_sub


a = '''
UserAgent Here. 
'''
pattern = '^(.*?): (.*)$'
for line in a.splitlines():
    print(re_sub(pattern, '\'\\1\': \'\\2\',', line))
print()