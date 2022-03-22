# Socialt medie til børn
Template-projekt for et lille socialt medie til børn, som skal færdiggøres i et tværfagligt forløb med KomIT og Programmering.

## Oversigt over koden
Projektet er opdelt i en række Python-filer, og derudover nogle statiske filer. I skal primært bekymre jer om `main.py`, og om filerne i mapperne `pages` og `static`.

### static
Under mappen `static` findes CSS-filer, billeder, og andre filer som ikke afhænger af Python-koden. Som udgangspunkt er det bare en enkelt CSS-fil, men I kommer sandsynligvis til at tilføje flere filer her.

### pages
Under mappen `pages` findes den Python-kode, der genererer de forskellige html-sider. F.eks. er der `pages/login.py`, som laver den HTML der skal vises på login-siden. Koden er pakket pænt ind i en funktion, som vi kan kalde fra andre moduler.

### main.py
I filen `main.py` findes koden for de forskellige endpoints på siden. Dette inkluderer nogle endpoints som brugeren aldrig får at se, fordi de blot får noget kode til at køre (som f.eks. opdaterer databasen), og derefter redirecter videre til en anden side.

### Database-kode
Filerne `dao.py`, `post.py`, og `user.py` har med databasen at gøre. Disse filer skal I ikke ændre på i dette projekt, men her er alligevel en kort forklaring:

* I `dao.py` defineres hvad et *Database Access Object*, eller DAO, skal kunne - det er generisk kode til at holde styr på en database-forbindelse.
* I `post.py` defineres så et mere konkret DAO som har med posts at gøre. Denne såkaldte PostDAO indeholder funktioner, der kan oprette og hente posts fra databasen.
* Tilsvarende indeholder `user.py` kode for en UserDAO, som tillader os at oprette og hente brugere i databasen.

### auth.py
Denne sidste fil indeholder kode der har med login-systemet at gøre. Den tillader os at bruge decoratoren `@protected` til at specificere at en side kun skal kunne tilgås, hvis brugeren er logget ind.
