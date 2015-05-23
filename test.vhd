library ieee;
use ieee.std_logic_1164.all;

library work;

entity test is
  generic
    (
      g_ClkFreqMHz : real := 50.0
      );
  port
    (
      p_Clk, p_Clk2 : in std_logic;
      p_Rst         : in std_logic
      );
end test;

-------------------------------------------------------------------------------
-- Test architecture declaration
-------------------------------------------------------------------------------
architecture behavioral_test of test is
  signal sig1 : std_logic := '0';
begin

  sig1 <= not sig1;



end behavioral_test;
