#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contact Manager - CRUD Application
MacOS optimized version
"""

import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class ContactManager:
    def __init__(self):
        self.contacts = []
        self.filename = "friendsContact.txt"
        self.load_contacts()
    
    def load_contacts(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as file:
                    self.contacts = json.load(file)
        except Exception as e:
            print(f"Error al cargar contactos: {e}")
            self.contacts = []
    
    def save_contacts(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(self.contacts, file, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar contactos: {e}")
    
    def create_contact(self, name, phone):
        contact_id = len(self.contacts) + 1
        contact = {"id": contact_id, "name": name, "phone": phone}
        self.contacts.append(contact)
        self.save_contacts()
        return contact
    
    def find_contact(self, name):
        for contact in self.contacts:
            if contact["name"].lower() == name.lower():
                return contact
        return None
    
    def update_contact(self, contact_id, name, phone):
        for contact in self.contacts:
            if contact["id"] == contact_id:
                contact["name"] = name
                contact["phone"] = phone
                self.save_contacts()
                return True
        return False
    
    def delete_contact(self, contact_id):
        for i, contact in enumerate(self.contacts):
            if contact["id"] == contact_id:
                del self.contacts[i]
                self.save_contacts()
                return True
        return False
    
    def get_all_contacts(self):
        return self.contacts

class ContactGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Administrador de Contactos")
        self.root.geometry("550x300")  # Tamaño inicial compacto
        self.root.configure(bg='#4a4a4a')
        
        self.contact_manager = ContactManager()
        self.list_visible = False  # Estado de visibilidad de la lista
        self.setup_ui()
        self.center_window()
    
    def center_window(self):
        self.root.update_idletasks()
        width = 550
        height = 300 if not self.list_visible else 500  # Altura dinámica
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        # Título
        title = tk.Label(self.root, text="Administrador de Contactos", 
                        font=('Helvetica', 16, 'bold'), 
                        bg='#4a4a4a', fg='white')
        title.pack(pady=20)
        
        # Frame para campos
        fields_frame = tk.Frame(self.root, bg='#4a4a4a')
        fields_frame.pack(pady=10)
        
        # Campo Name
        name_frame = tk.Frame(fields_frame, bg='#4a4a4a')
        name_frame.pack(pady=8, fill='x', padx=40)
        
        tk.Label(name_frame, text="Nombre:", font=('Helvetica', 12), 
                bg='#4a4a4a', fg='white', width=8, anchor='w').pack(side='left')
        
        self.name_entry = tk.Entry(name_frame, font=('Helvetica', 12), 
                                  bg='white', fg='black', insertbackground='black',
                                  relief='solid', bd=1)
        self.name_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        self.name_entry.insert(0, "Ingrese un nombre")
        self.name_entry.config(fg='gray')  # Inicializar placeholder en gris
        self.name_entry.bind('<FocusIn>', lambda e: self.on_focus_in(self.name_entry, "Ingrese un nombre"))
        self.name_entry.bind('<FocusOut>', lambda e: self.on_focus_out(self.name_entry, "Ingrese un nombre"))
        
        # Campo Number
        number_frame = tk.Frame(fields_frame, bg='#4a4a4a')
        number_frame.pack(pady=8, fill='x', padx=40)
        
        tk.Label(number_frame, text="Número:", font=('Helvetica', 12), 
                bg='#4a4a4a', fg='white', width=8, anchor='w').pack(side='left')
        
        self.phone_entry = tk.Entry(number_frame, font=('Helvetica', 12), 
                                   bg='white', fg='black', insertbackground='black',
                                   relief='solid', bd=1, validate='key')
        self.phone_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        self.phone_entry.insert(0, "Ingrese un número de teléfono")
        self.phone_entry.config(fg='gray')  # Inicializar placeholder en gris
        
        # Registrar función de validación para solo números
        vcmd = (self.root.register(self.validate_number), '%P')
        self.phone_entry.config(validatecommand=vcmd)
        
        self.phone_entry.bind('<FocusIn>', lambda e: self.on_focus_in(self.phone_entry, "Ingrese un número de teléfono"))
        self.phone_entry.bind('<FocusOut>', lambda e: self.on_focus_out(self.phone_entry, "Ingrese un número de teléfono"))
        
        # Frame para botones
        buttons_frame = tk.Frame(self.root, bg='#4a4a4a')
        buttons_frame.pack(pady=20)
        
        # Crear botones individuales con mejor visibilidad para macOS
        self.create_btn = tk.Button(buttons_frame, text="Create", command=self.create_contact,
                                   font=('Helvetica', 11, 'bold'), width=8, height=1,
                                   bg='white', fg='black', relief='raised', bd=2,
                                   activebackground='lightgray', activeforeground='black')
        self.create_btn.pack(side='left', padx=3)
        
        self.read_btn = tk.Button(buttons_frame, text="Read", command=self.read_contact,
                                 font=('Helvetica', 11, 'bold'), width=8, height=1,
                                 bg='white', fg='black', relief='raised', bd=2,
                                 activebackground='lightgray', activeforeground='black')
        self.read_btn.pack(side='left', padx=3)
        
        self.update_btn = tk.Button(buttons_frame, text="Update", command=self.update_contact,
                                   font=('Helvetica', 11, 'bold'), width=8, height=1,
                                   bg='white', fg='black', relief='raised', bd=2,
                                   activebackground='lightgray', activeforeground='black')
        self.update_btn.pack(side='left', padx=3)
        
        self.delete_btn = tk.Button(buttons_frame, text="Delete", command=self.delete_contact,
                                   font=('Helvetica', 11, 'bold'), width=8, height=1,
                                   bg='white', fg='black', relief='raised', bd=2,
                                   activebackground='lightgray', activeforeground='black')
        self.delete_btn.pack(side='left', padx=3)
        
        self.clear_btn = tk.Button(buttons_frame, text="Clear", command=self.clear_form,
                                  font=('Helvetica', 11, 'bold'), width=8, height=1,
                                  bg='white', fg='black', relief='raised', bd=2,
                                  activebackground='lightgray', activeforeground='black')
        self.clear_btn.pack(side='left', padx=3)
        
        # Frame para la lista de contactos (inicialmente oculto)
        self.list_frame = tk.LabelFrame(self.root, text="Lista de Contactos", 
                                       font=('Helvetica', 12, 'bold'), 
                                       bg='#4a4a4a', fg='white', 
                                       labelanchor='n', pady=10)
        # No empaquetamos inicialmente - se mostrará con Read
        
        # Crear Treeview para mostrar contactos
        columns = ('ID', 'Nombre', 'Teléfono')
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show='headings', height=8)
        
        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Teléfono', text='Teléfono')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Nombre', width=200, anchor='w')
        self.tree.column('Teléfono', width=200, anchor='w')
        
        # Scrollbar para la lista
        self.scrollbar = ttk.Scrollbar(self.list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        # Empaquetar treeview y scrollbar (dentro del frame, pero el frame está oculto)
        self.tree.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')
        
        # Bind para seleccionar contacto haciendo clic
        self.tree.bind('<<TreeviewSelect>>', self.on_contact_select)
    
    def on_focus_in(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='black')  # Texto negro sobre fondo blanco
    
    def on_focus_out(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg='gray')  # Placeholder en gris
        else:
            entry.config(fg='black')  # Mantener texto negro
    
    def validate_number(self, value):
        """Validar que solo se ingresen números, espacios, guiones y paréntesis"""
        if value == "" or value == "Ingrese un número de teléfono":
            return True
        
        # Permitir solo números, espacios, guiones, paréntesis y el signo +
        allowed_chars = "0123456789 ()-+"
        return all(char in allowed_chars for char in value)
    
    def get_entry_value(self, entry, placeholder):
        value = entry.get()
        return "" if value == placeholder else value.strip()
    
    def set_entry_value(self, entry, value, placeholder):
        entry.delete(0, tk.END)
        if value:
            entry.insert(0, value)
            entry.config(fg='black')  # Texto negro
        else:
            entry.insert(0, placeholder)
            entry.config(fg='gray')  # Placeholder gris
    
    def create_contact(self):
        name = self.get_entry_value(self.name_entry, "Ingrese un nombre")
        phone = self.get_entry_value(self.phone_entry, "Ingrese un número de teléfono")
        
        if not name or not phone:
            messagebox.showwarning("Advertencia", "Complete todos los campos")
            return
        
        # Validar que el teléfono tenga al menos algunos números
        digits_only = ''.join(filter(str.isdigit, phone))
        if len(digits_only) < 7:
            messagebox.showwarning("Advertencia", "El número debe tener al menos 7 dígitos")
            return
        
        if self.contact_manager.find_contact(name):
            messagebox.showwarning("Advertencia", f"Ya existe un contacto con el nombre '{name}'")
            return
        
        try:
            self.contact_manager.create_contact(name, phone)
            messagebox.showinfo("Éxito", f"Contacto '{name}' creado exitosamente")
            self.clear_form()
            # Solo actualizar lista si está visible
            if self.list_visible:
                self.refresh_contact_list()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
    
    def read_contact(self):
        name = self.get_entry_value(self.name_entry, "Ingrese un nombre")
        
        if name:
            # Si hay un nombre específico, buscar ese contacto
            contact = self.contact_manager.find_contact(name)
            if contact:
                info = f"Nombre: {contact['name']}\nTeléfono: {contact['phone']}"
                messagebox.showinfo("Información del Contacto", info)
                self.set_entry_value(self.name_entry, contact['name'], "Ingrese un nombre")
                self.set_entry_value(self.phone_entry, contact['phone'], "Ingrese un número de teléfono")
            else:
                messagebox.showinfo("No encontrado", f"No existe el contacto '{name}'")
        else:
            # Si no hay nombre específico, toggle la lista de contactos
            self.toggle_contact_list()
    
    def update_contact(self):
        name = self.get_entry_value(self.name_entry, "Ingrese un nombre")
        phone = self.get_entry_value(self.phone_entry, "Ingrese un número de teléfono")
        
        if not name or not phone:
            messagebox.showwarning("Advertencia", "Complete todos los campos")
            return
        
        # Validar que el teléfono tenga al menos algunos números
        digits_only = ''.join(filter(str.isdigit, phone))
        if len(digits_only) < 7:
            messagebox.showwarning("Advertencia", "El número debe tener al menos 7 dígitos")
            return
        
        contact = self.contact_manager.find_contact(name)
        if not contact:
            messagebox.showwarning("Advertencia", f"No existe el contacto '{name}'")
            return
        
        try:
            if self.contact_manager.update_contact(contact['id'], name, phone):
                messagebox.showinfo("Éxito", "Contacto actualizado exitosamente")
                self.clear_form()
                # Solo actualizar lista si está visible
                if self.list_visible:
                    self.refresh_contact_list()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
    
    def delete_contact(self):
        name = self.get_entry_value(self.name_entry, "Ingrese un nombre")
        
        if not name:
            messagebox.showwarning("Advertencia", "Ingrese un nombre para eliminar")
            return
        
        contact = self.contact_manager.find_contact(name)
        if not contact:
            messagebox.showwarning("Advertencia", f"No existe el contacto '{name}'")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el contacto '{name}'?"):
            try:
                if self.contact_manager.delete_contact(contact['id']):
                    messagebox.showinfo("Éxito", "Contacto eliminado exitosamente")
                    self.clear_form()
                    # Solo actualizar lista si está visible
                    if self.list_visible:
                        self.refresh_contact_list()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
    
    def clear_form(self):
        self.set_entry_value(self.name_entry, "", "Ingrese un nombre")
        self.set_entry_value(self.phone_entry, "", "Ingrese un número de teléfono")
    
    def refresh_contact_list(self):
        """Actualizar la lista de contactos"""
        # Limpiar lista actual
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar contactos actuales
        contacts = self.contact_manager.get_all_contacts()
        for contact in contacts:
            self.tree.insert('', 'end', values=(
                contact['id'],
                contact['name'],
                contact['phone']
            ))
    
    def on_contact_select(self, event):
        """Manejar selección de contacto en la lista"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item)['values']
            
            # Llenar formulario con los datos del contacto seleccionado
            self.set_entry_value(self.name_entry, values[1], "Ingrese un nombre")
            self.set_entry_value(self.phone_entry, values[2], "Ingrese un número de teléfono")
    
    def toggle_contact_list(self):
        """Mostrar u ocultar la lista de contactos"""
        if self.list_visible:
            # Ocultar la lista
            self.list_frame.pack_forget()
            self.list_visible = False
            # Cambiar el tamaño de la ventana a modo compacto
            self.root.geometry("550x300")
        else:
            # Mostrar la lista
            contacts = self.contact_manager.get_all_contacts()
            if not contacts:
                messagebox.showinfo("Sin contactos", "No hay contactos guardados")
                return
            
            # Actualizar la lista y mostrarla
            self.refresh_contact_list()
            self.list_frame.pack(pady=20, padx=20, fill='both', expand=True)
            self.list_visible = True
            # Cambiar el tamaño de la ventana para mostrar la lista
            self.root.geometry("550x500")

def main():
    root = tk.Tk()
    app = ContactGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
