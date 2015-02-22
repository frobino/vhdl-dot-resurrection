LIBRARY ieee;
USE ieee.std_logic_1164.all;

library work;

entity test is
  port
  (
    p_Clk      : in std_logic;
    p_Rst      : in std_logic
    );
end test;
      
-------------------------------------------------------------------------------
-- Test architecture declaration
-------------------------------------------------------------------------------
architecture behavioral_test of test is
  signal sig1 : STD_LOGIC := '0';
begin

    sig1 <= not sig1;

 
 
end behavioral_test;
