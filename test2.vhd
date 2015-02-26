library ieee;
use ieee.std_logic_1164.all;

library work;

entity test is
  port
    (
      p_Clk : in  std_logic;
      p_Rst : out std_logic
      );
end test;

-------------------------------------------------------------------------------
-- Test architecture declaration
-------------------------------------------------------------------------------
architecture behavioral_test of test is
  signal sig1 : std_logic := '0';
begin

  

  sig1 <= not (p_Clk);
  p_Rst <= sig1;


end behavioral_test;
