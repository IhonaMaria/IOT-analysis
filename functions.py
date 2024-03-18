def check_temperature(data, threshold):
    """
    Check if the temperature data exceeds a given threshold and print a warning if it does.


    Parameters:
    - data (float): The temperature data to check.
    - threshold (float): The temperature threshold.


    Returns:
    - bool: True if data is greater than threshold, False otherwise.
    """
    if data > threshold:
        return True
    else:
        return False


def convert_temperature(data, conversion):
    """
    Convert temperature data between Celsius, Fahrenheit, and Kelvin.

    Parameters:
    - data (float): The temperature data to convert.
    - conversion (str): The target temperature scale ('fahrenheit', 'kelvin', 'celsius').

    Returns:
    - tuple: A tuple containing the converted temperature data and its unit as a string.
    """
    if conversion.lower() == 'fahrenheit':
        return (data * 9/5) + 32, 'Fahrenheit'
    elif conversion.lower() == 'kelvin':
        return data + 273.15, 'Kelvin'
    elif conversion.lower() == 'celsius':
        return data, 'Celsius'  # Assuming the input data is already in Celsius.
    else:
        raise ValueError("Invalid conversion parameter. Use 'fahrenheit', 'kelvin', or 'celsius'.")

