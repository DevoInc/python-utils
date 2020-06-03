## Realtime fake generator

### Class

* [RealtimeFakeGenerator](../../devoutils/faker/generators/realtime_fake_generator.py)

### Doc

This generator is the parent class of several generators, but it is also useful for creating your own generators.

Just create a class like the example below, and create your own run function. With this you can add your own functions.

The important thing is, in the run function, call `self.realtime_iteration` sending your own write function in the 
variable `write_function` (It can be a send, or a print, or your own function to send it by https or a socket, anything.

    from .realtime_fake_generator import RealtimeFakeGenerator
    
    
    class MyCustomGenerator(RealtimeFakeGenerator):
        """Class to manage secure simulations of faker"""
        def __init__(self, template=None, **kwargs):
            RealtimeFakeGenerator.__init__(self, template=template, **kwargs)
    
        #You can override this function/Creat your own
        def run(self):
            """Run function for cli or call function"""
            #This call is neccesary for write/send/whatever, yo need send your function
            #in write_function. You receive in each call one text line
            self.realtime_iteration(write_function=lambda x: x) 
