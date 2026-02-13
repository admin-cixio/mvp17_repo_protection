"""
Hello World Application for MVP17 Repository Protection
This is a simple demo application that will be encrypted using FHE.
"""

def greet(name: str = "World") -> str:
    """
    Returns a greeting message.
    
    Args:
        name: The name to greet (default: "World")
        
    Returns:
        A greeting string
    """
    return f"Hello, {name}! Welcome to FHE Repository Protection."


def calculate_sum(numbers: list) -> int:
    """
    Calculate sum of numbers (this will be done with FHE).
    
    Args:
        numbers: List of integers to sum
        
    Returns:
        Sum of all numbers
    """
    return sum(numbers)


def calculate_product(numbers: list) -> int:
    """
    Calculate product of numbers (this will be done with FHE).
    
    Args:
        numbers: List of integers to multiply
        
    Returns:
        Product of all numbers
    """
    result = 1
    for num in numbers:
        result *= num
    return result


def main():
    """Main function to demonstrate the hello world app."""
    print("=" * 60)
    print(greet())
    print("=" * 60)
    
    # Demo calculations that will be done with FHE
    numbers = [1, 2, 3, 4, 5]
    print(f"\nOriginal numbers: {numbers}")
    print(f"Sum: {calculate_sum(numbers)}")
    print(f"Product: {calculate_product(numbers)}")
    
    print("\n" + "=" * 60)
    print("This application demonstrates:")
    print("1. Encryption of source code using AES-256")
    print("2. Homomorphic operations on encrypted data")
    print("3. Search in encrypted files")
    print("4. Working with encrypted codebase")
    print("=" * 60)


if __name__ == "__main__":
    main()
