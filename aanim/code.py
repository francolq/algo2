from manimlib.imports import *


def code_text(text):
    #text = TextMobject("\\begin{verbatim}"
    #    + text
    #    + "\\end{verbatim}", alignment="")
    #return text

    #return SingleStringTexMobject("\\texttt{" + text + "}")  # set_color doesn't work here
    return TextMobject("\\texttt{" + text + "}")


class Code(VGroup):

    def __init__(self, text):
        VGroup.__init__(self)

        self.text = TextMobject(
            "\\begin{verbatim}"
            + text
            + "\\end{verbatim}", alignment=""
        )
        self.add(self.text)

        self.highlight(0)

    def highlight(self, line):
        # TODO: compute max line length
        #mark = TextMobject(r"\verb+>                                             <+")
        # XXX: > and | have different results
        mark = TextMobject(r"\verb+|                                                |+")
        mark.align_to(self, LEFT + TOP)

        rect = SurroundingRectangle(mark)
        mark.set_color(rect.color)

        self.line = VGroup(mark, rect)
        #self.line.set_color(rect.color)  # set_color doesn't work for VGroup it seems
        self.line.shift(DOWN * 0.3 * line)
        self.add(self.line)
        return self.line

    def play_runstep(self, main, size=1):
        main.play(ApplyMethod(self.line.shift, DOWN * 0.3 * size))

    def play_hint(self, main, hint):
        hint = code_text(hint)
        hint.set_color(YELLOW)
        hint.scale(0.6)
        hint.next_to(self.line, RIGHT)
        main.play(FadeIn(hint), duration=0.5)
        main.play(FadeOut(hint), duration=0.5)
