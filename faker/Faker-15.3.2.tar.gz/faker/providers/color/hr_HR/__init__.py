from collections import OrderedDict

from .. import Provider as ColorProvider

localized = True


class Provider(ColorProvider):
    """Implement color provider for ``hr_HR`` locale."""

    all_colors = OrderedDict(
        (
            ("Akvamarin", "#7FFFD4"),
            ("Antikna bijela", "#FAEBD7"),
            ("Azurna", "#F0FFFF"),
            ("Bež", "#F5F5DC"),
            ("Bijela", "#FFFFFF"),
            ("Bijelo bilje", "#FFFAF0"),
            ("Bjelokost", "#FFFFF0"),
            ("Blijeda kudelja", "#EEE8AA"),
            ("Blijedi badem", "#FFEBCD"),
            ("Blijedoljubičasta", "#DB7093"),
            ("Blijedotirkizna", "#AFEEEE"),
            ("Blijedozelena", "#98FB98"),
            ("Breskva", "#FFDAB9"),
            ("Brončana", "#D2B48C"),
            ("Čeličnoplava", "#4682B4"),
            ("Čičak", "#D8BFD8"),
            ("Cijan", "#00FFFF"),
            ("Čipka", "#FDF5E6"),
            ("Čokoladna", "#D2691E"),
            ("Crna", "#000000"),
            ("Crvena", "#FF0000"),
            ("Dim", "#F5F5F5"),
            ("Dodger plava", "#1E90FF"),
            ("Duboko ružičasta", "#FF1493"),
            ("Fuksija", "#FF00FF"),
            ("Gainsboro", "#DCDCDC"),
            ("Grimizna", "#DC143C"),
            ("Indigo", "#4B0082"),
            ("Jelenska koža", "#FFE4B5"),
            ("Kadetski plava", "#5F9EA0"),
            ("Kestenjasta", "#800000"),
            ("Koraljna", "#FF7F50"),
            ("Kraljevski plava", "#4169E1"),
            ("Kudelja", "#DAA520"),
            ("Lan", "#FAF0E6"),
            ("Lavanda", "#E6E6FA"),
            ("Limun", "#FFFACD"),
            ("Lipa", "#00FF00"),
            ("Ljubičasta", "#EE82EE"),
            ("Magenta", "#FF00FF"),
            ("Maslinasta", "#808000"),
            ("Medljika", "#F0FFF0"),
            ("Menta", "#F5FFFA"),
            ("Modro nebo", "#00BFFF"),
            ("Modrozelena", "#008080"),
            ("Mornarska", "#000080"),
            ("Morskozelena", "#2E8B57"),
            ("Mračno siva", "#696969"),
            ("Narančasta", "#FFA500"),
            ("Narančastocrvena", "#FF4500"),
            ("Narančastoružičasta", "#FA8072"),
            ("Noćno plava", "#191970"),
            ("Orhideja", "#DA70D6"),
            ("Papaja", "#FFEFD5"),
            ("Peru", "#CD853F"),
            ("Plava", "#0000FF"),
            ("Plavi prah", "#B0E0E6"),
            ("Plavi škriljevac", "#6A5ACD"),
            ("Plavkasta", "#F0F8FF"),
            ("Plavo cvijeće", "#6495ED"),
            ("Plavo nebo", "#87CEEB"),
            ("Plavoljubičasta", "#8A2BE2"),
            ("Porculanska", "#FFE4C4"),
            ("Prljavomaslinasta", "#6B8E23"),
            ("Proljetnozelena", "#00FF7F"),
            ("Prozirno bijela", "#F8F8FF"),
            ("Pšenica", "#F5DEB3"),
            ("Purpurna", "#800080"),
            ("Rajčica", "#FF6347"),
            ("Rumena lavanda", "#FFF0F5"),
            ("Ružičasta", "#FFC0CB"),
            ("Ružičastosmeđa", "#BC8F8F"),
            ("Siva", "#808080"),
            ("Sivi škriljevac", "#708090"),
            ("Sivožuta", "#F0E68C"),
            ("Smeđa", "#A52A2A"),
            ("Smeđe sedlo", "#8B4513"),
            ("Smeđi pijesak", "#F4A460"),
            ("Smeđkasto bijela", "#FFDEAD"),
            ("Snijeg", "#FFFAFA"),
            ("Srebrna", "#C0C0C0"),
            ("Srednja akvamarin", "#66CDAA"),
            ("Srednja crvenoljubičasta", "#C71585"),
            ("Srednja morskozelena", "#3CB371"),
            ("Srednja orhideja", "#BA55D3"),
            ("Srednja plava", "#0000CD"),
            ("Srednja proljetnozelena", "#00FA9A"),
            ("Srednja purpurna", "#9370DB"),
            ("Srednja tirkizna", "#48D1CC"),
            ("Srednje plavi škriljevac", "#7B68EE"),
            ("Svijetla čeličnoplava", "#B0C4DE"),
            ("Svijetla narančastoružičasta", "#FFA07A"),
            ("Svijetli cijan", "#E0FFFF"),
            ("Svijetlo drvo", "#DEB887"),
            ("Svijetlokoraljna", "#F08080"),
            ("Svijetlomorskozelena", "#20B2AA"),
            ("Svijetloplava", "#ADD8E6"),
            ("Svijetloružičasta", "#FFB6C1"),
            ("Svijetlosiva", "#D3D3D3"),
            ("Svijetlosivi škriljevac", "#778899"),
            ("Svijetlozelena", "#90EE90"),
            ("Svijetložuta kudelja", "#FAFAD2"),
            ("Svijetložuta", "#FFFFE0"),
            ("Šamotna opeka", "#B22222"),
            ("Školjka", "#FFF5EE"),
            ("Šljiva", "#DDA0DD"),
            ("Tamna kudelja", "#B8860B"),
            ("Tamna magenta", "#8B008B"),
            ("Tamna narančastoružičasta", "#E9967A"),
            ("Tamna orhideja", "#9932CC"),
            ("Tamna sivožuta", "#BDB76B"),
            ("Tamni cijan", "#008B8B"),
            ("Tamno zelena", "#006400"),
            ("Tamnocrvena", "#8B0000"),
            ("Tamnoljubičasta", "#9400D3"),
            ("Tamnomaslinasta", "#556B2F"),
            ("Tamnonarančasta", "#FF8C00"),
            ("Tamnoplava", "#00008B"),
            ("Tamnoplavi škriljevac", "#483D8B"),
            ("Tamnosiva", "#A9A9A9"),
            ("Tamnosivi škriljevac", "#2F4F4F"),
            ("Tamnotirkizna", "#00CED1"),
            ("Tamnozelena", "#8FBC8F"),
            ("Tirkizna", "#40E0D0"),
            ("Topla ružičasta", "#FF69B4"),
            ("Vedro nebo", "#87CEFA"),
            ("Voda", "#00FFFF"),
            ("Zelena lipa", "#32CD32"),
            ("Zelena šuma", "#228B22"),
            ("Zelena tratina", "#7CFC00"),
            ("Zelena", "#008000"),
            ("Zeleni liker", "#7FFF00"),
            ("Zelenožuta", "#ADFF2F"),
            ("Zlatna", "#FFD700"),
            ("Žućkastocrvena zemlja", "#CD5C5C"),
            ("Žućkastoružičasta", "#FFE4E1"),
            ("Žućkastosmeđa glina", "#A0522D"),
            ("Žuta svila", "#FFF8DC"),
            ("Žuta", "#FFFF00"),
            ("Žutozelena", "#9ACD32"),
        )
    )

    safe_colors = (
        "crna",
        "kestenjasta",
        "zelena",
        "mornarska",
        "maslinasta",
        "purpurna",
        "modrozelena",
        "lipa",
        "plava",
        "srebrna",
        "siva",
        "žuta",
        "fuksija",
        "voda",
        "bijela",
    )
