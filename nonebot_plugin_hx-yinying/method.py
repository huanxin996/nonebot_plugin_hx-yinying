import random

def number_suiji():
    """
    随机数生成
    """
    digits = "0123456789"
    str_list =[random.choice(digits) for i in range(3)]
    random_str =''.join(str_list)
    return random_str