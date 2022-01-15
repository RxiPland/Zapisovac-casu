# Zapisovač času

Pro spuštění celého programu slouží main.py

#
Odkaz pro stažení programu v exe (64bit windows) [stáhnout](https://github.com/RxiPland/zapisovac-casu/releases/download/v1.0.1/zapisovac_casu.exe)
<br/>
<br/>
`a68cb13d0258ed559027a09c1fa7d7ee4203e910b0199459fe37c244747c820d` (SHA256)
#

Program slouží pro kontrolu vašeho času stráveného na určité činnosti. Jednoduše na začátku vaší činnosti kliknete v programu na "Zapsat začátek" a program můžete klidně zavřít. Jakmile s prací skončíte nebo vás přestane bavit, otevřete program a zmáčknete "Zapsat konec" a příště tento cyklus opakujete. Vždy se zaznamená datum a čas začátku a pak i konce a všechno se to nakonec sečte. Je to něco jako příchod a odchod v práci. Cílem toho je zjistit, jak dlouho jste danou aktivitu dlouhodobě vykonávali. V admin panelu se nachází možnosti s přejmenováním projektu nebo změnou hesla. Mimo jiné je zde pak i tabulka se statistikami. Tam se ukazuje např. už zmíněný celkový strávený čas, nebo datum prvního začátku. Nově se zde také nachází možnost psaní poznámek. Přístup do admin panelu je možný uzamknout heslem. Heslo je zašifrované v SHA256 hashi v souboru se stejným názvem jako projekt a koncovka .heslo (Heslo se dá se nastavit při vytváření nového projektu nebo pak v admin části tlačítkem pro změnu hesla. Pokud budete chtít heslo odstranit, kliknete na změnit heslo a pole necháte prázdné). Projektů se zapsanými časy můžete mít i více. Stačí vytvořit nový a vybrat ho.

#

Bylo by vhodné dát program do složky, protože se na stejném místě vytvoří databáze a soubor s heslem.
#

# Použité knihovny:
```
pip install PyQt5
```

# Náhled:

![screen1](https://user-images.githubusercontent.com/82058894/148750531-a5be1b91-1bff-486e-9694-e1d06ac16816.png)

![screen2](https://user-images.githubusercontent.com/82058894/148751257-2115e1fe-3660-4575-b2d6-2c13a5e48303.png)

![screen3](https://user-images.githubusercontent.com/82058894/148751420-421ddd96-58d1-4e9a-8514-fc26ebdcedae.png)

![screen4](https://user-images.githubusercontent.com/82058894/149635799-c6cb1f7d-ccc6-445c-8821-2a960398d576.png)

![screen5](https://user-images.githubusercontent.com/82058894/149635816-720f50ba-b557-455a-a9e7-297408537fa9.png)
