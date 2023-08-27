
import numpy as np

if __name__ == "__main__":
    # Create a 2D array (3x4) of random integers between 1 and 4
    random_integers = np.random.randint(low=1, high=5, size=(3, 4))

    # Convert the array rows to formatted strings and save to a variable
    formatted_array_str = '\n'.join([' '.join(map(str, row)) for row in random_integers])

    print(formatted_array_str)
