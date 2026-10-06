# Concurrenten: wat we overnemen en wat niet

Gevolgde accounts: [@zegna](https://www.instagram.com/zegna/), [@loropiana](https://www.instagram.com/loropiana/), [@boggimilanoofficial](https://www.instagram.com/boggimilanoofficial/), [@brunellocucinelli_brand](https://www.instagram.com/brunellocucinelli_brand/).

> **Stand:** basisanalyse van oktober 2026, op basis van de huidige campagnes en de vaste beeldtaal van de merken.
> Zodra Windsor.ai "Instagram Public" gekoppeld is, haalt Claude de echte posts op (zie `README.md`) en komen de cijfers per maand in `creative-engine/research/`.

## Loro Piana: rust als statement

- **FW26-campagne** door Mario Sorrenti (creatieve leiding Franck Durand), in de Menil Collection en de Rothko Chapel in Houston. Kleding in beweging en in gebruik, zonder dramatische styling, overdreven poses of zware effecten. Jonge en oudere modellen samen in dezelfde ruimte.
- **Vaste beeldtaal:** tonale neutrale kleuren (havermout, greige, navy), veel lege ruimte, grondstoffen (baby cashmere, vicuña), macro's van stof, weidse landschappen, loafers zonder sokken, nergens een logo.
- **Overnemen:** stille architectuur (shot `architecture`), beweging (lopen, niet poseren), macro van breisel (`texture`), still life (`still-life`), sokloze loafers.
- **Niet overnemen:** posts die zo abstract zijn dat je het product niet meer ziet. Wij moeten ook verkopen.

## Zegna: tonaal van top tot teen, in de natuur

- **FW26-show "A Family Closet"** (Alessandro Sartori, 16 januari 2026, Milaan): over tijd, continuïteit en doorgeven. Formeel en informeel door elkaar: gebreide stukken met tailoring.
- **Vaste beeldtaal:** Oasi Zegna (bergen, bossen, wol en cashmere vanaf de bron), tonale outfits in één kleurfamilie, mannen klein in een groot landschap.
- **Overnemen:** head-to-toe tonaal (onze paletten), landschap (`landscape`), twee generaties (`two-generations`), breigoed met een pantalon.
- **Niet overnemen:** sneakers, stropdassen, overjassen. Die verkopen we niet.

## Brunello Cucinelli: warmte en menselijkheid

- **FW26 menswear** (Milaan, 16 januari 2026): bruine trenchcoat over een crème col, een geruit jasje over een grijze col, gebroken witte broek. Laag over laag in neutrale tinten.
- **Vaste beeldtaal:** Solomeo in Umbrië, warm zonlicht op steen, oudere knappe modellen met grijze baard die lachen, gelaagd cashmere, ambacht (handen van vakmensen), filosofische captions.
- **Overnemen:** het dorp (`borgo`), interieur met zacht raamlicht (`interior`), lachende en oudere modellen, breisel over breisel (tee + cardigan, polo + Pieno gilet).
- **Niet overnemen:** sjaals, pochetten, zonnebrillen en ceintuurs die Cucinelli vaak toevoegt.

## Boggi Milano: dichtst bij onze prijs

- **2026:** officieel formalwear-leverancier van het FIFA WK 2026 en het vrouwen-WK 2027, met een licentiecapsule. Nieuwe winkels, onder meer in Bali.
- **Vaste beeldtaal:** commerciëler en vaker. Duidelijke productbeelden, stijltips, smart casual (polo met blazer), Riviera in de zomer, Milanese straten.
- **Overnemen:** helderheid over het product, carrousels "één look, drie beelden" (`styling`), binnenplaats (`milano-courtyard`), Riviera in de zomer (`riviera`), een vast ritme.
- **Niet overnemen:** uitverkoopsfeer, pakken en dassen, drukke stadsachtergronden met winkels en auto's.

## Samengevat: de ModernoMilano-mix

| Van | Nemen we | Shot in de engine |
|---|---|---|
| Loro Piana | rust, architectuur, beweging, stof van dichtbij | `architecture`, `texture`, `still-life` |
| Zegna | tonaal, landschap, generaties | `landscape`, `two-generations`, `studio-full` |
| Cucinelli | warmte, dorp, interieur, lachen | `borgo`, `interior`, `studio-portrait` |
| Boggi | productduidelijkheid, styling, ritme | `styling`-carrousel, `milano-courtyard`, `riviera` |

## Wat we per maand meten (zodra de koppeling er is)

Per account, uit `summarize()` in `src/creative/competitors.ts`:

- posts per week en verdeling foto, carrousel en video
- gemiddelde interactie (likes + reacties) en interactie als % van volgers
- welk type post het best scoort, en op welke weekdagen
- meest gebruikte hashtags
- top 5 posts van de maand, met link

Dat gaat naar `creative-engine/research/<jaar>-<maand>.md`, met per punt wat het betekent voor ons volgende raster.
