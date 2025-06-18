import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

variables = {}
arrays = {}
functions = {}
debug = False

def tokenize(line):
    words = line.split()
    tokens = []
    for word in words:
        if word in {"PRINT", "SET", "ARRAY", "SETARR", "GETARR", "FUNC", "CALL", "IF", "ELSE", "WHILE"}:
            tokens.append(("KEYWORD", word))
        elif word in {"+", "-", "*", "/", "=", "==", "!=", "<", ">"}:
            tokens.append(("OPERATOR", word))
        elif word.lstrip('-').isdigit():
            tokens.append(("NUMBER", word))
        else:
            tokens.append(("IDENTIFIER", word))
    return tokens

def evaluate_expression(a, op, b):
    x = int(a) if a.lstrip("-").isdigit() else variables.get(a, 0)
    y = int(b) if b.lstrip("-").isdigit() else variables.get(b, 0)
    if op == "+": return x + y
    if op == "-": return x - y
    if op == "*": return x * y
    if op == "/": return x // y if y != 0 else 0
    return 0

def evaluate_condition(a, op, b):
    x = int(a) if a.lstrip("-").isdigit() else variables.get(a, 0)
    y = int(b) if b.lstrip("-").isdigit() else variables.get(b, 0)
    if op == "==": return x == y
    if op == "!=": return x != y
    if op == "<": return x < y
    if op == ">": return x > y
    return False

def run_interpreter():
    code = input_text.get("1.0", tk.END).strip().split('\n')
    output_text.delete("1.0", tk.END)
    global variables, arrays, functions, debug
    variables, arrays, functions = {}, {}, {}

    i = 0
    while i < len(code):
        line = code[i].strip()
        tokens = tokenize(line)
        if not tokens:
            i += 1
            continue

        cmd = tokens[0][1]

        try:
            if cmd == "SET":
                var = tokens[1][1]
                lhs = tokens[3][1]
                if len(tokens) > 4 and tokens[4][0] == "OPERATOR":
                    op = tokens[4][1]
                    rhs = tokens[5][1]
                    variables[var] = evaluate_expression(lhs, op, rhs)
                else:
                    variables[var] = int(lhs) if lhs.lstrip("-").isdigit() else variables.get(lhs, 0)

            elif cmd == "PRINT":
                var = tokens[1][1]
                value = variables.get(var, var)
                output_text.insert(tk.END, f"{value}\n")

            elif cmd == "ARRAY":
                name = tokens[1][1]
                size = int(tokens[2][1])
                arrays[name] = [0] * size

            elif cmd == "SETARR":
                name = tokens[1][1]
                idx = int(tokens[2][1])
                val = int(tokens[3][1])
                arrays[name][idx] = val

            elif cmd == "GETARR":
                name = tokens[1][1]
                idx = int(tokens[2][1])
                output_text.insert(tk.END, f"{arrays[name][idx]}\n")

            elif cmd == "IF":
                var = tokens[1][1]
                op = tokens[2][1]
                val = tokens[3][1]
                condition = evaluate_condition(var, op, val)
                if_block = code[i + 1].strip()
                else_block = code[i + 2].strip() if i + 2 < len(code) and code[i + 2].strip().startswith("ELSE") else None
                if condition:
                    run_interpreter_line(if_block)
                elif else_block:
                    run_interpreter_line(else_block[5:].strip())
                i += 2 if else_block else 1

            elif cmd == "WHILE":
                var = tokens[1][1]
                op = tokens[2][1]
                val = tokens[3][1]
                body = code[i + 1].strip()
                while evaluate_condition(var, op, val):
                    run_interpreter_line(body)
                i += 1

        except Exception as e:
            messagebox.showerror("Error", f"Runtime error at line {i + 1}:\n{str(e)}")

        i += 1

def run_interpreter_line(line):
    global input_text
    input_text.delete("1.0", tk.END)
    input_text.insert("1.0", line)
    run_interpreter()

# GUI
root = tk.Tk()
root.title("🧠 Custom Mini-Interpreter")
root.geometry("850x650")
root.config(bg="#1e1e2f")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", padding=6, relief="flat", background="#4A90E2", foreground="white", font=("Segoe UI", 11, "bold"))
style.configure("TLabel", background="#1e1e2f", foreground="#ffffff", font=("Segoe UI", 12))
style.configure("TFrame", background="#1e1e2f")

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

ttk.Label(main_frame, text="Enter Code:").pack(anchor="w")
input_text = scrolledtext.ScrolledText(main_frame, height=15, width=100, font=("Consolas", 11), bg="#27293d", fg="white", insertbackground="white")
input_text.pack(pady=10)

ttk.Button(main_frame, text="▶ Run Code", command=run_interpreter).pack(pady=10)

ttk.Label(main_frame, text="Output:").pack(anchor="w")
output_text = scrolledtext.ScrolledText(main_frame, height=12, width=100, font=("Consolas", 11), bg="#1e1e2f", fg="lightgreen", insertbackground="white")
output_text.pack(pady=5)

root.mainloop()