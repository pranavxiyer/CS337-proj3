import re
from fractions import Fraction

def to_decimal(amount):
    total = 0
    for part in amount.split():
        total += float(Fraction(part))

    return total

def multiply_ingredients(parsed_recipe, multiplier):
    units = []

    for ingredient in parsed_recipe['ingredients']:
        ingredient['amount'] = multiplier * to_decimal(ingredient['amount'])
        units.append(ingredient['unit'])

    pattern = re.compile(r'(\d+\s\d+/\d+|\d+/\d+|\d+(\.\d+)?)\s*(' + '|'.join(units) + r')')

    for step, text in parsed_recipe['directions'].items():
        def double_match(match):
            quantity = match.group(1)
            unit = match.group(3)
            
            value = multiplier * to_decimal(quantity)
            
            formatted_value = f'{value}'.rstrip('0').rstrip('.')
            
            if value == 1 and unit.endswith('s'):
                unit = unit[:-1]
            elif value != 1 and not unit.endswith('s'):
                unit += 's'
            
            return f'{formatted_value} {unit}'
        
        parsed_recipe['directions'][step] = pattern.sub(double_match, text)

    return parsed_recipe