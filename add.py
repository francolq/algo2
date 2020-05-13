from manimlib.imports import *
from aanim.list import List
from aanim.code import code_text, Code
from aanim.state import State, Value


class Add(Scene):

    def construct(self):
        # present code text
        code = Code(open('add.txt').read())
        #code.highlight(4)
        code.scale(0.5)
        code.to_edge(LEFT)
        self.add(code.text)
        self.wait()

        # present call
        call = code_text("add(s=\{4,7,-10\}, e=6)")
        call.to_edge(UP)
        call.shift(RIGHT * FRAME_WIDTH * 0.25)  # starting from ORIGIN
        self.play(Write(call))

        # start execution
        self.play(FadeIn(code.line))

        # variables
        vars = State([
            ('s', List([-10, 4, 7])),
            ('n', Value('0')),
            ('saux', List([])),
            ('is\_member', Value('false')),
            ('d', Value('X')),
        ])

        # place state in the middle right (not so nice)
        vars.scale(0.5)
        vars.next_to(call, DOWN, buff=MED_LARGE_BUFF)
        vars.move_to(ORIGIN + RIGHT * FRAME_WIDTH * 0.20)

        # parameter s
        self.play(Write(vars.var('s')))
        self.play(FadeIn(vars.value('s')))

        # declarations
        for name in ['n', 'saux', 'is\_member', 'd']:
            code.play_runstep(self)
            self.play(Write(vars.var(name)))

        # initializations
        code.play_runstep(self, 2)
        self.play(FadeIn(vars.value('n')))
        code.play_runstep(self, 1)
        saux = vars.value('saux')
        saux = vars.value('s').play_list_copy(self, saux)
        vars.set_value('saux', saux)
        code.play_runstep(self, 1)
        self.play(FadeIn(vars.value('is\_member')))       

        # main loop
        code.play_runstep(self, 3)
        nvals = [1, 2, 2]
        branch = [2, 2, 3]
        for i in range(3):
            # evaluate condition
            code.play_hint(self, 'true')

            # update d: head
            code.play_runstep(self, 1)
            d = vars.value('d')
            new_d = saux.play_head(self, d)
            vars.set_value('d', new_d)

            # evaluate if
            code.play_runstep(self, branch[i])
            vars.value('n').play_change(self, str(nvals[i]))

            # tail
            code.play_runstep(self, 5 - branch[i])
            saux.play_tail(self)

            # move back to condition
            code.play_runstep(self, -6)

        # loop terminates
        code.play_hint(self, 'false')

        # evaluate last if
        code.play_runstep(self, 9)
        code.play_hint(self, 'true')

        # list_add_at
        code.play_runstep(self, 1)
        vars.value('s').play_add_at(self, 2, 6)

        # list_destroy
        code.play_runstep(self, 3)
        self.play(FadeOut(saux))
        vars.del_value('saux')

        # end: fade out variables
        code.play_runstep(self, 1)
        s_var, s_value = vars.var('s'), vars.value('s')
        vars.del_var('s')
        self.play(FadeOut(vars))        

        # show result as list
        g = VGroup(s_var, s_value)
        # https://github.com/3b1b/manim/issues/865
        def f(g):
            g.move_to(ORIGIN + RIGHT * FRAME_WIDTH * 0.25)
            g.scale(2.0)
            return g
        self.play(ApplyFunction(f, g))

        # now as set
        result = code_text("\{6, 4,7,-10\}")
        result.replace(s_value)
        #result.set_height(s.get_height())  # too big
        result.shift(DOWN * 1.5)  # i would like to animate this
        #result.next_to(s, DOWN)
        self.play(FadeIn(result))  #, ApplyMethod(result.shift, DOWN))

        self.wait()
