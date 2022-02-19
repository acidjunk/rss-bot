from rss_bot.stripper import strip_tags


def test_stripper():
    html = """<p>Het project WinnerZ is een muzikaal overzicht op CD geproduceerd door zeven winnaars van de Eujazz Young Talent Award.<br />
De resultaten van de  live opnames zijn in een overzichtelijk representatieve productie gebundeld. De productie laat  niet alleen de kwaliteit van de winnaars horen, maar geeft ook een beeld van “the next generation” wat en door wie gepresteerd wordt  in de Provincie Limburg.</p>"""
    stripped_html = strip_tags(html)
    print(stripped_html)
    assert (
        stripped_html
        == """Het project WinnerZ is een muzikaal overzicht op CD geproduceerd door zeven winnaars van de Eujazz Young Talent Award.
De resultaten van de  live opnames zijn in een overzichtelijk representatieve productie gebundeld. De productie laat  niet alleen de kwaliteit van de winnaars horen, maar geeft ook een beeld van “the next generation” wat en door wie gepresteerd wordt  in de Provincie Limburg."""
    )
