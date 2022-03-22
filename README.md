# Socialt medie til børn
Template-projekt for et lille socialt medie til børn, som skal færdiggøres i et tværfagligt forløb med KomIT og Programmering.

## Oversigt over koden
Projektet er opdelt i en række Python-filer, og derudover nogle statiske filer. I skal primært bekymre jer om `main.py`, og om filerne i mapperne `pages` og `static`.

### main.py
I filen `main.py` findes de forskellige handlers. Der er overordnet to typer:
* Handlers der viser en side ved at kalde funktioner fra de forskellige filer i `pages`-mappen. Nogle af dem læser først data fra databasen, andre gør ikke. Disse er generelt annoteret med `@app.get(...)`.
* Handlers der opdaterer noget i databasen, hvorefter de redirecter til en anden side. Disse er generelt annoteret med `@app.post(...)`.

Den eneste handler der ikke falder pænt i en af ovenstående kategorier er `logout`-handleren, som er annoteret med `@app.get("/logout")`, og som ændrer - ikke i databasen, men i en variabel - og derefter redirecter til forsiden.

### pages
Under mappen `pages` findes den Python-kode, der genererer de forskellige html-sider. F.eks. er der `pages/login.py`, som laver den HTML der skal vises på login-siden. Koden er pakket pænt ind i en funktion, som vi kan kalde fra andre moduler.

Her bruges `dominate` til at generere den HTML-kode der skal vises.

### static
Under mappen `static` findes CSS-filer, billeder, og andre filer som ikke afhænger af Python-koden. Som udgangspunkt er det bare en enkelt CSS-fil, men I kommer sandsynligvis til at tilføje flere filer her.

### Database-kode
Under mappen `database` findes filerne `dao.py`, `post.py`, og `user.py`, som alle har med databasen at gøre. Disse filer skal I ikke ændre på i dette projekt, men her er alligevel en kort forklaring:

* I `database/dao.py` defineres hvad et *Database Access Object*, eller DAO, skal kunne - det er generisk kode til at holde styr på en database-forbindelse.
* I `database/post.py` defineres så et mere konkret DAO som har med posts at gøre. Denne såkaldte PostDAO indeholder funktioner, der kan oprette og hente posts fra databasen.
* Tilsvarende indeholder `database/user.py` kode for en UserDAO, som tillader os at oprette og hente brugere i databasen.

### auth.py
Denne sidste fil indeholder kode der har med login-systemet at gøre. Den tillader os at bruge decoratoren `@protected` til at specificere at en side kun skal kunne tilgås, hvis brugeren er logget ind.
