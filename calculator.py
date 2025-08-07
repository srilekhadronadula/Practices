def calculator():
    print("Simple Calculator")
    while True:
        print("\nSelect operation:")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("5. Exit")
        
        try:
            choice = int(input("Enter choice (1/2/3/4/5): "))
            if choice == 5:
                print("Exiting the calculator. Goodbye!")
                break  # Exit the loop if the user selects 5
            
            if choice not in [1, 2, 3, 4]:
                print("Invalid choice! Please select a valid option.")
                continue  # If invalid, prompt the user again
            
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == 1:
                result = num1 + num2
                operation = "+"
            elif choice == 2:
                result = num1 - num2
                operation = "-"
            elif choice == 3:
                result = num1 * num2
                operation = "*"
            elif choice == 4:
                if num2 == 0:
                    print("Error! Division by zero is not allowed.")
                    continue  # Skip this operation and ask for input again
                result = num1 / num2
                operation = "/"

            print(f"{num1} {operation} {num2} = {result}")
        
        except ValueError:
            print("Invalid input! Please enter numeric values.")

# Run the calculator
calculator()
