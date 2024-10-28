import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector

# Database connection
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Naitik121",
            database="movie_booking"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# Login function
def login():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Username and Password required")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Success", "Login successful!")
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Error", "Invalid credentials")

    cursor.close()
    conn.close()

# Ticket booking function
def book_ticket():
    name = name_entry.get()
    movie = movie_var.get()
    time = time_var.get()
    tickets = ticket_var.get()
    seat = seat_var.get()
    price = price_var.get()

    if not name or not movie or not time or not tickets or not seat or not price:
        messagebox.showerror("Error", "All fields must be filled!")
        return

    try:
        tickets = int(tickets)
        price = float(price)
    except ValueError:
        messagebox.showerror("Error", "Tickets and Price must be valid numbers!")
        return

    conn = connect_db()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        sql = "INSERT INTO tickets (name, movie, time, tickets, seat, price) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (name, movie, time, tickets, seat, price)
        cursor.execute(sql, values)
        conn.commit()
        messagebox.showinfo("Success", "Ticket booked successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# View bookings function
def view_bookings():
    view_window = tk.Toplevel(root)
    view_window.title("View Bookings")
    view_window.geometry("700x400")
    view_window.config(bg="#121212")

    columns = ("ID", "Name", "Movie", "Time", "Tickets", "Seat", "Price")
    tree = ttk.Treeview(view_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(fill="both", expand=True)

    conn = connect_db()
    if conn is None:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

    cursor.close()
    conn.close()

    def delete_booking():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a booking to delete")
            return

        booking_id = tree.item(selected_item)['values'][0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tickets WHERE id=%s", (booking_id,))
        conn.commit()
        cursor.close()
        conn.close()

        tree.delete(selected_item)
        messagebox.showinfo("Success", "Booking deleted successfully!")

    def modify_booking():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a booking to modify")
            return

        booking_id = tree.item(selected_item)['values'][0]
        modify_window = tk.Toplevel(view_window)
        modify_window.title("Modify Booking")
        modify_window.geometry("400x300")
        modify_window.config(bg="#252525")

        tk.Label(modify_window, text="Name:", font=("Arial", 12), fg="white", bg="#252525").pack(anchor="w", padx=10, pady=5)
        new_name = tk.Entry(modify_window)
        new_name.pack(fill="x", padx=10)

        tk.Label(modify_window, text="Movie:", font=("Arial", 12), fg="white", bg="#252525").pack(anchor="w", padx=10, pady=5)
        new_movie = tk.Entry(modify_window)
        new_movie.pack(fill="x", padx=10)

        tk.Label(modify_window, text="Time:", font=("Arial", 12), fg="white", bg="#252525").pack(anchor="w", padx=10, pady=5)
        new_time = tk.Entry(modify_window)
        new_time.pack(fill="x", padx=10)

        tk.Label(modify_window, text="Tickets:", font=("Arial", 12), fg="white", bg="#252525").pack(anchor="w", padx=10, pady=5)
        new_tickets = tk.Entry(modify_window)
        new_tickets.pack(fill="x", padx=10)

        tk.Label(modify_window, text="Seat:", font=("Arial", 12), fg="white", bg="#252525").pack(anchor="w", padx=10, pady=5)
        new_seat = tk.Entry(modify_window)
        new_seat.pack(fill="x", padx=10)

        tk.Label(modify_window, text="Price:", font=("Arial", 12), fg="white", bg="#252525").pack(anchor="w", padx=10, pady=5)
        new_price = tk.Entry(modify_window)
        new_price.pack(fill="x", padx=10)

        def update_booking():
            name = new_name.get()
            movie = new_movie.get()
            time = new_time.get()
            tickets = new_tickets.get()
            seat = new_seat.get()
            price = new_price.get()

            if not name or not movie or not time or not tickets or not seat or not price:
                messagebox.showerror("Error", "All fields must be filled!")
                return

            try:
                tickets = int(tickets)
                price = float(price)
            except ValueError:
                messagebox.showerror("Error", "Tickets and Price must be valid numbers!")
                return

            conn = connect_db()
            cursor = conn.cursor()
            sql = "UPDATE tickets SET name=%s, movie=%s, time=%s, tickets=%s, seat=%s, price=%s WHERE id=%s"
            values = (name, movie, time, tickets, seat, price, booking_id)
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()

            tree.item(selected_item, values=(booking_id, name, movie, time, tickets, seat, price))
            messagebox.showinfo("Success", "Booking updated successfully!")
            modify_window.destroy()

        tk.Button(modify_window, text="Update Booking", command=update_booking, bg="#1db954", fg="white").pack(pady=10)

    tk.Button(view_window, text="Delete Booking", command=delete_booking, bg="#ff1744", fg="white").pack(side="left", padx=10, pady=10)
    tk.Button(view_window, text="Modify Booking", command=modify_booking, bg="#1db954", fg="white").pack(side="right", padx=10, pady=10)

# Main window after login
def open_main_window():
    global root
    root = tk.Tk()
    root.title("Movie Ticket Booking")
    root.geometry("800x600")

    bg_image = Image.open("background.jpg")  
    bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    frame = tk.Frame(root, bg="#000000", bd=5)
    frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.8, anchor="n")

    title_label = tk.Label(frame, text="Movie Ticket Booking System", font=("Helvetica", 20, "bold"), bg="#000000", fg="white")
    title_label.pack(pady=10)

    tk.Label(frame, text="Name:", font=("Arial", 12), fg="white", bg="#000000").pack(anchor="w", padx=10)
    global name_entry
    name_entry = tk.Entry(frame)
    name_entry.pack(fill="x", padx=10, pady=5)

    tk.Label(frame, text="Select Movie:", font=("Arial", 12), fg="white", bg="#000000").pack(anchor="w", padx=10)
    global movie_var
    movie_var = tk.StringVar()
    movies = ["Inception", "The Dark Knight", "Interstellar", "Dunkirk"]
    movie_dropdown = tk.OptionMenu(frame, movie_var, *movies)
    movie_dropdown.pack(fill="x", padx=10, pady=5)

    tk.Label(frame, text="Select Time:", font=("Arial", 12),
    fg="white", bg="#000000").pack(anchor="w", padx=10)
    global time_var
    time_var = tk.StringVar()
    times = ["10:00 AM", "1:00 PM", "4:00 PM", "7:00 PM", "10:00 PM"]
    time_dropdown = tk.OptionMenu(frame, time_var, *times)
    time_dropdown.pack(fill="x", padx=10, pady=5)

    tk.Label(frame, text="Number of Tickets:", font=("Arial", 12), fg="white", bg="#000000").pack(anchor="w", padx=10)
    global ticket_var
    ticket_var = tk.StringVar()
    ticket_entry = tk.Entry(frame, textvariable=ticket_var)
    ticket_entry.pack(fill="x", padx=10, pady=5)

    tk.Label(frame, text="Select Seat:", font=("Arial", 12), fg="white", bg="#000000").pack(anchor="w", padx=10)
    global seat_var
    seat_var = tk.StringVar()
    seats = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]
    seat_dropdown = tk.OptionMenu(frame, seat_var, *seats)
    seat_dropdown.pack(fill="x", padx=10, pady=5)

    tk.Label(frame, text="Ticket Price:", font=("Arial", 12), fg="white", bg="#000000").pack(anchor="w", padx=10)
    global price_var
    price_var = tk.StringVar()
    price_entry = tk.Entry(frame, textvariable=price_var)
    price_entry.pack(fill="x", padx=10, pady=5)

    # Buttons
    button_frame = tk.Frame(frame, bg="#000000")
    button_frame.pack(fill="x", pady=20)

    book_button = tk.Button(button_frame, text="Book Ticket", command=book_ticket, bg="#1db954", fg="white", font=("Arial", 12, "bold"))
    book_button.pack(side="left", padx=10)

    view_button = tk.Button(button_frame, text="View Bookings", command=view_bookings, bg="#1db954", fg="white", font=("Arial", 12, "bold"))
    view_button.pack(side="left", padx=10)

    exit_button = tk.Button(button_frame, text="Exit", command=root.quit, bg="#ff1744", fg="white", font=("Arial", 12, "bold"))
    exit_button.pack(side="right", padx=10)

    root.mainloop()

# Login window
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("400x300")

tk.Label(login_window, text="Username", font=("Arial", 12)).pack(pady=10)
username_entry = tk.Entry(login_window)
username_entry.pack(pady=5)

tk.Label(login_window, text="Password", font=("Arial", 12)).pack(pady=10)
password_entry = tk.Entry(login_window, show="*")
password_entry.pack(pady=5)

login_button = tk.Button(login_window, text="Login", command=login, bg="#1db954", fg="white", font=("Arial", 12, "bold"))
login_button.pack(pady=20)

login_window.mainloop()
