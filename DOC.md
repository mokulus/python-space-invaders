# Space Invaders

Autor: Mateusz Okulus

# Projekt

## Opis

Program implementuje grę bardzo podobną do oryginalnej gry Space
Invaders. Po uruchomieniu gra prezentuje animowane menu z informacją o
najwyższym wyniku jaki udało się uzyskać i o tym ile punktów daje
zestrzelenie poszczególnych typów kosmitów. Grę można zacząć klikając
klawisz enter. Po wciśnięciu prezentowany jest interfejs użytkownika, a
kosmici zaczynają być animowani. Po skończeniu animacji pojawia się
statek gracza. Gracz może poruszać się za pomocą klawiszy A i D na lewo
i prawo oraz strzelać za pomocą spacji. Gracz zaczyna z czterema
tarczami.

## Kosmici

W każdej rundzie pojawia się 55 kosmitów w 5 wierszach po 11 w trzech
typach. Kosmici poruszają się między granicami gry naprzemienie w prawo
i lewo. Przy granicy przeskakują też w dół. W każdej klatce gry porusza
się tylko jeden kosmita, co nadaje grze dynamiki - 5 kosmitów porusza się
11 razy szybciej niż na początku.

## Pociski kosmitów

Kosmici strzelają trzema typami pocisków. Dwa z nich są tworzone w
odpowiednich kolumnach, tak jak w oryginalnej grze. Ostatni pojawia się
zawsze w tej samej kolumnie co gracz. Kosmici strzelają kiedy w grze nie
ma żadnych pocisków lub gdy od ostatniego strzału minęło wystarczająco
dużo czasu, ustalonego na podstawie liczby punktów uzyskanych przez
gracza. Jeżeli pocisk danego typu jest już w grze, to pociski tego
samego typu nie zostaną już wystrzelone.

## Gracz

Gracz strzela tylko jednym typem pocisku. Jeżeli w grze jest już jego
pocisk, to nie może on wystrzelić następnego. Gracz zaczyna z trzema
życiami. Po trafieniu kosmici zatrzymują się na chwilę i wyświetlana
jest animacja niszczenia staku gracza. Życia wyświetlane są w lewym
dolnym rogu. Po utraceniu wszystkich żyć gra kończy się.

## Eksplozje

Pociski gracza i kosmitów eksplodują przy kolizji. Obydwa typy mogą
uszkodzić tarcze chroniące gracza. Chybione pociski kosmitów ekplodują
na poziomej linii oddzielającej wyświetlane życia gracza, a chybione
pociski gracza eksplodują przed interfejsem wyświetlającym uzyskane
punkty. Kosmici również eksplodują po trafieniu pociskiem gracza.

## Tarcze

Tarcze mogą być niszczone przez pociski kosmitów i gracza, kawałek po
kawałku, tak jak w oryginalnej grze.

## Spodek

W grze co pewien czas pojawia się specjalny spodek. Pojawia się on nad
kosmitami, poniżej informacji z punktami. Może poruszać się od prawej do
lewej strony gry lub odwrotnie, w zależności od liczby wystrzelonej
przez gracza pocisków. Licza punktów uzyskana z jego zestrzelenia
również zależy od liczby wystrzelonych pocisków. Można otrzymać od 50 do
300 punków. Informacja o liczbie uzykanych punktów jest krótko
wyświetlana po zestrzeleniu.

## Rundy

Gra przechodzi do następnej rundy po zestrzeleniu wszystkich kosmitów
przez gracza. Z kolejnymi rundami kosmici pojawiają się coraz bliżej
tarcz. Dodatkowo wraz z większym wynikiem kosmici strzelają coraz
szybciej.

## Koniec gry

Gra kończy się gdy gracz stracił wszystkie życia lub gdy gdy kosmici są
zbyt blisko gracza. Kosmici przechodzą przez tarcze całkowicie je
niszcząc.

# Podział programu

Gra składa się z obiektów (pociski, eksplozje itp.) i systemów, które
zarządzają logiką tworzenia tych obiektów. Następnie w pętli gry
wszystkie systemy i obiekty są aktualizowane i informowane o
ewentualnych kolizjach.

- `System` - ogólna definicja systemu.
- `GameObject` - ogólna definicja obiektu.
- `Game` - aktualizuje wszystkie systemy i obiekty, sprawdza kolizje.
  Przechowuje też ogólne informacje o grze, takie jak wynik i numer
  rundy. Umożliwia dodawanie systemów i obiektów.
- `GameSettings` - zbiór ustawień gry.
- `CheatGameSettings` - zbiór ustawień gry z włączonymi kodami.

- `Point` - prosty dwuwymiarowy punkt.
- `Animation` - prosta animacja cyklicznie przechodząca przez listę
  obrazków, używana np. do animowania kosmitów.
- `StaticSprite` - prosty obiekt który składa się tylko z obrazka.
- `TextObject` - `StaticSprite` wyświetlający tekst.
- `VariableTextObject` - `TextObject` wyświetlający zmienny tekst, używany
  do wyświetlania wyniku gracza.
- `Input` - flagi używane przez `Player` do wykonywania akcji. Umożliwia
  jednoczesne strzelanie i poruszanie się gracza.
- `GameOver` - pomocnicza animacja końca gry. Po zakończeniu wraca do
  menu.
- `DeathAnimation` - pomocnicza animacja niszczenia gracza.
- `TextAnimation` - animacja teksu, używana do wyświetlenia GAME OVER i
  początkowej animacji menu.

- `Alien` - kosmita. Tworzy eksplozję przy zniszczeniu i dodaje
  odpowiednią liczbę punktów do wyniku. Za poruszanie się kosmitów
  odpowiada `AlienSystem`.
- `Shield` - tarcza która może być niszczona przez ekplozje.
- `Bullet` - abstrakcyjna klasa pocisku, który eksploduje przy wyjściu
  poza zakres gry i w przypadku pewnych kolizji.
- `PlayerBullet` - pocisk gracza.
- `AlienBullet` - pocisk kosmity.
- `Explosion` - prosty obiekt wyświetlający obrazek przez określoną
  liczbę klatek, po których zostaje usunięty.
- `Player` - gracz. Umożliwia sterowanie, dostęp do liczby żyć i liczby
  wystrzelonych pocisków oraz czy gracz jest w trakcie niszczenia.
- `SaucerExplosion` - pomocnicza eksplozja która po zakończeniu dodatkowo
  wyświetli informację o wyniku.
- `Saucer` - spodek. Kierunek ruchu i ilość przyznanych punktów zależy od
  liczby wystrzelonych przez gracza pocisków, tak jak w oryginalnej
  grze.

- `LifeSystem` - system aktualizujący obiekty tworzące część interfejsu
  wyświetlającą liczbę żyć gracza.
- `ShieldSystem` - system tworzący tarcze.
- `GuiSystem` - system tworzący obieky wyświetlające wynik. Obecny w menu
  i w grze.
- `SaucerSystem` - system tworzący spodek z odpowiednią częstotliwością.
- `MenuSystem` - system animujący początkowe menu gry.
- `BulletSystem` - system tworzący pociski kosmitów. Decyduje kiedy,
  gdzie i jakiego typu powinien zostać wystrzelony pocisk.
- `AlienSystem` - system animujący kosmitów na początku gry i
  odpowiadający za ich poruszanie się.


# Instrukcja

Po uruchomieniu programu należy wcisnąć klawisz enter by zacząć grę. Nie
trzeba czekać na koniec animacji menu. W grze poruszamy się klawiszami A
i D w lewo i prawo. Strzelamy spacją.

# Kody

Do testowania gry można użyć opcji `--cheats` przy uruchamianiu
programu. Daje to graczowi niezniszczalność, możliwość ciągłego strzału
i zwiększa częstotliwość pojawiania się spodków.

# Źródła

* https://www.computerarcheology.com/Arcade/SpaceInvaders/Code.html

Strona z opisaną logiką gry, część z niej została odwzorowana w tym
programie. Zawiera także zakodowane grafiki obiektów gry.

* https://en.wikipedia.org/wiki/Space_Invaders

Ogólny opis gry Space Invaders.
