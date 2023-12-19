import mysql.connector as mysql  # import lib mysql connector
import re   # import lib regex
from datetime import datetime, timedelta  # import lib date

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

    except mysql.Error as err:  # return error pada mysql
        print(f"Error: {err}")  # tampilkan error

# fungsi menu


def menu():
    # menampilkan pilihan yang tersedia
    print('===== [1] Tampilkan Data Buku =====')
    print('===== [2] Meminjam Data Buku =====')
    print('===== [3] Tampilkan Data Peminjam =====')
    print('===== [4] Mengedit Data Buku =====')
    print('===== [5] Menambah Data Buku =====')
    print('===== [6] Menghapus Data Buku =====')

    choice = input(' Masukkan pilihan anda: ')   # meminta user input pilihan

    if choice == '1':
        tampilkan_data_buku()     # jika pilihan = 1 maka tampilkan data buku
    elif choice == '2':
        pinjam_buku()        # jika pilihan = 2 maka tampilkan peminjaman buku
    elif choice == '3':
        data_peminjaman()         # jika pilihan = 3 maka tampilkan data peminjam buku
    elif choice == '4':
        edit_data_buku()      # jika pilihan = 4 maka tampilkan data editing data buku
    elif choice == '5':
        tambah_data_buku()      # jika pilihan = 5 maka tampilkan penambahan data buku
    elif choice == '6':
        hapus_data_buku()   # jika pilihan = 6 maka tampilkan penghapusan data buku
    else:
        # jika pilihan tidak tidak valid maka print
        print("===== Invalid input! =====")

# membuat fungsi registrasi


def register():
    # memanggil fungsi database lalu disimpan pada var connection
    connection = connect_to_database()
    cursor = connection.cursor()    # menggunakan fungsi cursor() sbg pointer

    cursor = connection.cursor()  # memanggil / mengeksekusi kode mysql

    # meminta user untuk mengisikan username dan password
    username = input('Enter a new username: ')
    password = input('Enter a new password: ')

    try:    # menggunakan try-except untuk cek apakah username / akun sudah ada
        # Cek apakah username sudah ada
        cursor.execute("SELECT * FROM users WHERE username = %s",
                       (username,))  # memilih username dari tabel users
        existing_user = cursor.fetchone()   # return/menangkap baris pertama

        if existing_user:   # jika kondisi ini terpenuhi jalankan kode dibawahnya
            print(
                '===== Username sudah ada! ===== \n ===== Pilih username yang lain. =====')
        else:   # jika kondisi sebelumnya tidk terpenuhi jalankan kode ini
            # input data user baru
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))  # input data baru (username & password) ke tabel users
            connection.commit()  # commit perubahan
            # tampilkan output jika akun tlah dibuat
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
    # memanggil fungsi database lalu disimpan pada var connection
    connection = connect_to_database()
    cursor = connection.cursor()    # menggunakan fungsi cursor() sbg pointer

    cursor = connection.cursor()    # digunakan untuk memanggil / mengeksekusi kode mysql

    # meminta user untuk mengisikan username dan password
    username = input('Enter your username: ')
    password = input('Enter your password: ')

    try:
        # menggunakan try-except untuk cek apakah username / akun sudah ada
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s", (username, password))  # memilih username & password dari tabel users
        user = cursor.fetchone()    # return/menangkap baris pertama

        if user:    # jika kondisi terpenuhi user akan menuju menu
            print('===== Selamat anda berhasil login! =====')
            menu()  # memanggil fungsi menu
        else:   # jika kondisi tidak terpenuhi maka kode di bawah akan ditampilkan
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
    # memanggil fungsi database lalu disimpan pada var connection
    connection = connect_to_database()
    cursor = connection.cursor()    # menggunakan fungsi cursor() sbg pointer

    try:
        cursor.execute(
            "SELECT * FROM data_buku")    # memilih tabel data_buku
        buku = cursor.fetchall()    # return/tangkap semua baris dlm tabel

        if buku:    # jika data buku ada
            for x in buku:  # looping sebanyak data buku
                print(
                    f"No: {str(x[0]):<2} | Judul Buku: {str(x[1]):<27} | Penulis: {str(x[2]):<20} | Penerbit: {str(x[3]):<25} | Tahun Terbit: {str(x[4]):<15} |")  # tampilkan data buku
        else:   # jika tidak ada data buku tampilkan kode di bawah
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
    # memanggil fungsi database lalu disimpan pada var connection
    connection = connect_to_database()
    cursor = connection.cursor()    # menggunakan fungsi cursor() sbg pointer

    try:
        # memilih id_buku dan, judul_buku dari tabel data_buku
        cursor.execute(
            "SELECT id_buku, judul_buku, ketersediaan FROM data_buku")
        buku_avail = cursor.fetchall()   # return semua baris dalam tabel

        if buku_avail:  # jika buku tersedia
            print("===== DATA BUKU YANG TERSEDIA =====")
            for i in buku_avail:  # looping sebanyak data buku yang tersedia
                print(
                    f"- No: {str(i[0]):<2} | Judul Buku: {str(i[1]):<37} | Ketersediaan: {str(i[2]):<13} |")    # tampilkan data buku

            # tempat menyimpan data buku yang akan dipinjam (sementara)
            temp_buku = []

            while True:  # looping infinite hingga kondisi false
                cari_judul = input(
                    "Masukkan judul buku yang ingin Anda pinjam: ")
                match_book = []  # tempat menyimpan buku yang dicari
                for x in buku_avail:    # loop sebnyk data buku
                    # mencari buku menggunakan fungsi regex
                    cari = re.search(cari_judul, x[1], re.IGNORECASE)
                    if cari:    # jika buku yang dicari ada
                        # jika ada tambahkan ke mathc_book
                        match_book.append(x)
                        print(
                            f"- ID Buku: {x[0]} | Judul Buku: {x[1]} | Ketersediaan: {x[2]}")   # tampilkan buku yang dicari

                if match_book:  # jika match book memiliki data
                    # judul_buku = input(
                    #     "Masukkan judul buku yang ingin Anda pinjam: ")  # meminta user untuk input buku yang ingin dipinja
                    cocok = [match_book for match_book in match_book if cari_judul.lower(
                    ) in match_book[1].lower()]  # list untuk memfilter berdasarkan buku apa yang dicari

                    if cocok:   # jika var cocok memiliki data
                        # assign buku pertama menjadi var buku_pilihan
                        buku_pilihan = cocok[0]
                        print(
                            f"Buku {buku_pilihan[1]} dipilih untuk dipinjam. Ketersediaan: {buku_pilihan[2]}")  # tampilkan buku pilihan dan ketersediaannya

                        tambah_buku = input(
                            "Apakah Anda ingin menambah buku lain? (y/n): ")    # meminta user untuk mencari buku lagi atau tidak
                        if tambah_buku.lower() == 'n':  # jika tidak
                            # tambahkan buku pilihan ke temp_buku
                            temp_buku.append(buku_pilihan)
                            break   # keluar dari loop
                        elif tambah_buku.lower() == 'y':    # jika ya tambahkan buku pertama ke temp_buku
                            temp_buku.append(buku_pilihan)
                        else:
                            # jika memilih pilihan lain tampilkan
                            print("Pilihan tidak valid.")
                    else:
                        # jika memilih pilihan lain tampilkan
                        print("Judul buku tidak valid atau buku tidak ditemukan.")
                else:
                    # jika memilih pilihan lain tampilkan
                    print("Tidak ada buku yang sesuai dengan pencarian.")

            if temp_buku:   # jika temp_buku memiliki data
                # user inputkan data diri
                nama_peminjam = input("Masukkan nama peminjam: ")
                no_telepon = input("Masukkan nomor telepon: ")
                alamat = input("Masukkan alamat: ")

                tanggal_pinjam = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                for buku in temp_buku:  # iterasi sebanyak temp_buku
                    # menambah data peminjam ke tabel data_pinjam
                    cursor.execute("INSERT INTO data_pinjam (nama_peminjam, no_telepon, alamat, tanggal_pinjam, id_buku) VALUES (%s, %s, %s, %s, %s)",
                                   (nama_peminjam, no_telepon, alamat, buku[0], tanggal_pinjam))

                    # ubah status ketersediaan buku menjadi 'Not Available'
                    jumlah_buku = len(temp_buku)
                    cursor.execute("UPDATE data_buku SET ketersediaan = 'Not Available' WHERE id_buku = %s",
                                   (buku[0],))

                # assign banyak temp_buku menjadi jumlah_buku
                jumlah_buku = len(temp_buku)
                # update jumlah buku yang dipinjam oleh peminjam
                cursor.execute(
                    "UPDATE data_pinjam SET jumlah = %s WHERE nama_peminjam = %s", (jumlah_buku, nama_peminjam))
                connection.commit()  # commit perubahan ke database
                # tampilkan jika peminjaman berhasil
                print("===== Peminjaman Buku Berhasil! =====")

        else:
            # jika buku yang dicari tidak ada
            print("Tidak ada buku yang tersedia.")

    except mysql.Error as err:    # jika terjadi error maka tampilkan error
        print(f"Error: {err}")

    finally:       # menutup database cursor
        if cursor:  # jika cursor ada maka jjalankan kode di bawah
            cursor.close()
        if connection:  # jika koneksi ada maka jalankan kode di bawah
            connection.close()


# fungsi peminjaman buku
def data_peminjaman():
    # memanggil fungsi database lalu disimpan pada var connection
    connection = connect_to_database()
    cursor = connection.cursor()    # menggunakan fungsi cursor() sbg pointer

    try:
        cursor.execute(
            "SELECT * FROM data_pinjam")    # memilih tabel data_buku
        peminjam = cursor.fetchall()    # return semua baris dlm tabel

        if peminjam:    # jika data buku ada
            for data in peminjam:  # looping sebanyak data peminjaman
                print(
                    f"- ID Peminjaman: {str(data[0]):<4} | Nama Peminjam: {str(data[1]):<10} | Tanggal Pinjam: {str(data[4]):<10} | Tanggal Pengembalian: {str(data[5]):<10}")
                # Menampilkan data peminjaman
        else:   # jika tidak ada data buku tampilkan kode di bawah
            print("===== Data buku tidak ditemukan =====")

    except mysql.Error as err:    # jika terjadi error maka tampilkan error
        print(f"Error: {err}")


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
