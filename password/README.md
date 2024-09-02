Bu Python programı, bir şifre yöneticisidir ve kullanıcıların şifrelerini güvenli bir şekilde saklamasını, görüntülemesini ve silmesini sağlar.

#### Kullanılan Kütüphaneler:
- cryptography.fernet: Şifreleri şifrelemek ve çözmek için kullanılır.
- os: Dosya işlemleri için kullanılır (örn. şifreleme anahtarını kaydetmek veya yüklemek).
- tkinter: Grafiksel arayüz (GUI) oluşturmak için kullanılır.
#### Nasıl Çalışır:
- Şifreleme Anahtarı: Program, şifreleme için bir anahtar oluşturur ve key.key dosyasına kaydeder. Bu dosya yoksa, yeni bir anahtar oluşturur.
- Şifreleme ve Kaydetme: Kullanıcı bir site adı ve şifre girer. Şifre, şifrelenir ve passwords.txt dosyasına kaydedilir.
- Şifre Görüntüleme: Kullanıcı, doğru ana şifreyi girerse, kaydedilmiş şifreler çözülür ve gösterilir.
- Şifre Silme: Kullanıcı, bir şifreyi seçip silebilir. Bu işlem de doğru ana şifreyi gerektirir.
- Arayüz: Program, Tkinter ile oluşturulmuş basit bir arayüze sahiptir. Kullanıcı buradan şifreleri kaydedebilir, görüntüleyebilir ve silebilir.
Programın başlatılmasıyla ana arayüz açılır ve kullanıcı bu arayüzdeki butonlarla işlemlerini yapabilir.
