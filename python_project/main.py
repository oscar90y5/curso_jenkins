from calculator import Calculator

if __name__ == '__main__':
    print(f"Versión {Calculator.version} de la calculadora.")

    op = input("¿Qué operación desea realizar? (suma o resta): ")

    if op == "suma":
        print("Suma")
        num1 = int(input("Introduzca el primer número: "))
        num2 = int(input("Introduzca el segundo número: "))
        print(f"La suma de {num1} y {num2} es {Calculator.add(num1, num2)}")
    elif op == "resta":
        print("Resta")
        num1 = int(input("Introduzca el primer número: "))
        num2 = int(input("Introduzca el segundo número: "))
        print(f"La resta de {num1} y {num2} es {Calculator.sub(num1, num2)}")