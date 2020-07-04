# Python-Ses-Asistan-
Öncelikle Bu ses assistanında Google Takvim'i de kullandığımı belirtmek isterim bunun için Google Takvim Api'nizi indirmeniz gerekecektir. Bu işlemi kısaca anlatmak gerekirse:

Google'a ait Google Calendar Api Sitesinden Api Kodunuzu indirmeniz gerek bunun için bir gmail ile bağlanmanız gerek ve sonra https://developers.google.com/calendar/quickstart/js sitesinden Api'nizi indirebilirsiniz. Eğer daha önce Google Developer için hiç işlem yapmadıysanız öncelikle bir Oauth Onayı yapmanız gerekecek Linki: https://console.developers.google.com/

Bu işlemleri yaptıktan sonra indirdiğiniz credentials.json dosyanızı Projenizin içine kopyalamalısınız ve paylaştığım kodda import ettiğim kütüphaneleri yüklemelisiniz. (yani pytz, gtts, playsound, speech_recognition)

Sonrasında da kodu kullanabilir yada genişletebilirsiniz.
Uygulamayı çalıştırdığınız zaman dinlemeye başlayacaktır ve "hey bilgisayar" komutu ile size "dinliyorum" diyecektir. Eğer şu kelimelere karşılık şu cevabı ver gibi komutlar eklemek isterseniz en sondaki gibi (SELAM_STRS) komutundaki gibi eklemeler yapabilirsiniz.
