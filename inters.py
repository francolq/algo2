from manimlib.imports import *
from aanim.list import List
from aanim.code import code_text, Code
from aanim.state import State, Value


class Inters(Scene):

    def construct(self):
        # present code text
        code = Code(open('inters.txt').read())
        #code.highlight(4)
        code.scale(0.5)
        code.to_edge(LEFT)
        self.add(code.text)
        self.wait()

        # present call
        call = code_text("inters(s=\{4,7,-10\}, s0=\{-3,4,2\})")
        call.scale(0.8)
        call.shift(RIGHT * FRAME_WIDTH * 0.25)  # starting from ORIGIN
        call.to_edge(UP)
        self.play(Write(call))

        # group for parameters and variables
        state = VGroup()

        # parameters
        params = State([
            ('s', List([-10, 4, 7])),
            ('s0', List([-3, 2, 4])),
        ])
        state.add(params)

        # variables
        vars = State([
            #('saux', None),
            #('d', None),
            ('saux', List([])),
            ('d', Value('X')),
        ])
        vars.shift(DOWN * 2.2 * 3)
        #vars.next_to(params, DOWN, buff=MED_LARGE_BUFF)
        vars.align_to(params, LEFT)
        state.add(vars)

        # place state in the middle right (not so nice)
        state.scale(0.5)
        state.move_to(ORIGIN + RIGHT * FRAME_WIDTH * 0.25)

        # start execution
        self.play(FadeIn(code.line))

        # show params
        for name in ['s', 's0']:
            self.play(Write(params.var(name)))
            self.play(FadeIn(params.value(name)))

        # show variables
        for name in ['saux', 'd']:
            code.play_runstep(self)
            self.play(Write(vars.var(name)))

        # initialization
        code.play_runstep(self, 2)
        s = params.value('s')
        saux = vars.value('saux')
        saux = s.play_list_copy(self, saux)
        vars.set_value('saux', saux)

        # main loop
        code.play_runstep(self, 1)
        member = [False, True, False]
        elim = [0, None, 1]
        for i in range(3):
            # evaluate condition
            code.play_hint(self, 'True')

            # update d: head
            code.play_runstep(self, 1)
            d = vars.value('d')
            new_d = saux.play_head(self, d)
            vars.set_value('d', new_d)

            # evaluate inner if
            code.play_runstep(self, 1)
            value = not member[i]
            # TODO: highlight d and s0
            code.play_hint(self, str(value))
            if value:
                # true: elim
                code.play_runstep(self, 1)
                s = params.value('s')
                s.play_elim_at(self, elim[i])
                code.play_runstep(self, 2)
            else:
                code.play_runstep(self, 3)

            # tail
            saux.play_tail(self)

            # move back to condition
            code.play_runstep(self, -5)

        # loop terminates
        code.play_hint(self, 'false')

        # list destroy
        code.play_runstep(self, 7)
        self.play(FadeOut(saux))
        vars.del_value('saux')

        # end
        code.play_runstep(self, 1)
        s_var, s_value = params.var('s'), params.value('s')
        params.del_var('s')
        self.play(FadeOut(state))

        # display result
        g = VGroup(s_var, s_value)
        # https://github.com/3b1b/manim/issues/865
        def f(g):
            g.move_to(ORIGIN + RIGHT * FRAME_WIDTH * 0.25)
            g.scale(2.0)
            return g
        self.play(ApplyFunction(f, g))

        # now as a set
        result = code_text("\{4\}")
        result.replace(s_value)
        result.shift(DOWN * 1.5)  # i would like to animate this
        self.play(FadeIn(result))

        self.wait()
