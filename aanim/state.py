from manimlib.imports import *
from aanim.code import code_text


class State(VGroup):

    def __init__(self, vars_values):
        VGroup.__init__(self)

        self.var_dict = var_dict = {}

        for i, (name, value) in enumerate(vars_values):
            # values to the right
            #var = algorithms.code(varname.ljust(maxlen) + ':')
            #var.shift(DOWN * i)
            #value.next_to(var, RIGHT)

            # values below
            var = code_text(name)
            var.shift(DOWN * 2.2 * i)
            var.align_to(ORIGIN, LEFT)
            self.add(var)
            if value is not None:
                value.next_to(var, DOWN)
                value.align_to(ORIGIN, LEFT)
                self.add(value)
            else:
                assert False
            
            var_dict[name] = (var, value)

    def var(self, name):
        return self.var_dict[name][0]
    
    def value(self, name):
        return self.var_dict[name][1]

    def set_value(self, name, value):
        var, old_value = self.var_dict[name]
        if old_value is not None:
            #value.replace(old_value, dim_to_match=1)
            self.remove(old_value)
        else:
            assert False
        #value.align_to(var, LEFT)
        #value.next_to(var, DOWN)
        self.add(value)
        self.var_dict[name] = (var, value)
    
    def del_var(self, name):
        var, value = self.var_dict[name]
        self.remove(var, value)

    def del_value(self, name):
        _, value = self.var_dict[name]
        self.remove(value)


class Value(VGroup):

    def __init__(self, value):
        VGroup.__init__(self)
        self.value = code_text(value)
        self.add(self.value)

    def play_change(self, main, value):
        old_value = self.value
        value2 = code_text(value)
        value2.replace(old_value)
        value2.set_height(old_value.get_height())
        value2.align_to(old_value, LEFT)
        main.play(Transform(old_value, value2))
