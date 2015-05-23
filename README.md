# vhdl-dot-resurrection
vhdl-dot-resurrection

Follows the notes down here.
At the moment it works only with test2.vhd and test2_tb.vhd.
It also works with hier_test.vhd (test components).

result = yacc.parse(fileContents,debug=1)

NOTEs (and future improvements):
* does not support generate statements
* at the moment requires the keywords to be in small cases
* to be tested with generate statements
* ENTITY DECLARATION:
  requires entity <NAME> ... end <NAME>
     -> can the parser be modified to support this?
* COMPONENT DECLARATION:
  requires G1 : INV port map (A => A_s, F => F_s);
  For example, G1 : INV port map (A_s, F_s); is not supported.
     -> can the parser be modified to support this?
  However it supports G1 : INV port map (A => A_s, F => F_s);
  or G1 : INV port map (F => F_s, A => A_s); giving the same result
  for both.
      -> is it possible to connect ports directly to components without
      having to go through signals?
* inout ports are not supported
* complex components (e.g. cpu) have a very bad visualization of signals interconnections...
  How can this be improved?

# General commands and use guide

python vhdl-dot.py hier_test.vhd
dot -Tpdf ier_test.dot -o ier_test.pdf

if using emacs as editor to show pdf, use M-x auto-revert-mode to update pdf every time it changes

# Comments and notes for future:

* Ports are rectangles, octagons are signals
* Update to pygraphviz, as George did for f2dot?
* Take insp from f2dot
* COMPLETE THIS README WITH COMMENTS FROM PAPER
* Careful, sometime signal is used instead of ports...

