def get_prefixes(file='lietuviu.aff'):
    with open(file,'r', encoding='iso-8859-13') as f:
        x = f.readlines()
        
    prefix = '|'.join(x).split('suffixes')[0].split('|')
    prefix = [t.strip() for t in prefix if t!='\n']    
    prefix = [t.strip() for t in prefix if not t.startswith('#')]    
    prefix = [t.split('>')[1].strip().lower() for t in prefix if '>' in t]   
    prefix = sorted(prefix, key=len)[::-1]
    
    return prefix

def extract_prefix(word, prefixes):
    if len(word)<=3:
        return "", word
    wordl = word.lower()
    for key in prefixes:
        if wordl == key:
            return "", word
        if wordl.startswith(key):
            return word[:len(key)], word[len(key):]
    return "", word

def get_suffixes(file='lietuviu.aff'):
    with open(file,'r', encoding='iso-8859-13') as f:
        x = f.readlines()
        
    suffix = '|'.join(x).split('suffixes')[1].split('|')
    suffix = [t.strip() for t in suffix if t!='\n']    
    suffix = [t.strip() for t in suffix if not t.startswith('#')]    
    suffix = [t.strip() for t in suffix if '>' in t] 
    suffix = [t.split('#')[0].strip() for t in suffix] #remove comments
    suffix1 = [(t.split('>')[0].replace(' ','').lower(), 
               t.split('>')[1].split(',')[0].strip().strip('-').lower(), 
               t.split('>')[1].split(',')[1].strip().lower()) for t in suffix if ',' in t]
    suffix2 = [(t.split('>')[0].replace(' ','').lower(), 
               t.split('>')[1].split(',')[0].strip().strip('-').lower(), 
               t.split('>')[1].split(',')[0].strip().strip('-').lower()) for t in suffix if ',' in t]    
    suffix = suffix1 + suffix2
    suffix = sorted(suffix, key=lambda x: len(x[2]))[::-1]
    return suffix

def extract_suffix(word, suffixes):
    if len(word)<=3:
        return "", word    
    wordl = word.lower()
    for match, repl, key in suffixes:
        if wordl == key:
            return "", word
        if wordl.endswith(key):
            tmp = wordl[len(key):]
            tmp += repl
            #if tmp.endswith(match):
            return word[len(word)-len(key):], word[:len(word)-len(key)]
    return "", word

def split_word(word, prefixes, suffixes):
    prefix, word = extract_prefix(word, prefixes)
    suffix, root = extract_suffix(word, suffixes)
    return prefix, root, suffix

prefixes = get_prefixes()
suffixes = get_suffixes()

print(extract_prefix('pAsiBaiGusIuOse', prefixes))
print(extract_suffix('pAsiBaiGusIuOse', suffixes))
print(split_word('pAsiBaiGusIuOse', prefixes, suffixes))

text = "Baltieji rūmai patvirtino tolimojo nuotolio ATACMS raketų pristatymą į Ukrainą po to kai Kijevas paskelbė apie jų pirmąjį panaudojimą"
print(" ".join([r[0]+'|'+r[1]+'|'+r[2] for r in [split_word(t, prefixes, suffixes) for t in text.split(' ')]]))
