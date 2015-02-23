-------------------------------------------------------------------------------
--! @file
--! @brief Test module
--!
--! Implements test module for doxygen
-------------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.all;

library work;
-------------------------------------------------------------------------------
--! Test entity declaration
-------------------------------------------------------------------------------
entity test2_tb is
   
end test2_tb;
      
-------------------------------------------------------------------------------
--! Test architecture declaration
-------------------------------------------------------------------------------
architecture behavioral_test2_tb of test2_tb is

signal p_Clk,p_Rst,o_Out : std_logic :=0;  
  
begin

  test_1: entity work.test2
    port map (
      p_Clk => p_Clk,
      p_Rst => p_Rst,
      o_Out => o_Out);  
 
end behavioral_test_tb;
