from manimlib.imports import *


def list_segment(elems):
    """Segment of a list (do not draw handles)."""
    group = VGroup()

    width = 1.0
    height = 1.0
    v = height / 2.0
    h0 = width * len(elems) / 2.0
    top = Line(np.array([-h0, v, 0]), np.array([h0, v, 0]))
    bottom = Line(np.array([-h0, -v, 0]), np.array([h0, -v, 0]))
    group.add(top)
    group.add(bottom)

    for i, elem in enumerate(elems):
        h = - h0 + i * width
        vline = Line(np.array([h, v, 0]), np.array([h, -v, 0]))
        text = TextMobject(elem)
        text.move_to(np.array([h + width / 2.0, 0, 0]))
        group.add(vline)
        group.add(text)
    vline = Line(np.array([h0, v, 0]), np.array([h0, -v, 0]))
    group.add(vline)

    return group


def list_isegment(elems):
    """Initial segment of a list (only draw left handle)."""
    isegment = list_segment(elems)

    # handles
    width = 1.0
    height = 1.0
    hw = width * 0.1  # handle width
    hleft = Rectangle(height=height, width=hw)
    hleft.next_to(isegment, LEFT, buff=0)
    isegment.add(hleft)

    return isegment


def list_fsegment(elems):
    """Final segment of a list (only draw right handle)."""
    fsegment = list_segment(elems)

    # handles
    width = 1.0
    height = 1.0
    hw = width * 0.1  # handle width
    hright = Rectangle(height=height, width=hw)
    hright.next_to(fsegment, RIGHT, buff=0)
    fsegment.add(hright)

    return fsegment


def list(elems):
    """Entire list (draw both handles)."""
    segment = list_segment(elems)

    # handles
    width = 1.0
    height = 1.0
    hw = width * 0.1  # handle width
    hleft = Rectangle(height=height, width=hw)
    hleft.next_to(segment, LEFT, buff=0)
    hright = Rectangle(height=height, width=hw)
    hright.next_to(segment, RIGHT, buff=0)
    segment.add(hleft, hright)

    return segment


class List(VGroup):

    def __init__(self, elems):
        VGroup.__init__(self)
        self.list_elems = elems
        self.list_view = list(elems)
        self.add(self.list_view)

    def head_view(self):
        return self.list_view.submobjects[3]  # hack into the list view

    def play_tail(self, main):
        self.list_elems = self.list_elems[1:]

        view = self.list_view
        view2 = list(self.list_elems)
        view2.replace(view, dim_to_match=1)
        #view2.set_height(view.get_height())  # just do dim_to_match=1
        view2.align_to(view, RIGHT)
        main.add(view2)
        main.play(FadeOut(view))
        main.play(ApplyMethod(view2.align_to, view, LEFT))
        self.list_view = view2
        self.remove(view)
        self.add(view2)

    def play_add_at(self, main, index, elem):
        elems = self.list_elems
        view = self.list_view

        left = list_isegment(elems[:index])
        left.replace(view, dim_to_match=1)
        left.align_to(view, LEFT)

        right = list_fsegment(elems[index:])
        right.replace(view, dim_to_match=1)
        right.align_to(view, RIGHT)

        result = elems[:index] + [elem] + elems[index:]
        self.list_elems = result

        view2 = list(result)
        view2.replace(view, dim_to_match=1)
        view2.align_to(view, LEFT)

        main.add(left, right)
        main.remove(view)
        main.play(FadeOut(view))
        #main.remove(view)  # XXX: need this?
        main.play(ApplyMethod(right.align_to, view2, RIGHT))
        main.play(FadeIn(view2))
        main.remove(left, right)

        self.list_view = view2
        self.remove(view)
        self.add(view2)

    def play_elim_at(self, main, index):
        elems = self.list_elems
        view = self.list_view
        result = elems[:index] + elems[index + 1:]

        # animation part
        left = list_isegment(elems[:index])
        left.replace(view, dim_to_match=1)
        left.align_to(view, LEFT)

        right = list_fsegment(elems[index + 1:])
        right.replace(view, dim_to_match=1)
        right.align_to(view, RIGHT)

        main.add(left)
        main.add(right)
        main.play(FadeOut(view))
        #main.remove(view)  # XXX: need this?
        main.play(right.next_to, left, RIGHT, 0.0)  # buff=0.0
        main.remove(left, right)

        view2 = list(result)
        view2.replace(view, dim_to_match=1)
        view2.align_to(view, LEFT)
        main.add(view2)

        # semantic part
        self.list_elems = result
        self.list_view = view2
        self.remove(view)
        self.add(view2)

    def play_list_copy(self, main, dest):
        """
        dest -- only use to mark destination
        """
        copy = self.copy()
        dest2 = List(self.list_elems)
        dest2.replace(dest, dim_to_match=1)
        dest2.align_to(dest, LEFT)
        main.play(ReplacementTransform(copy, dest2, path_arc=-4))
        #main.remove(copy)  # removes both (?!)
        #main.remove(dest2)  # removes both (?!)
        return dest2

    def play_head(self, main, dest):
        """
        dest -- only use to mark destination
        """
        head = self.head_view().copy()
        #self.play(Transform(head, dest, path_arc=-4), FadeOut(dval))
        #self.play(ApplyMethod(head.replace, dest, 1, path_arc=-4))  # 1 is dim_to_match
        main.play(ApplyMethod(head.move_to, dest, path_arc=-4))
        main.remove(dest)
        return head
