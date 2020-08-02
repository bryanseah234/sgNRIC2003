def is_nric_valid(nric):
    nricCheckDigits = 'JZIHGFEDCBA'
    finCheckDigits = 'XWUTRQPNMLK'
    weights = [2, 7, 6, 5, 4, 3, 2]
    if len(nric) != 9:
        return False

    firstChar = nric[0].upper()
    digits = nric[1:8]
    lastChar = nric[8].upper()
    
    if firstChar not in "STFG" or not digits.isdigit():
        return False

    total = 0
    if firstChar in "GT":
        total += 4

    for i in range(7):
        total += int(digits[i]) * weights[i]

    if firstChar in "ST":
        return nricCheckDigits[total % 11] == lastChar

    return finCheckDigits[total % 11] == lastChar

for nric in all_nrics:
    if is_nric_valid(nric) == True:
        print(nric)
    else:
        pass
