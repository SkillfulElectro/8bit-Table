def get_bit_count(n):
    """Returns the number of set bits (1s) in binary representation of n."""
    return bin(n).count('1')

def minterm_to_binary(minterm, num_vars):
    """Convert minterm number to binary string with num_vars bits."""
    return format(minterm, f'0{num_vars}b')

def combine_terms(term1, term2):
    """Combine two terms if they differ by exactly one bit."""
    combined = []
    diff_count = 0
    for bit1, bit2 in zip(term1, term2):
        if bit1 != bit2:
            combined.append('-')
            diff_count += 1
        else:
            combined.append(bit1)
    if diff_count == 1:
        return ''.join(combined)
    return None

def find_prime_implicants(minterms, num_vars):
    groups = [[] for _ in range(num_vars + 1)]

    # Group minterms by number of 1s in their binary representation
    for minterm in minterms:
        bin_repr = minterm_to_binary(minterm, num_vars)
        groups[get_bit_count(minterm)].append(bin_repr)

    prime_implicants = set()
    all_combinations = set()

    while True:
        new_groups = [[] for _ in range(num_vars + 1)]
        used = set()
        has_combined = False

        for i in range(len(groups) - 1):
            for term1 in groups[i]:
                for term2 in groups[i + 1]:
                    combined = combine_terms(term1, term2)
                    if combined:
                        has_combined = True
                        new_groups[get_bit_count(int(combined.replace('-', '0'), 2))].append(combined)
                        used.add(term1)
                        used.add(term2)
                        all_combinations.add(combined)
        
        # Collect uncombined terms as prime implicants
        for group in groups:
            for term in group:
                if term not in used:
                    prime_implicants.add(term)
        
        if not has_combined:
            break
        
        groups = new_groups
    
    return prime_implicants

def get_essential_prime_implicants(prime_implicants, minterms, num_vars):
    essential_prime_implicants = set()
    covered_minterms = set()

    for minterm in minterms:
        covering_implicants = []
        for implicant in prime_implicants:
            bin_minterm = minterm_to_binary(minterm, num_vars)
            if all(m == i or i == '-' for m, i in zip(bin_minterm, implicant)):
                covering_implicants.append(implicant)
        
        if len(covering_implicants) == 1:
            essential_prime_implicants.add(covering_implicants[0])
            covered_minterms.add(minterm)
    
    for implicant in essential_prime_implicants:
        minterms = [m for m in minterms if not all(mb == ib or ib == '-' for mb, ib in zip(minterm_to_binary(m, num_vars), implicant))]

    return essential_prime_implicants, minterms

def term_to_expr(term, num_vars):
    """Convert binary term with '-' to a Boolean expression."""
    variables = [chr(ord('A') + i) for i in range(num_vars)]
    expr = []
    for i, bit in enumerate(term):
        if bit != '-':
            if bit == '0':
                expr.append(variables[i] + "'")
            else:
                expr.append(variables[i])
    return ''.join(expr)

def simplify_minterms(minterms, num_vars):
    prime_implicants = find_prime_implicants(minterms, num_vars)
    essential_prime_implicants, remaining_minterms = get_essential_prime_implicants(prime_implicants, minterms, num_vars)

    # Form the final simplified expression
    simplified_expr = ' + '.join(term_to_expr(term, num_vars) for term in essential_prime_implicants)
    
    return simplified_expr


#A B C D E F G H
def replace_letters(input_string):
    # Define the mapping of letters to replacements
    letter_mapping = {'A': 'E', 'B': 'F', 'C': 'G', 'D': 'H'}

    # Initialize an empty result string
    result = ""

    # Iterate through each character in the input string
    for char in input_string:
        # If the character is in the mapping, replace it; otherwise, keep it unchanged
        result += letter_mapping.get(char, char)

    return result


def simplify_8bit_nums(start, end):
    arr1 = []
    arr2 = []
    for number in range(start, end + 1):
        # Convert to binary without the '0b' prefix and pad with leading zeros
        binary_string = bin(number)[2:].zfill(8)
        
        # Split the 8-bit binary into two 4-bit segments
        first_4_bits = binary_string[:4]
        second_4_bits = binary_string[4:]
        
        # Convert each 4-bit segment back to decimal integer
        first_half_int = int(first_4_bits, 2)
        second_half_int = int(second_4_bits, 2)
        
        arr1.append(first_half_int)
        arr2.append(second_half_int)
        
        
    
    simplified_expr1 = simplify_minterms(arr1, 4)
    print(f"Simplified expression: {simplified_expr1}")
    
    simplified_expr2 = simplify_minterms(arr2, 4)
    print(f"Simplified expression: {replace_letters(simplified_expr2)}")
    
    print(f"final expression = ({simplified_expr1})&({replace_letters(simplified_expr2)})")



start_num = int(input("Enter the start number: "))
end_num = int(input("Enter the end number: "))

simplify_8bit_nums(start_num, end_num)


