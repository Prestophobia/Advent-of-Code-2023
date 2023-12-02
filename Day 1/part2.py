import test_input

digits_as_words = {
    "zero" : 0,
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

def word_to_digit(word):
    while not word in digits_as_words:
        if len(word) < 3:
            return 0,word
        else:
            word = word[1:]
    return digits_as_words[word],word

def update_digits(new_digit, digit_1, digit_2, read_2_digits):
    if digit_1 == 0:
        digit_1 = new_digit
    else:
        digit_2 = new_digit
        read_2_digits = True
    return digit_1, digit_2, read_2_digits

def sum_calibration_values(sinput):
    calibration_val_sum = 0
    lines = sinput.split('\n')
    for line in lines:
        calibration_digit_1 = 0
        calibration_digit_2 = 0
        calibration_digit_str = ""
        calibration_digit_str_as_number = 0
        read_2_digits = False
        parsed_digit_word = ""

        for char in line:
            calibration_digit_str_as_number,parsed_digit_word = word_to_digit(calibration_digit_str)
            if calibration_digit_str_as_number > 0:
                calibration_digit_1,calibration_digit_2,read_2_digits = update_digits(calibration_digit_str_as_number,calibration_digit_1,calibration_digit_2,read_2_digits)
                calibration_digit_str = parsed_digit_word[1:]
            if char.isnumeric():
                calibration_digit_1,calibration_digit_2,read_2_digits = update_digits(int(char),calibration_digit_1,calibration_digit_2,read_2_digits)
            else: 
                calibration_digit_str = calibration_digit_str + char

        calibration_digit_str_as_number,parsed_digit_word = word_to_digit(calibration_digit_str)
        if calibration_digit_str_as_number > 0:
            calibration_digit_1,calibration_digit_2,read_2_digits = update_digits(calibration_digit_str_as_number,calibration_digit_1,calibration_digit_2,read_2_digits)
            calibration_digit_str = parsed_digit_word[1:]
        if not read_2_digits:
            calibration_digit_2 = calibration_digit_1
        
        calibration_val = (int(calibration_digit_1)*10) + int(calibration_digit_2)
        calibration_val_sum = calibration_val_sum + calibration_val
    return calibration_val_sum

calibration_sum = sum_calibration_values(test_input.full_input)

print(calibration_sum)