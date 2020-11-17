def temp_converter(temp, new_temp_unit):
        if new_temp_unit == 'celsius':
            result = { 'C':temp - 273.15}
            return result
        elif new_temp_unit == 'farenheit':
            result = {'F':(temp - 273.15) * 9/5 + 32}
            return result
        else :
            result = {'K' : temp}
            return result