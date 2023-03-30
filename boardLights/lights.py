def binary_row_to_boolean(binary_row):
    return_array = [0 for i in range(8)]
    num_bits = 8
    bits = [(binary_row >> bit) & 1 for bit in range(num_bits - 1, -1, -1)]

    count = 0
    for num in bits:
        if num == 1:
            return_array[count] = True
        else:
            return_array[count] = False
        count += 1
    return return_array

print(binary_row_to_boolean(0b11110111))
