LIBRARY ieee;
USE ieee.std_logic_1164.all;

library work;

ENTITY test IS
  GENERIC
  (
    g_ClkFreqMHz     : real := 50.0
  );
  PORT
  (
    p_Clk      : in std_logic;
    p_Rst      : in std_logic
  ); 
END test;
      
-------------------------------------------------------------------------------
-- Test architecture declaration
-------------------------------------------------------------------------------
ARCHITECTURE behavioral_test OF test IS
  SIGNAL sig1 : STD_LOGIC := '0';
begin

    sig1 <= NOT sig1;

 
 
END behavioral_test;
