import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import caesarCipher
import playfairCipher
import railFenceCipher
import vigenereCipher
import xorCipher

class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptography Algorithm Simulator")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)  # Set minimum window size
        self.root.resizable(True, True)
        
        # Store the result for copying
        self.result_text = ""
        
        # Key format descriptions
        self.key_formats = {
            "Caesar Cipher": "Enter a number (e.g., 3)",
            "Playfair Cipher": "Enter a word or phrase",
            "Rail Fence Cipher": "Enter a number > 1 (e.g., 3)",
            "Vigenère Cipher": "Enter a word (letters only)",
            "XOR Cipher": "Enter any text"
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Cryptography Algorithm Simulator", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Top section: Input and Result in the same area
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Left side - Input frame
        input_frame = ttk.LabelFrame(top_frame, text="Input", padding="10")
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        # Text input
        ttk.Label(input_frame, text="Enter plaintext:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.plaintext = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.plaintext, width=40).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Algorithm selection
        ttk.Label(input_frame, text="Select algorithm:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.algorithm = tk.StringVar()
        algorithms = ["Caesar Cipher", "Playfair Cipher", "Rail Fence Cipher", "Vigenère Cipher", "XOR Cipher"]
        algorithm_menu = ttk.Combobox(input_frame, textvariable=self.algorithm, values=algorithms, width=20, state="readonly")
        algorithm_menu.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        algorithm_menu.current(0)
        algorithm_menu.bind("<<ComboboxSelected>>", self.update_key_format)
        
        # Key input with format hint - using a consistent label now
        ttk.Label(input_frame, text="Enter key:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.key = tk.StringVar()
        self.key_entry = ttk.Entry(input_frame, textvariable=self.key, width=40)
        self.key_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Key format instruction
        self.key_format_var = tk.StringVar()
        self.key_format_var.set(self.key_formats["Caesar Cipher"])
        self.key_format_label = ttk.Label(input_frame, textvariable=self.key_format_var, 
                                       font=("Arial", 9, "italic"), foreground="gray")
        self.key_format_label.grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # Action buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Encrypt", command=self.encrypt).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Decrypt", command=self.decrypt).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear).pack(side=tk.LEFT, padx=5)
        
        # Right side - Result frame
        result_frame = ttk.LabelFrame(top_frame, text="Ciphertext", padding="10")
        result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Result display area
        result_display_frame = ttk.Frame(result_frame)
        result_display_frame.pack(fill=tk.X, expand=True, pady=5)
        
        self.result_display = ttk.Entry(result_display_frame, width=30, state="readonly")
        self.result_display.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ttk.Button(result_display_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(side=tk.RIGHT, padx=5)
        
        # Output and steps area
        output_frame = ttk.LabelFrame(main_frame, text="Step-by-Step Simulation", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=80, height=20)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.output_text.config(font=("Consolas", 10))
    
    def update_key_format(self, event=None):
        algorithm = self.algorithm.get()
        # Update only the key format instruction
        self.key_format_var.set(self.key_formats[algorithm])
        
    def encrypt(self):
        plaintext = self.plaintext.get().strip()
        key = self.key.get().strip()
        algorithm = self.algorithm.get()
        
        if not plaintext:
            messagebox.showerror("Error", "Please enter plaintext")
            return
            
        if not key:
            messagebox.showerror("Error", "Please enter a key")
            return
            
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"ENCRYPTION USING {algorithm.upper()}\n")
        self.output_text.insert(tk.END, f"Plaintext: {plaintext}\n")
        self.output_text.insert(tk.END, f"Key: {key}\n\n")
        
        try:
            if algorithm == "Caesar Cipher":
                result, steps = caesarCipher.encrypt(plaintext, key, True)
            elif algorithm == "Playfair Cipher":
                result, steps = playfairCipher.encrypt(plaintext, key, True)
            elif algorithm == "Rail Fence Cipher":
                result, steps = railFenceCipher.encrypt(plaintext, key, True)
            elif algorithm == "Vigenère Cipher":
                result, steps = vigenereCipher.encrypt(plaintext, key, True)
            elif algorithm == "XOR Cipher":
                result, steps = xorCipher.encrypt(plaintext, key, True)
                
            self.output_text.insert(tk.END, steps)
            self.output_text.insert(tk.END, f"\nFinal ciphertext: {result}\n")
            
            # Update result for copying
            self.result_text = result
            self.update_result_display()
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}")
            self.result_text = ""
            self.update_result_display()
    
    def decrypt(self):
        ciphertext = self.plaintext.get().strip()  # Using the plaintext field for ciphertext
        key = self.key.get().strip()
        algorithm = self.algorithm.get()
        
        if not ciphertext:
            messagebox.showerror("Error", "Please enter ciphertext in the plaintext field")
            return
            
        if not key:
            messagebox.showerror("Error", "Please enter a key")
            return
            
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"DECRYPTION USING {algorithm.upper()}\n")
        self.output_text.insert(tk.END, f"Ciphertext: {ciphertext}\n")
        self.output_text.insert(tk.END, f"Key: {key}\n\n")
        
        try:
            if algorithm == "Caesar Cipher":
                result, steps = caesarCipher.decrypt(ciphertext, key, True)
                self.result_text = result
            elif algorithm == "Playfair Cipher":
                result, steps, cleaned_result = playfairCipher.decrypt(ciphertext, key, True)
                # Store the cleaned result for copying
                self.result_text = cleaned_result
                # Add note to steps about the result formats
                steps += "\nNote: The result shown in the copy area is the version with X's removed."
            elif algorithm == "Rail Fence Cipher":
                result, steps = railFenceCipher.decrypt(ciphertext, key, True)
                self.result_text = result
            elif algorithm == "Vigenère Cipher":
                result, steps = vigenereCipher.decrypt(ciphertext, key, True)
                self.result_text = result
            elif algorithm == "XOR Cipher":
                result, steps = xorCipher.decrypt(ciphertext, key, True)
                self.result_text = result
                
            self.output_text.insert(tk.END, steps)
            if algorithm != "Playfair Cipher":
                self.output_text.insert(tk.END, f"\nFinal plaintext: {result}\n")
            
            self.update_result_display()
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}")
            self.result_text = ""
            self.update_result_display()
    
    def clear(self):
        self.plaintext.set("")
        self.key.set("")
        self.output_text.delete(1.0, tk.END)
        self.result_text = ""
        self.update_result_display()
    
    def update_result_display(self):
        # Enable the entry to update it
        self.result_display.config(state="normal")
        self.result_display.delete(0, tk.END)
        self.result_display.insert(0, self.result_text)
        # Set back to readonly
        self.result_display.config(state="readonly")
    
    def copy_to_clipboard(self):
        if not self.result_text:
            messagebox.showinfo("Copy", "No result to copy")
            return
        
        # Clear clipboard and append text
        self.root.clipboard_clear()
        self.root.clipboard_append(self.result_text)
        
        messagebox.showinfo("Copy", "Result copied to clipboard")

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()