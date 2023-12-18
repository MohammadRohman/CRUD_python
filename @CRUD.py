import mysql.connector as mysql  # impor lib mysql connector
import re
from datetime import datetime, timedelta

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

#
# fungsi meminjam buku

# membuat fungsi menu


def menu():
    # menampilkan pilihan yang
    print('===== [1] Tampilkan Data Buku =====')
    print('===== [2] Mengedit Data Buku =====')
    print('===== [3] Menambah Data Buku =====')
    print('===== [4] Menghapus Data Buku =====')
    print('===== [5] Meminjam Data Buku =====')

    choice = input(' Masukkan pilihan anda: ')   # meminta user input pilihan

    if choice == '1':
        tampilkan_data_buku()     # jika pilihan = 1 maka tampilkan data buku
    elif choice == '2':
        edit_data_buku()        # jika pilihan = 2 maka tampilkan data buku
    elif choice == '3':
        tambah_data_buku()         # jika pilihan = 3 maka tampilkan data buku
    elif choice == '4':
        hapus_data_buku()      # jika pilihan = 4 maka tampilkan data buku
    elif choice == '5':
        pinjam_buku()      # jika pilihan = 4 maka tampilkan data buku
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
        if cursor:  # jika cursor ada maka jalankan kode di bawah
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

# menambahkan fungsi peminjaman buku


def pinjam_buku():
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT id_buku, judul_buku FROM data_buku")
        books = cursor.fetchall()

        if books:
            print("===== Data Buku Tersedia =====")
            for book in books:
                print(f"- ID Buku: {book[0]} | Judul Buku: {book[1]}")

            print("\n===== Menu =====")
            print("1. Cari Buku")
            print("2. Pinjam Buku")
            choice = input("Masukkan pilihan (1/2): ")

            if choice == '1':
                judul_cari = input("Masukkan kata kunci pencarian: ")
                matched_books = []
                for book in books:
                    match = re.search(judul_cari, book[1], re.IGNORECASE)
                    if match:
                        matched_books.append(book)
                        print(f"- ID Buku: {book[0]} | Judul Buku: {book[1]}")

                if matched_books:
                    judul_buku = input(
                        "Masukkan judul buku yang ingin dipinjam: ")
                    matched_book_ids = [
                        book[0] for book in matched_books if judul_buku.lower() in book[1].lower()]

                    if matched_book_ids:
                        id_buku = matched_book_ids[0]

                        nama_peminjam = input("Masukkan nama peminjam: ")
                        no_telepon = input("Masukkan nomor telepon: ")
                        alamat = input("Masukkan alamat: ")

                        # Tanggal pinjam
                        tanggal_pinjam = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        # Menghitung tanggal pengembalian (contoh: 7 hari setelah peminjaman)
                        tanggal_pengembalian = (
                            datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")

                        # Menambah data peminjam ke tabel peminjaman dengan tanggal pengembalian
                        cursor.execute("INSERT INTO data_pinjam (nama_peminjam, no_telepon, alamat, id_buku, tanggal_pinjam, tanggal_pengembalian) VALUES (%s, %s, %s, %s, %s, %s)",
                                       (nama_peminjam, no_telepon, alamat, id_buku, tanggal_pinjam, tanggal_pengembalian))

                        # Ubah status ketersediaan buku menjadi 'Not Available'
                        cursor.execute("UPDATE data_buku SET ketersediaan = 'Not Available' WHERE id_buku = %s",
                                       (id_buku,))
                        connection.commit()
                        print("===== Peminjaman Buku Berhasil! =====")
                    else:
                        print("Judul buku tidak valid atau buku tidak ditemukan.")

                else:
                    print("Tidak ada buku yang sesuai dengan pencarian.")

            elif choice == '2':
                id_buku = input("Masukkan ID buku yang ingin dipinjam: ")
                nama_peminjam = input("Masukkan nama peminjam: ")
                no_telepon = input("Masukkan nomor telepon: ")
                alamat = input("Masukkan alamat: ")

                # Tanggal pinjam
                tanggal_pinjam = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Menghitung tanggal pengembalian (contoh: 7 hari setelah peminjaman)
                tanggal_pengembalian = (
                    datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")

                # Menambah data peminjam ke tabel peminjaman dengan tanggal pengembalian
                cursor.execute("INSERT INTO data_pinjam (nama_peminjam, no_telepon, alamat, id_buku, tanggal_pinjam, tanggal_pengembalian) VALUES (%s, %s, %s, %s, %s, %s)",
                               (nama_peminjam, no_telepon, alamat, id_buku, tanggal_pinjam, tanggal_pengembalian))

                # Ubah status ketersediaan buku menjadi 'Not Available'
                cursor.execute("UPDATE data_buku SET ketersediaan = 'Not Available' WHERE id_buku = %s",
                               (id_buku,))
                connection.commit()
                print("===== Peminjaman Buku Berhasil! =====")

            else:
                print("Pilihan tidak valid!")

        else:
            print("Tidak ada data buku tersedia.")

    except mysql.Error as err:
        print(f"Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Contoh pemanggilan fungsi pinjam_buku()

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

            # pilihan untuk mengedit data buku
            print("===== Pilih atribut yang ingin diedit: =====")
            print('===== [1] Judul Buku =====')
            print('===== [2] Penulis =====')
            print('===== [3] Penerbit =====')
            print('===== [4] Tahun Terbit =====')
            print('===== [5] Semua Atribut =====')

            try:
                choice = int(
                    input("Masukkan nomor atribut yang ingin diedit: "))
            except ValueError:
                print("===== Invalid input! =====")

            if choice == 5:
                # jika user memilih untuk mengedit semua atribut
                judul = input("Masukkan judul buku baru: ")
                penulis = input("Masukkan nama penulis buku baru: ")
                penerbit = input("Masukkan nama penerbit buku baru: ")
                tahun_terbit = input("Masukkan tahun terbit buku baru: ")
                # insert data buku baru ke database
                cursor.execute("INSERT INTO data_buku (judul_buku, penulis, penerbit, tahun_terbit) VALUES (%s, %s, %s, %s)",
                               (judul, penulis, penerbit, tahun_terbit))

            elif 1 <= choice <= 4:
                # jika user ingin mengedit atribut tertentu
                attribute_names = ["judul_buku",
                                   "penulis", "penerbit", "tahun_terbit"]
                attribute_edit = attribute_names[choice - 1]
                new_value = input(f"Masukkan {attribute_edit} baru: ")

                # Update the specific attribute in the database
                cursor.execute(f"UPDATE data_buku SET {attribute_edit} = %s WHERE id_buku = %s",
                               (new_value, book_num[0]))
            else:
                print("===== Pilihan Invalid! =====")
                return

            # commit perubahan ke database
            connection.commit()
            print("===== Data baru berhasil ditambahkan! =====")

        else:   # jika input nomor buku salah maka jalankan kode di bawah
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
        print("===== Menambah Data Buku =====")
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

# fungsi menghapus data buku


def hapus_data_buku():
    connection = connect_to_database()  # memanggil fungsi ke database
    if not connection:  # jika koneksi gagal print kode di bawah
        print("===== Error Connection! =====")

    cursor = connection.cursor()  # digunakan untuk memanggil / mengeksekusi kode mysql

    try:
        tampilkan_data_buku()  # menampilkan data buku

        try:
            # input untuk menghapus data buku
            select_book = int(input("Masukkan nomor buku yang akan dihapus: "))
        except ValueError:  # menangani invalid input
            print(
                "===== Input Invalid! =====\n===== Mohon masukkan nomor yang tersedia! =====")

        # mengambil data dari table data_buku
        cursor.execute("SELECT * FROM data_buku")
        books = cursor.fetchall()   # mengambil seluruh baris dalat data_buku

        # cek apakah input dalam range
        if 1 <= select_book <= len(books):
            # menyesuaikan dengan index ( - 1)
            book_num = books[select_book - 1]
            # Tampilkan buku yang akan dihapus
            print(
                f"No: {book_num[0]} | Judul Buku: {book_num[1]} | Penulis: {book_num[2]} | Penerbit: {book_num[3]} | Tahun Terbit: {book_num[4]}")

            # konfirmasi sebelum dihapus
            konfirmasi = input(
                "Anda yakin ingin menghapus data buku ini? (y/n): ").lower()

            if konfirmasi == "y":
                # menghapus buku dari database
                delete_query = "DELETE FROM data_buku WHERE judul_buku = %s"
                cursor.execute(delete_query, (book_num[1],))

                connection.commit()  # Commit perubahan ke database
                print("===== Buku berhasil dihapus! =====")
            elif konfirmasi == "n":
                print("===== Data tidak dihapus =====")
            else:
                print("===== Invalid input =====")

        else:
            print("====== Invalid nomor buku. =====")

    except mysql.Error as err:    # jika terjadi error maka tampilkan error
        print(f"Error: {err}")

    finally:       # menutup database cursor
        if cursor:  # jika cursor ada maka jalankan kode di bawah
            cursor.close()
        if connection:  # jika koneksi ada maka jalankan kode di bawah
            connection.close()


# input user untuk login/registrasi
print('Ketik login jika sudah memiliki akun')
print('Ketik regis jika belum memiliki akun')
choice = input('Masukkan pilihan anda (login/regis): ')

# cek pilihan user
if choice == 'regis':
    register()
elif choice == 'login':
    login()
else:
    print('Invalid choice')
