import test_input

def sum_calibration_values(sinput):
    calibration_val_sum = 0
    lines = sinput.split('\n')
    for line in lines:
        calibration_digit_1 = 0
        calibration_digit_2 = 0
        read_2_digits = False
        for char in line:
            if char.isnumeric():
                if calibration_digit_1 == 0:
                    calibration_digit_1 = int(char)
                else:
                    calibration_digit_2 = int(char)
                    read_2_digits = True
        if not read_2_digits:
            calibration_digit_2 = calibration_digit_1
        calibration_val = (int(calibration_digit_1)*10) + int(calibration_digit_2)
        calibration_val_sum = calibration_val_sum + calibration_val
    return calibration_val_sum

calibration_sum = sum_calibration_values(test_input.full_input)

print(calibration_sum)