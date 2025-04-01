# tuman.py

def viloyatlar():
    """Barcha viloyatlar ro‘yxatini qaytaradi."""
    return [
        "Toshkent","Toshkent viloyati", "Andijon", "Samarqand", "Farg‘ona", "Namangan",
        "Buxoro", "Xorazm", "Surxondaryo", "Qashqadaryo", "Jizzax",
        "Navoiy", "Sirdaryo", "Qoraqalpog‘iston"
    ]

def get_tumanlar(viloyat):
    """Berilgan viloyatga tegishli tumanlarni qaytaradi."""
    tumanlar = {
        "Toshkent": ["Bektemir tumani", "Chilonzor tumani", "Hamza tumani", "Mirobod tumani", "Mirzo Ulugʻbek tumani", "Sergeli tumani", "Shayxontohur tumani", "Olmazor tumani", "Uchtepa tumani", "Yakkasaroy tumani", "Yunusobod tumani", "Yangihayot tumani"],
        "Toshkent viloyati": ["Bekobod tumani", "Boʻstonliq tumani", "Boʻka tumani", "Chinoz tumani", "Qibray tumani", "Ohangaron tumani", "Oqqoʻrgʻon tumani", "Parkent tumani", "Piskent tumani", "Quyi Chirchiq tumani", "Oʻrta Chirchiq tumani", "Yangiyoʻl tumani", "Yuqori Chirchiq tumani", "Zangiota tumani"],
        "Andijon": ["Andijon tumani", "Asaka tumani", "Baliqchi tumani", "Boʻston tumani", "Buloqboshi tumani", "Izboskan tumani", "Jalaquduq tumani", "Xoʻjaobod tumani", "Qoʻrgʻontepa tumani", "Marhamat tumani", "Oltinkoʻl tumani", "Paxtaobod tumani", "Shahrixon tumani", "Ulugʻnor tumani"],
        "Samarqand": ["Bulungʻur tumani", "Ishtixon tumani", "Jomboy tumani", "Kattaqoʻrgʻon tumani", "Qoʻshrabot tumani", "Narpay tumani", "Nurobod tumani", "Oqdaryo tumani", "Paxtachi tumani", "Payariq tumani", "Pastdargʻom tumani", "Samarqand tumani", "Toyloq tumani", "Urgut tumani"],
        "Farg‘ona": ["Oltiariq tumani", "Bagʻdod tumani", "Beshariq tumani", "Buvayda tumani", "Dangʻara tumani", "Fargʻona tumani", "Furqat tumani", "Qoʻshtepa tumani", "Quva tumani", "Rishton tumani", "Soʻx tumani", "Toshloq tumani", "Uchkoʻprik tumani", "Oʻzbekiston tumani", "Yozyovon tumani"],
        "Namangan": ["Chortoq tumani", "Chust tumani", "Kosonsoy tumani", "Mingbuloq tumani", "Namangan tumani", "Norin tumani", "Pop tumani", "Toʻraqoʻrgʻon tumani", "Uchqoʻrgʻon tumani", "Uychi tumani", "Yangiqoʻrgʻon tumani"],
        "Buxoro": ["Olot tumani", "Buxoro tumani", "Gʻijduvon tumani", "Jondor tumani", "Kogon tumani", "Qorakoʻl tumani", "Qorovulbozor tumani", "Peshku tumani", "Romitan tumani", "Shofirkon tumani", "Vobkent tumani"],
        "Xorazm": ["Bogʻot tumani", "Gurlan tumani", "Xonqa tumani", "Hazorasp tumani", "Xiva tumani", "Qoʻshkoʻpir tumani", "Shovot tumani", "Urganch tumani", "Yangiariq tumani", "Yangibozor tumani", "Tuproqqalʼa tumani"],
        "Surxondaryo": ["Angor tumani", "Boysun tumani", "Denov tumani", "Jarqoʻrgʻon tumani", "Qiziriq tumani", "Qumqoʻrgʻon tumani", "Muzrabot tumani", "Oltinsoy tumani", "Sariosiyo tumani", "Sherobod tumani", "Shoʻrchi tumani", "Termiz tumani", "Uzun tumani", "Bandixon tumani"],
        "Qashqadaryo": ["Chiroqchi tumani", "Dehqonobod tumani", "Gʻuzor tumani", "Qamashi tumani", "Qarshi tumani", "Koson tumani", "Kasbi tumani", "Kitob tumani", "Mirishkor tumani", "Muborak tumani", "Nishon tumani", "Shahrisabz tumani", "Yakkabogʻ tumani", "Koʻkdala tumani"],
        "Jizzax": ["Arnasoy tumani", "Baxmal tumani", "Doʻstlik tumani", "Forish tumani", "Gʻallaorol tumani", "Sharof Rashidov tumani", "Mirzachoʻl tumani", "Paxtakor tumani", "Yangiobod tumani", "Zomin tumani", "Zafarobod tumani", "Zarbdor tumani"],
        "Navoiy": ["Konimex tumani", "Karmana tumani", "Qiziltepa tumani", "Xatirchi tumani", "Navbahor tumani", "Nurota tumani", "Tomdi tumani", "Uchquduq tumani"],
        "Sirdaryo": ["Oqoltin tumani", "Boyovut tumani", "Guliston tumani", "Xovos tumani", "Mirzaobod tumani", "Sayxunobod tumani", "Sardoba tumani", "Sirdaryo tumani"],
        "Qoraqalpog‘iston": ["Amudaryo tumani", "Beruniy tumani", "Chimboy tumani", "Ellikqalʼa tumani", "Kegeyli tumani", "Moʻynoq tumani", "Nukus tumani", "Qanlikoʻl tumani", "Qoʻngʻirot tumani", "Qoraoʻzak tumani", "Shumanay tumani", "Taxtakoʻpir tumani", "Toʻrtkoʻl tumani", "Xoʻjayli tumani", "Taxiatosh tumani", "Boʻzatov tumani"]
    }
    return tumanlar.get(viloyat, [])  # Viloyat topilmasa bo‘sh ro‘yxat qaytaradi
