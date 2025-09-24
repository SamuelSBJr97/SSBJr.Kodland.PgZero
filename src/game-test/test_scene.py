from game.scene import Scene, SceneManager


class DummyScene(Scene):
    def __init__(self, name):
        super().__init__(name)
        self.entered = False
        self.exited = False

    def on_enter(self, prev_scene):
        self.entered = True

    def on_exit(self, next_scene):
        self.exited = True


def test_scene_push_pop():
    mgr = SceneManager()
    s1 = DummyScene("s1")
    s2 = DummyScene("s2")
    mgr.push(s1)
    assert mgr.current is s1
    mgr.push(s2)
    assert mgr.current is s2
    popped = mgr.pop()
    assert popped is s2
    assert mgr.current is s1


def test_replace():
    mgr = SceneManager()
    s1 = DummyScene("s1")
    s2 = DummyScene("s2")
    mgr.push(s1)
    mgr.replace(s2)
    assert mgr.current is s2
    assert s1.exited
    assert s2.entered
