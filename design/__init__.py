# Define types of keywords (as regex?)

functions = ["if","elif","else","return","def",
             "and","or","not","is","in","for "," as ",
             "while ", "class ", "import " ]

key_types = ["str","int","float","type","repr",
             "range","open","len","sorted","set",
             "None","True","False","bool" ]

user_defn = ["foxdot"]

comments =  ["#"]

# Dictionary of keywords to their appropriate colours

python_kw =   { 'functions' : functions,
                'key_types' : key_types,
                'user_defn' : user_defn,
                'comments'  : comments }

python_kw_chars = []

for a, b in python_kw.items():
    for word in b:
        for char in word:
            if char not in python_kw_chars:
                python_kw_chars.append(char)
