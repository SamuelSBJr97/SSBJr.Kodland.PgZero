from game.entities import Jogador, Livro, Sala, Guardiao, Mapa, Cidade, Estrada


def test_livro_and_player_pick():
    l = Livro(id="l1", title="Livro 1")
    p = Jogador("Test")
    assert not l.collected
    p.pick_book(l)
    assert l.collected
    assert p.has_book("l1")


def test_room_and_guardian():
    s = Sala("Sala A", "Descricao")
    g = Guardiao("Guardiao")
    s.add_guardian(g)
    assert g in s.guardians


def test_map_connect():
    m = Mapa()
    s1 = Sala("A")
    s2 = Sala("B")
    m.add_room(s1)
    m.add_room(s2)
    m.connect("A", "B")
    assert "B" in m.connections["A"]
    assert "A" in m.connections["B"]
