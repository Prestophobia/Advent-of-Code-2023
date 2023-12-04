import test_input

def word_to_digit(word:str) -> int:
    digits_as_words = {
        "one" : 1,
        "two" : 2,
        "three" : 3,
        "four" : 4,
        "five" : 5,
        "six" : 6,
        "seven" : 7,
        "eight" : 8,
        "nine" : 9
    } 
    while not word in digits_as_words:
        if len(word) < 3:
            return 0,word
        else:
            word = word[1:]
    return digits_as_words[word],word

def update_digits(new_digit:int, digit_1:int, digit_2:int):
    if digit_1 == 0:
        digit_1 = new_digit
    else:
        digit_2 = new_digit
    return digit_1, digit_2,

def update_parse_digit(buf:str, digit_1:int, digit_2:int):
    parsed_digit,parsed_word = word_to_digit(buf)
    if parsed_digit > 0:
        digit_1,digit_2 = update_digits(parsed_digit,digit_1,digit_2)
        buf = parsed_word[1:] # avoids reparsing
    return buf, digit_1, digit_2

def sum_calibration_values(sinput:str)->int:
    calibration_val_sum = 0
    lines = sinput.split('\n')
    for line in lines:
        digit_1,digit_2,buf = 0,0,""
        for char in line:
            buf,digit_1,digit_2 = update_parse_digit(buf,digit_1,digit_2)
            if char.isnumeric():
                digit_1,digit_2 = update_digits(int(char),digit_1,digit_2)
            else: 
                buf = buf + char
        buf,digit_1,digit_2 = update_parse_digit(buf,digit_1,digit_2)
        digit_2= digit_1 if digit_2 <= 0 else digit_2
        calibration_val_sum = calibration_val_sum + (int(digit_1)*10) + int(digit_2)
    return calibration_val_sum

print(sum_calibration_values(test_input.full_input))