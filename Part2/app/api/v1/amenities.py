---FILEPATH Part2/app/api/v1/amenities.py
---FIND
```
class Amenity:
    """Amenity class"""
    
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    
def some_function_with_a_long_name_that_exceeds_the_character_limit_of_seventy_nine_characters():
    print("This is a long line that needs to be broken down into multiple lines to comply with PEP 8 guidelines.")
    
```
---REPLACE
```
class Amenity:
    """Amenity class"""


    def __init__(self, name):
        self.name = name


    def __str__(self):
        return self.name


def some_function_with_a_long_name_that_exceeds_the_character_limit_of_seventy_nine_characters():
    print("This is a long line that needs to be broken down into multiple "
          "lines to comply with PEP 8 guidelines.")

```
---COMPLETE