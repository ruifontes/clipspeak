# Изговаряне на клипборда (Clipspeak)


## Информация
* Authors: Rui Fontes, Ângelo Abrantes, Abel Passos Júnior и със сътрудничеството на Noelia Ruiz Martínez, базирано на работата на Damien Sykes-Lindley
* Обновено на 21.03.2024 г.
* Изтегляне на [стабилна версия][1]
* Съвместимост с NVDA: 2019.3 и по-нови версии


##Представяне
\"Изговаряне на клипборда\" (\"Clipspeak\") е добавка, която позволява на NVDA автоматично да докладва операции в клипборда (като изрязване, копиране и поставяне), заедно с други общи операции за редактиране, като отмяна и повторение.
С цел избягване на съобщаването на тези операции в случаите в които те реално не се извършват, \"Изговаряне на клипборда\" извършва проверки на контролата и клипборда с цел да прецени дали в дадения случай трябва да се осъществи съобщаване.
Можете да избирате между само докладване на копирането/изрязването/поставянето или също какво се копира/изрязва/поставя в прозореца с настройките на NVDA, в раздела \"ClipSpeak\".
По подразбиране, командите (жестовете) на \"Изговаряне на клипборда\" съвпадат с тези, използвани в английските дистрибуции на Windows. Например:
* Control+Z: Отмяна
* Control+Y: Връщане
* Control+X: Изрязване
* Control+C: Копиране
* CTRL+SHIFT+C: Copy file path (Only in Windows 11)
* Control+V: Поставяне
Ако това не са командите, използвани за тези задачи във вашата версия на Windows, ще трябва да преназначите тези жестове в прозореца за настройка на жестовете на въвеждане на NVDA, в категорията \"Клипборд\".

[1]: https://github.com/ruifontes/clipspeak/releases/download/2025.06.13/clipspeak-2025.06.13.nvda-addon
