import mysql.connector as mysql  # impor lib mysql connector

# fungsi untuk menghubungkan ke mysql


def connect_to_database():
    try:
        connection = mysql.connect(
            host='localhost',
            user='root',
            password='',
            database='dbperpus',
            port=3310
        )
        return connection

    except mysql.Error as err:  # menangkap error pada mysql
        print(f"Error: {err}")  # print error

# membuat fungsi menu


def menu():
    # menampilkan pilihan yang
    print('===== [1] Tampilkan Data Buku =====')
    print('===== [2] Mengedit Data Buku =====')
    print('===== [3] Menambah Data Buku =====')
    print('===== [4] Menghapus Data Buku =====')

    choice = input(' Masukkan pilihan anda: ')   # meminta user input pilihan

    if choice == '1':
        tampilkan_data_buku()     # jika pilihan = 1 maka tampilkan data buku
    elif choice == '2':
        edit_data_buku()        # jika pilihan = 2 maka tampilkan data buku
    elif choice == '3':
        tambah_data_buku()         # jika pilihan = 3 maka tampilkan data buku
    elif choice == '4':
        hapus_data_buku()      # jika pilihan = 4 maka tampilkan data buku
    else:
        # jika pilihan tidak tidak valid maka print
        print("===== Invalid input! =====")

# membuat fungsi registrasi


def register():
    connection = connect_to_database()  # memanggil fungsi untuk koneksi ke database
    if not connection:  # jika koneksi gagal print kode di bawah
        print("===== Error Connection! =====")

    cursor = connection.cursor()  # digunakan untuk memanggil / mengeksekusi kode mysql

    # meminta user untuk mengisikan username dan password
    username = input('Enter a new username: ')
    password = input('Enter a new password: ')

    try:    # menggunakan try-except untuk cek apakah username / akun sudah ada
        # Cek apakah username sudah ada
        cursor.execute("SELECT * FROM users WHERE username = %s",
                       (username,))  # memilih tabel users
        existing_user = cursor.fetchone()   # return/menangkap baris pertama

        if existing_user:   # jika kondisi ini terpenuhi jalankan kode dibawahnya
            print(
                '===== Username sudah ada! ===== \n ===== Pilih username yang lain. =====')
        else:   # jika kondisi sebelumnya tidk terpenuhi jalankan kode ini
            # input data user baru
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))  # input data baru ke tabel users
            cursor.execute(
                "UPDATE users SET username = %s, password = %s WHERE id_users = %s")  # update perubahan ke databse
            connection.commit()  # commit perubahan
            # print output jika akun tlah dibuat
            print('===== Akun berhasil dibuat! =====')

    except mysql.Error as err:    # jika terjadi error maka tampilkan error
        print(f"Error: {err}")

    finally:       # menutup database cursor
        if cursor:  # jika cursor ada maka jjalankan kode di bawah
            cursor.close()
        if connection:  # jjika koneksi ada maka jalankan kode di bawah
            connection.close()

# membuat fungsi login


def login():
    connection = connect_to_database()  # memanggil fungsi ke database
    if not connection:  # jika koneksi gagal print kode di bawah
        print("===== Error Connection! =====")

    cursor = connection.cursor()    # digunakan untuk memanggil / mengeksekusi kode mysql

    # meminta user untuk mengisikan username dan password
    username = input('Enter your username: ')
    password = input('Enter your password: ')

    try:
        # menggunakan try-except untuk cek apakah username / akun sudah ada
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s", (username, password))  # memilih tabel users
        user = cursor.fetchone()    # return/menangkap baris pertama

        if user:    # jjiika kondisi terpenuhi user akan menuju menu
            print('===== Selamat anda berhasil login! =====')
            menu()
        else:   # jika kondisi tidak terpenuhi maka kode di bawah akan diekskusi
            print('===== Username atau Password salah! =====')

    except mysql.Error as err:  # jika terjadi error maka tampilkan error
        print(f"Error: {err}")

    finally:       # menutup database cursor
        if cursor:  # jika cursor ada maka jjalankan kode di bawah
            cursor.close()
        if connection:  # jjika koneksi ada maka jalankan kode di bawah
            connection.close()

# membuat fungsi untuk menampilkan data buku


def tampilkan_data_buku():
    connection = connect_to_database()  # memanggil fungsi ke database
    if not connection:  # jika koneksi gagal print kode di bawah
        print("===== Error Connection! =====")

    cursor = connection.cursor()    # digunakan untuk memanggil / mengeksekusi kode mysql

    try:
        cursor.execute(
            "SELECT * FROM data_buku")    # memilih tabel dgn nama kolom tertentu
        buku = cursor.fetchall()    # return/tangkap semua baris dlm tabel

        if buku:    # jika data buku ada
            for x in buku:  # looping sebanyak data buku
                print(
                    f"No: {x[0]} | Judul Buku: {x[1]} | Penulis: {x[2]} | Penerbit: {x[3]} | Tahun Terbit: {x[4]} |")  # tampilkan data buku
        else:   # jika tidak ada data buku
            print("===== Data buku tidak ditemukan =====")

    except mysql.Error as err:    # jika terjadi error maka tampilkan error
        print(f"Error: {err}")

    finally:       # menutup database cursor
        if cursor:  # jika cursor ada maka jjalankan kode di bawah
            cursor.close()
        if connection:  # jika koneksi ada maka jalankan kode di bawah
            connection.close()

# fungsi mengedit data buku


def edit_data_buku():
    connection = connect_to_database()  # memanggil fungsi ke database
    if not connection:  # jika koneksi gagal print kode di bawah
        print("===== Error Connection! =====")

    cursor = connection.cursor()    # digunakan untuk memanggil / mengeksekusi kode mysql

    tampilkan_data_buku()   # memanggil fungsi data buku

    try:
        # user input nomor data buku
        select_book = int(input("Masukkan nomor buku yang akan di edit: "))
    except ValueError:  # jika input yang dimasukkan tidak sesuai
        print("===== Input invalid!. Masukkan nomor yang tersedia =====.")

    try:
        # memilih semua data dalam table data_buku
        cursor.execute("SELECT * FROM data_buku")
        books = cursor.fetchall()   # tangkap semua baris

        # jika select_book lebih besar atau sama dengan satu dan lebih kecil dari panjang data buku
        if 1 <= select_book <= len(books):
            # kurangi satu karena list pertama yaitu 0
            book_num = books[select_book - 1]
            # tampilkan data buku yang akan di edit
            print(
                f"No: {book_num[0]} | Judul Buku: {book_num[1]} | Penulis: {book_num[2]} | Penerbit: {book_num[3]} | Tahun Terbit: {book_num[3]} | ")

            # input data buku baru
            judul = input("Masukkan judul buku: ")
            penulis = input("Masukkan nama penulis buku: ")
            penerbit = input("Masukkan nama penerbit buku: ")
            tahun_terbit = input("Masukkan tahun terbit buku: ")

        # insert data buku baru ke database
            cursor.execute("INSERT INTO data_buku (judul_buku, penulis, penerbit, tahun_terbit) VALUES (%s, %s, %s, %s)",
                           (judul, penulis, penerbit, tahun_terbit))

        # commit perubahan ke database
            connection.commit()
            print("===== Data baru berhasil ditambahkan! =====")

        else:   # jjika input nomor buku salah maka jalankan kode di bawah
            print("===== Nomor Buku Invalid! =====")

    except mysql.Error as err:    # jika terjadi error maka tampilkan error
        print(f"Error: {err}")

    finally:       # menutup database cursor
        if cursor:  # jika cursor ada maka jjalankan kode di bawah
            cursor.close()
        if connection:  # jika koneksi ada maka jalankan kode di bawah
            connection.close()

# menambah data buku


def tambah_data_buku():
    connection = connect_to_database()  # memanggil fungsi ke database
    if not connection:  # jika koneksi gagal print kode di bawah
        print("===== Error Connection! =====")

    cursor = connection.cursor()    # digunakan untuk memanggil / mengeksekusi kode mysql

    try:
        tampilkan_data_buku()   # menampilkan data buku

        # input user untuk data buku baru
        judul = input("Masukkan judul buku: ")
        penulis = input("Masukkan nama penulis buku: ")
        penerbit = input("Masukkan nama penerbit buku: ")
        tahun_terbit = input("Masukkan tahun terbit buku: ")

        # insert data buku baru ke database
        cursor.execute("INSERT INTO data_buku (judul_buku, penulis, penerbit, tahun_terbit) VALUES (%s, %s, %s, %s)",
                       (judul, penulis, penerbit, tahun_terbit))

        # commit perubahan ke databae
        connection.commit()
        print("===== Data baru berhasil ditambahkan! =====")

    except mysql.Error as err:    # jika terjadi error maka tampilkan error
        print(f"Error: {err}")

    finally:       # menutup database cursor
        if cursor:  # jika cursor ada maka jjalankan kode di bawah
            cursor.close()
        if connection:  # jika koneksi ada maka jalankan kode di bawah
            connection.close()


def hapus_data_buku():
    connection = connect_to_database()  # Connect to the database
    if not connection:  # If connection fails, print the error message
        print("===== Error Connection! =====")
        return  # Return from the function if the connection is not successful

    cursor = connection.cursor()  # Create a cursor to execute MySQL queries

    try:
        tampilkan_data_buku()  # Display book data

        try:
            # User input for the book number to be deleted
            select_book = int(input("Masukkan nomor buku yang akan dihapus: "))
        except ValueError:  # Handle invalid input
            print(
                "===== Input Invalid! =====\n===== Mohon masukkan nomor yang tersedia! =====")
            return  # Return from the function if input is invalid

        # Fetch all data from the data_buku table
        cursor.execute("SELECT * FROM data_buku")
        books = cursor.fetchall()

        # Check if the selected book number is within a valid range
        if 1 <= select_book <= len(books):
            # Adjust the index to match the list (subtract 1)
            book_num = books[select_book - 1]
            # Display the book data to be deleted
            print(
                f"No: {book_num[0]} | Judul Buku: {book_num[1]} | Penulis: {book_num[2]} | Penerbit: {book_num[3]} | Tahun Terbit: {book_num[4]}")

            # Ask for confirmation before deletion
            konfirmasi = input(
                "Anda yakin ingin menghapus data buku ini? (y/n): ").lower()

            if konfirmasi == "y":
                # Delete the book data from the database
                delete_query = "DELETE FROM data_buku WHERE nomor_buku = %s"
                cursor.execute(delete_query, (book_num[0],))

                connection.commit()  # Commit changes to the database
                print("Book deleted successfully!")
            elif konfirmasi == "n":
                print("Data tidak dihapus")
            else:
                print("Invalid input")

        else:
            print("Invalid nomor buku.")

    except mysql.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the database cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# input user untuk login/registrasi
print('Type "login" if you already have an account')
print('Type "regis" if you don\'t have an account yet')
choice = input('Enter your choice (login/regis): ')

# cek pilihan user
if choice == 'regis':
    register()
elif choice == 'login':
    login()
else:
    print('Invalid choice')
