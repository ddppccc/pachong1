import re
def if_contain_symbol(keyword):
    if re.search(r"\W", keyword.replace(' ','')):
        return True
    else:
        return False
