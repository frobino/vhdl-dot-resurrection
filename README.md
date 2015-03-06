# vhdl-dot-resurrection
vhdl-dot-resurrection

Follows the notes down here.
At the moment it works only with test2.vhd and test2_tb.vhd.
It also works with hier_test.vhd (test components).

result = yacc.parse(fileContents,debug=1)

NOTE:
	- does not support generate statements
	- at the moment requires the keywords to be in small cases
	- to be tested with generate statements
	- ENTITY DECLARATION:
	  requires entity <NAME> ... end <NAME>
	     -> can the parser be modified to support this?
	- COMPONENT DECLARATION:
	  requires G1 : INV port map (A => A_s, F => F_s);
	  For example, G1 : INV port map (A_s, F_s); is not supported.
	     -> can the parser be modified to support this?
	  However it supports G1 : INV port map (A => A_s, F => F_s);
	  or G1 : INV port map (F => F_s, A => A_s); giving the same result
	  for both.

	      -> is it possible to connect ports directly to components without
	      having to go through signals?