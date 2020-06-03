## Simulation fake generator

### Class

* [SimulationFakeGenerator](../../devoutils/faker/generators/simulation_fake_generator.py)

### Doc

This is a basic generator to create simulations on the screen, useful to see how a template 
would work, etc., without risking sending data.

In short, it is a generator to display the data on the screen, as if you activated the flag 
`simulation` and` verbose` in any of the other generators

### CLI Usage

If you take any use of the CLI, be it file, bash, realtime, etc., 
and use the `--simulation` flag, instead of executing the chosen FakeGenerator, 
simulation will be used, which does not send or write anywhere, but displays in a screen  
the result of the template and the configuration values

You have more info, flags and options in [Terminal/Shell CLI usage](shellcli.md)
